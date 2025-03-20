import time
import asyncio
import os
from flask import Flask
from telethon.sync import TelegramClient
from telethon import errors

app = Flask(__name__)

class TelegramForwarder:
    def __init__(self, api_id, api_hash, phone_number):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.client = TelegramClient('session_' + phone_number, api_id, api_hash)

    async def forward_messages_to_channel(self, source_chat_ids, destination_channel_id):
        await self.client.connect()
        await self.client.start()

        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone_number)
            await self.client.sign_in(self.phone_number, input('Enter the code: '))

        try:
            last_message_ids = {}
            chat_titles = {}

            # Get chat titles and last message IDs
            for chat_id in source_chat_ids:
                entity = await self.client.get_entity(chat_id)
                chat_titles[chat_id] = entity.title  # Store chat title
                
                messages = await self.client.get_messages(chat_id, limit=1)
                last_message_ids[chat_id] = messages[0].id if messages else 0

            while True:
                print("Checking for new messages...")

                for chat_id in source_chat_ids:
                    messages = await self.client.get_messages(chat_id, min_id=last_message_ids[chat_id], limit=10)

                    for message in reversed(messages):
                        if message.id > last_message_ids[chat_id]:
                            chat_title = chat_titles.get(chat_id, "Unknown Chat")
                            print(f"New message from {chat_title}: {message.text}")
                            await self.client.send_message(destination_channel_id, f"{chat_title}\n{message.text}")
                            last_message_ids[chat_id] = message.id
                            print("Message forwarded")

                await asyncio.sleep(1)

        except errors.FloodWaitError as e:
            print(f"Flood wait error! Sleeping for {e.seconds} seconds")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"Error: {e}")

def read_credentials():
    try:
        with open("credentials.txt", "r") as file:
            lines = file.readlines()
            api_id = lines[0].strip()
            api_hash = lines[1].strip()
            phone_number = lines[2].strip()
            return api_id, api_hash, phone_number
    except FileNotFoundError:
        print("Credentials file not found.")
        return None, None, None

async def start_forwarding():
    api_id, api_hash, phone_number = read_credentials()
    if api_id is None or api_hash is None or phone_number is None:
        print("Error: Missing credentials.")
        return

    forwarder = TelegramForwarder(api_id, api_hash, phone_number)
    destination_channel_id = # Add your destination channel ID here  
    source_chat_ids = [, ] # Add multiple chat IDs here
    
    await forwarder.forward_messages_to_channel(source_chat_ids, destination_channel_id)

@app.route('/')
def home():
    return "Telegram Forwarder is running!"

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_forwarding())
    port = int(os.getenv("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
