from pyrogram import Client
from pyrogram.types import Message
import os
import re
import time

api_id = 24379421
api_hash = "545969994106f7f812946b0a3be998ca"
channel_username = "DS_ML_DL_NLP"

base_download_folder = r"C:\Users\sony\Videos\AIML by Krish Naik"
os.makedirs(base_download_folder, exist_ok=True)

start_from_id = 20  # 👈 Set your starting message ID here

app = Client("my_session", api_id=api_id, api_hash=api_hash)

with app:
    print("✅ Logged in successfully.")

    messages = list(app.get_chat_history(channel_username, limit=10000))
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

                    file_path = app.download_media(message, file_name=full_path)

                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    print(f"✅ Saved: {file_path} ⏱️ Time taken: {elapsed_time:.2f} seconds")

                except Exception as e:
                    print(f"❌ Error downloading media: {e}")
