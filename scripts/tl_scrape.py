from telethon import TelegramClient
import logging
import asyncio
import csv
import os
import sqlite3
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')
TG_API_ID = os.getenv('TG_API_ID')
TG_API_HASH = os.getenv('TG_API_HASH')
phone = os.getenv('PHONE')

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to extract username from URL
def extract_username(url):
    parsed_url = urlparse(url)
    return parsed_url.path.strip('/')

# Function to scrape data from a single channel
async def scrape_channel(client, channel_url, data, media_dir):
    channel_username = extract_username(channel_url)
    entity = await client.get_entity(channel_username)
    channel_title = getattr(entity, 'title', channel_username)  # Extract the channel's title if it exists, otherwise use the username
    logging.info(f"Scraping data from channel: {channel_title}")
    async for message in client.iter_messages(entity, limit=150):  # Limit to 150 messages
        media_path = None
        if message.media and hasattr(message.media, 'photo'):
            # Create a unique filename for the photo
            filename = f"{channel_username}_{message.id}.jpg"
            media_path = os.path.join(media_dir, filename)
            # Check if the photo already exists to avoid re-downloading
            if not os.path.exists(media_path):
                # Download the media to the specified directory if it's a photo
                await client.download_media(message.media, media_path)
        
        # Append the channel title along with other data to the list
        data.append([channel_title, channel_username, message.id, message.message, message.date, media_path])
    logging.info(f"Finished scraping data from channel: {channel_title}")

# Function to save data to CSV
def save_to_csv(data, file_name='telegram_data.csv'):
    try:
        with open(file_name, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path'])  # Include channel title in the header
            for row in data:
                writer.writerow(row)
        logging.info(f"Data saved to {file_name}")
    except PermissionError as e:
        logging.error(f"Permission error: {e}")
    except Exception as e:
        logging.error(f"Error saving to CSV: {e}")

# Function to save data to the database
def save_to_database(data, db_file='telegram_data.db'):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Create a table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS telegram_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_title TEXT,
                channel_username TEXT,
                message_id INTEGER,
                message TEXT,
                date TEXT,
                media_path TEXT
            )
        ''')
        
        # Insert data into the database
        cursor.executemany('''
            INSERT INTO telegram_data (
                channel_title, channel_username, message_id, message, date, media_path
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', data)
        
        conn.commit()
        conn.close()
        logging.info("Data saved to database successfully")
    except sqlite3.Error as e:
        logging.error(f"SQLite error: {e}")
    except Exception as e:
        logging.error(f"Error saving to database: {e}")

# Initialize the client once
client = TelegramClient('scraping_session', TG_API_ID, TG_API_HASH)

async def main():
    async with client:
        await client.start()
        logging.info("Telegram client started.")
        
        # Create a directory for media files
        media_dir = 'photos'
        os.makedirs(media_dir, exist_ok=True)
        logging.info("Media directory created.")
        
        # Data list to store all messages
        data = []
        
        # List of channels to scrape
        channels = [
            'https://t.me/DoctorsET',
            'https://t.me/Chemed',
            'https://t.me/lobelia4cosmetics',
            'https://t.me/yetenaweg',
            'https://t.me/EAHCI'
            # Add more channels here from https://et.tgstat.com/medicine
        ]
        
        # Iterate over channels and scrape data into the single CSV file
        for channel in channels:
            await scrape_channel(client, channel, data, media_dir)
            logging.info(f"Scraped data from {channel}")

        # Save data to CSV and database separately
        save_to_csv(data)
        save_to_database(data)

# If running inside an existing event loop, use await
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError:
        # If there is an event loop already running, use await
        asyncio.ensure_future(main())
