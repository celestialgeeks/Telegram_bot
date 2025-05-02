from pyrogram import Client
import os
import re
import shutil

# === CONFIGURATION ===
api_id = "YOUR_API_ID" # Replace with your actual API ID (integer)
api_hash = "YOUR_API_HASH"  # Replace with your actual API Hash
channel_username = "@YourChannelUsername"  # Replace with the Telegram channel name
download_folder = r"C:\Users\sony\Videos\AIML by Krish Naik\Uncategorized"

# === HELPERS ===
def get_file_number(filename):
    match = re.match(r"(\d{3})", filename)
    return match.group(1) if match else None

# === INITIALIZE ===
app = Client("chapter_classifier_session", api_id=api_id, api_hash=api_hash)
chapter_map = {}  # {chapter_title: [file_numbers]}
chapter_list = []  # ordered list for interactive display
current_chapter = None

# === FETCH MESSAGES ===
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

# === SHOW CHAPTERS FOR SELECTION ===
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
print("\nOrganizing selected chapters...")
for chapter in selected_chapters:
    folder_path = os.path.join(download_folder, chapter)
    os.makedirs(folder_path, exist_ok=True)

    for filename in os.listdir(download_folder):
        file_path = os.path.join(download_folder, filename)
        if not os.path.isfile(file_path):
            continue
        file_number = get_file_number(filename)
        if file_number and file_number in chapter_map[chapter]:
            dest_path = os.path.join(folder_path, filename)
            print(f"Moving {filename} → {chapter}")
            shutil.move(file_path, dest_path)

print("\n✅ Done! Selected chapters have been organized.")
