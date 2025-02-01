import os
import logging
from telethon.tl.types import MessageMediaPhoto

# Function to download media (photos) from a message and save them to a folder
async def download_images(message, channel_name, client):
    """
    Download media (photos) from a Telegram message and save them to a specified folder.

    Args:
        message: The Telegram message containing media.
        channel_name: The name of the channel from which the image is downloaded.
        client: The Telegram client used to interact with the Telegram API.
    """
    try:
        # Create folder if it doesn't exist
        folder_path = '../data/photos/'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Check if the message contains a photo
        if isinstance(message.media, MessageMediaPhoto):
            file_path = os.path.join(folder_path, f"{channel_name}_{message.id}.jpg")
            await client.download_media(message.media, file_path)
            logging.info(f"Downloaded image from message {message.id} in {channel_name}")
        else:
            logging.info(f"No valid image found in message {message.id}.")
    except Exception as e:
        logging.error(f"Error downloading image from message {message.id}: {e}")
