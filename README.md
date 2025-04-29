# Telegram Channel Media Downloader

A Python bot that automatically downloads media files from a specified Telegram channel, organizing them into folders by chapters/topics.

## 🌟 Features

- Downloads all media (videos, documents, photos) from a specified Telegram channel
- Automatically organizes files into chapter folders based on message content
- Resumes downloads from where it left off if interrupted
- Shows download progress in real-time
- Handles rate limiting with automatic pauses
- Downloads media in the original quality

## 📋 Requirements

- Python 3.7+
- A Telegram account
- Telegram API credentials (API ID and Hash)

## 🔧 Installation

1. Clone this repository or download the script

2. Install the required dependencies:
   ```bash
   pip install pyrogram tgcrypto python-dotenv
   ```

3. Create a `.env` file in the same directory as the script with the following content:
   ```
   API_ID=your_telegram_api_id
   API_HASH=your_telegram_api_hash
   CHANNEL_USERNAME=target_channel_username
   ```

## 🔑 How to get Telegram API credentials

1. Visit https://my.telegram.org/auth and log in with your phone number
2. Go to "API development tools"
3. Create a new application (fill in any required fields)
4. Copy the "API ID" and "API Hash" values to your `.env` file

## 🚀 Usage

1. Configure the download folder in the script:
   ```python
   base_download_folder = r"C:\Users\your_username\Videos\your_folder"
   ```

2. Run the script:
   ```bash
   python downloader.py
   ```

3. The first time you run the script, you'll be prompted to enter your phone number and the authentication code sent to your Telegram account.


```
Base Download Folder/
├── 01 - Chapter Title/
│   ├── file1.mp4
│   ├── file2.pdf
│   └── ...
├── 02 - Another Chapter/
│   ├── file1.mp4
│   └── ...
└── Uncategorized/
    ├── file1.jpg
    └── ...
```

## ⚙️ How It Works

1. The script connects to Telegram using your API credentials
2. It retrieves messages from the specified channel
3. It automatically detects chapter titles from messages using regex patterns
4. For each media file, it:
   - Creates the appropriate chapter folder
   - Downloads the file with a progress bar
   - Saves the last processed message ID for resuming later

## 📝 Resuming Downloads

The script creates a `last_id.txt` file that stores the ID of the last successfully downloaded message. If the script is interrupted, it will resume from this point when restarted.

## ⚠️ Rate Limiting

Telegram has rate limits for downloads. If an error occurs, the script will pause for 10 seconds before continuing, helping to avoid temporary blocks.

## 🛠️ Customization

- To change the number of messages to retrieve, modify the `limit` parameter:
  ```python
  messages = list(app.get_chat_history(CHANNEL_USERNAME, limit=10000))
  ```

- To customize the chapter detection pattern, modify the regex in the code:
  ```python
  match = re.match(r'^\s*(\d{1,2})[\s\-\.:]+(.+)', text_to_check.strip())
  ```

## 📄 License

This project is open source and available for personal use.

## 🙏 Acknowledgements

This script uses [Pyrogram](https://docs.pyrogram.org/), a powerful Telegram client library for Python.