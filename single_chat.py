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

    async def forward_messages_to_channel(self, source_chat_id, destination_channel_id):
        await self.client.connect()
        await self.client.start()  # Ensure client is fully started

        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone_number)
            await self.client.sign_in(self.phone_number, input('Enter the code: '))

        try:
            last_message_id = (await self.client.get_messages(source_chat_id, limit=1))[0].id  

            while True:
                print("Checking for new messages...")
                messages = await self.client.get_messages(source_chat_id, min_id=last_message_id, limit=10)

                for message in reversed(messages):
                    if message.id > last_message_id:  
                        print(f"New message: {message.text}")
                        await self.client.send_message(destination_channel_id, message.text)
                        last_message_id = message.id  
                        print("Message forwarded")

                await asyncio.sleep(5)

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
    destination_channel_id = # Add your destination channel ID here (where messages are going to)  
    source_chat_id = # Add the source chat's id (where messages are coming from)
    await forwarder.forward_messages_to_channel(source_chat_id, destination_channel_id)

@app.route('/')
def home():
    return "Telegram Forwarder is running!"

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_forwarding())  # Ensures proper async handling
    port = int(os.getenv("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
