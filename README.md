Download dependencies: pip install -r requirements.txt

Run the 'original.py' first by redianmarku to locat your desired chat's source and destination ID

You will need to enter your telegram phone number, api hash and api id which you can locate within the link below.

Next you will need to update either the single_chat.py (line 66 & line 67) or multiple_chat.py (line 78 & 79) file with your source chat/s id and destination id.

You can then head to https://dashboard.render.com/ (create an account) New > web service

Upload files to github and create a repository then link it to render and change root directory to ./telegram-bot and 
build command to pip install -r requirements.txt
and start command to python (single_chat or multiple_chats).py

Telegram API: https://my.telegram.org/apps

Copytrader: https://www.mql5.com/en/market/product/70538?source=External

