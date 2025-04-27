from pyrogram import Client
from pyrogram.types import Message
from dotenv import load_dotenv
import os
import re
import time

load_dotenv()
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")

base_download_folder = r"C:\Users\sony\Videos\AIML by Krish Naik"
os.makedirs(base_download_folder, exist_ok=True)

last_id_file = "last_id.txt"  

# 🛡️ Read last saved ID if available
if os.path.exists(last_id_file):
    with open(last_id_file, "r") as f:
        start_from_id = int(f.read().strip())
    print(f"🔄 Resuming from message ID {start_from_id}")
else:
    start_from_id = 66
    print(f"🚀 Starting fresh download.")

app = Client(
    "my_session",
    API_ID=API_ID,
    API_HASH=API_HASH,
    downloadd_timeout=1200,)

with app:
    print("✅ Logged in successfully.")

    messages = list(app.get_chat_history(CHANNEL_USERNAME, limit=10000))
    messages.reverse()

    current_chapter = "Uncategorized"
    for message in messages:
        if isinstance(message, Message):

            # 🚀 Skip messages before start_from_id
            if message.id < start_from_id:
                continue

            # 📘 Detect chapter from text or caption
            if message.text or message.caption:
                text_to_check = message.text if message.text else message.caption
                match = re.match(r'^\s*(\d{1,2})[\s\-\.:]+(.+)', text_to_check.strip())
                if match:
                    chapter_number = match.group(1).zfill(2)
                    chapter_title = match.group(2).strip()
                    current_chapter = f"{chapter_number} - {chapter_title}".replace(':', ' -').replace('/', '-')
                    print(f"\n📘 Chapter Detected: {current_chapter}")

            # 📥 If media present, download it
            if message.media:
                chapter_folder = os.path.join(base_download_folder, current_chapter)
                os.makedirs(chapter_folder, exist_ok=True)

                try:
                    suggested_filename = None
                    if message.document and message.document.file_name:
                        suggested_filename = message.document.file_name
                    elif message.video:
                        suggested_filename = f"{message.id}.mp4"
                    elif message.photo:
                        suggested_filename = f"{message.id}.jpg"
                    else:
                        suggested_filename = f"{message.id}.file"

                    full_path = os.path.join(chapter_folder, suggested_filename)

                    print(f"⬇️  Downloading from message ID {message.id}")
                    start_time = time.time()

                    file_path = app.download_media(
                        message,
                        file_name=full_path,
                        block_size= 512 * 1024)

                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    print(f"✅ Saved: {file_path} ⏱️ Time taken: {elapsed_time:.2f} seconds")

                    # 📝 Save the last successful downloaded message ID
                    with open(last_id_file, "w") as f:
                        f.write(str(message.id))

                except Exception as e:
                    print(f"❌ Error downloading media: {e}")
                    print(f"⏳ Waiting 10 seconds before continuing...")
                    time.sleep(3)  # Wait before retrying
                    continue  
