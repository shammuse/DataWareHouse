import logging
import pandas as pd

# Function to scrape messages and store in DataFrame
async def scrape_messages(channel_url, client):
    try:
        messages = []
        logging.info(f"Scraping messages from channel: {channel_url}")

        # Get the channel entity
        channel = await client.get_entity(channel_url)
        channel_name = channel.username or channel.title.replace(' ', '_')

        # Scrape messages from the channel
        async for message in client.iter_messages(channel):
            msg_id = message.id
            text = message.message if message.message else ''
            sender = message.sender_id if message.sender_id else 'Unknown'
            
            # Format message_id to include channel name and underscore
            formatted_msg_id = f"{channel_name}_{msg_id}"
            
            # Append message info to the list
            messages.append({
                'message_id': formatted_msg_id,
                'text': text,
                'sender': sender,
                'channel': channel_name,
                'date': message.date
            })
        
        # Convert list of messages to DataFrame
        df = pd.DataFrame(messages)
        logging.info(f"Finished scraping messages from channel: {channel_url}")
        return df
    except Exception as e:
        logging.error(f"Error scraping messages from channel {channel_url}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error
