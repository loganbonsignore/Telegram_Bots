import requests
import json
import time
import sys
from config import TOKEN, DEV_CHANNEL_ID

# Set up logging
# import logging
# logging.basicConfig(filename="notification_bot_logfile.txt",format="%(levelname)s:%(message)s",filemode="w",level=logging.DEBUG)

############################# Start Definitions #############################

class MessageHandler:
    def __init__(self):
        self.known_update_ids = set()

    def send_message(self, chat_id:str, message:str) -> None:
        # Send a message once the bot is started/start command is ran
        response = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id":chat_id, "text":message})
        response = json.loads(response.text)
        # If bad query...
        if not response["ok"]:
            raise LookupError(f"Bot startup failed. Telegram error message: '{response['description']}'")

class RuntimeHandler:
    def __init__(self):
        self.admins = ["loganbon"]
        self.first_run = True
    
    def main(self) -> None:
        # Entry point the bot
        self.hello_world()
        self.stay_idle()

    def hello_world(self) -> None:
        # Notifies chat the bot is live
        mh.send_message(DEV_CHANNEL_ID, "The Notifications Bot is live! \n\nAdmin can use 'stop notifications bot' to shutdown this bot.")
    
    def stay_idle(self) -> None:
        offset = 0
        while True:
            # Get list of updates
            response = requests.post(f"https://api.telegram.org/bot{TOKEN}/getUpdates", data={"offset":offset, "allowed_updates":["message", "channel_post"]})
            response = json.loads(response.text)
            # If bad query...
            if not response["ok"]:
                raise LookupError(f"Bot failed to get an update. Telegram error message: '{response['description']}'")
            # If launching bot and new 'stale' updates...
            if self.first_run and response["result"]:
                offset = self.update_offset_at_launch(response)
                continue
            # If new updates available...
            if response["result"]:
                # Execute new updates
                new_updates = response["result"]
                print(f"\nNew Updates: {len(new_updates)}") # Logging
                for update in new_updates:
                    if "channel_post" in update:
                        # Do something with channel_post
                        text = update["channel_post"]["text"]
                        print(f"New Channel Post: '{text}'") # Logging
                    elif "message" in update:
                        # Do something with direct message ...
                        chat_id = update["message"]["chat"]["id"]
                        text = update['message']['text']
                        # Check if message is 'stop' message from admin
                        # NOTE: Bot kill switch that admin uses from telegram app
                        self.check_for_admin_shutdown(update, text, chat_id)
                        # Confirm message recieved in chat 
                        mh.send_message(chat_id, f"Received your message: '{text}'")
                        print(f"New Message Text: '{text}'") # Logging
                # Tell telegram API we've handled responses below latest update_id
                offset = response["result"][-1]["update_id"]+1
            # If no new updates available...
            else:
                print(f"\nNew Updates: 0") # Logging
                if self.first_run:
                    self.first_run = False
            # Pause to get next update
            print("----------------------------------------") # Logging
            time.sleep(2)
    
    def check_for_admin_shutdown(self, update, text, chat_id) -> exit:
        message_sender = update["message"]["from"]["username"]
        if message_sender in self.admins and text.lower() == "stop notifications bot":
            mh.send_message(chat_id, f"Shutting down... at request of @{message_sender}")
            print(f"Shutting down... at request of @{message_sender}") # Logging
            sys.exit()

    def update_offset_at_launch(self, response):
        # Stop bot from acting on 'stale' updates at launch of bot's runtime code
        self.first_run = False
        offset = response["result"][-1]["update_id"]+1
        return offset

############################## End Definitions ##############################

mh = MessageHandler()
rh = RuntimeHandler()

if __name__ == "__main__":
    rh.main()