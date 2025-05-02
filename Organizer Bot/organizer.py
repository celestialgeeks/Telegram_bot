from pyrogram import Client
from dotenv import load_dotenv
import os
import re
import shutil
import argparse

# === LOAD ENVIRONMENT VARIABLES ===
load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
channel_username = os.getenv("CHANNEL_USERNAME") 
download_folder = r"C:\Users\sony\Videos\AIML by Krish Naik\Uncategorized"

# === ARGUMENT PARSER ===
parser = argparse.ArgumentParser(description="Organize Telegram course files by chapter.")
parser.add_argument("--dry-run", action="store_true", help="Preview file actions without copying.")
args = parser.parse_args()

# === HELPERS ===
def get_file_number(filename):
    match = re.match(r"(\d{3})", filename)
    return match.group(1) if match else None

# === FETCH FROM TELEGRAM ===
app = Client("chapter_classifier_session", api_id=api_id, api_hash=api_hash)
chapter_map = {}
chapter_list = []
current_chapter = None

with app:
    print("Fetching messages from Telegram channel...")
    for message in app.get_chat_history(channel_username, reverse=True):
        if message.text:
            match = re.match(r"^\d+\s*-\s*(.+)", message.text.strip())
            if match:
                current_chapter = message.text.strip()
                chapter_map[current_chapter] = []
                chapter_list.append(current_chapter)
        elif message.document or message.video:
            if current_chapter:
                filename = message.document.file_name if message.document else message.video.file_name
                file_number = get_file_number(filename)
                if file_number:
                    chapter_map[current_chapter].append(file_number)

# === INTERACTIVE SELECTION ===
print("\nAvailable Chapters:")
for idx, chapter in enumerate(chapter_list):
    print(f"[{idx}] {chapter} ({len(chapter_map[chapter])} files)")

selection = input("\nEnter chapter numbers to organize (comma-separated, or 'all'): ").strip()

if selection.lower() == "all":
    selected_chapters = chapter_list
else:
    indices = [int(i) for i in selection.split(",") if i.strip().isdigit()]
    selected_chapters = [chapter_list[i] for i in indices if 0 <= i < len(chapter_list)]

# === ORGANIZE FILES ===
if args.dry_run:
    print("\n🧪 Dry Run: The following files WOULD be copied:")
else:
    print("\nCopying selected chapters into folders (original files untouched)...")

for chapter in selected_chapters:
    folder_path = os.path.join(download_folder, chapter)
    if not args.dry_run:
        os.makedirs(folder_path, exist_ok=True)

    for filename in os.listdir(download_folder):
        file_path = os.path.join(download_folder, filename)
        if not os.path.isfile(file_path):
            continue
        file_number = get_file_number(filename)
        if file_number and file_number in chapter_map[chapter]:
            dest_path = os.path.join(folder_path, filename)
            if args.dry_run:
                print(f"[DRY RUN] Would copy: {filename} → {chapter}")
            else:
                print(f"Copying {filename} → {chapter}")
                shutil.copy2(file_path, dest_path)

print("\n✅ Done!" if not args.dry_run else "\n✅ Dry run complete. No files were modified.")
