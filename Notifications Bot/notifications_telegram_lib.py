# import necessary libraries
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from config import TOKEN, DEV_CHANNEL_ID

# set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#################################### Start Definitions ####################################

def start(update, context):
    # send a message once the bot is started/start command is ran
    update.message.reply_text('Testing 123')

def hello(update, context):
    # send a message once the command /hello is keyed
    update.message.reply_text('Hello World! \U0001F600')

# for error debugging
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

# to start the bot
def main():
    # setup updating together with our telegram api token
    updater = Updater(TOKEN, use_context=True)

    # get the dispatcher to register handlers
    dp = updater.dispatcher

    # add command handlers for different command
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("hello", hello))

    # error logging
    dp.add_error_handler(error)

    # start the bot
    updater.start_polling()

    # set the bot to run until you force it to stop
    updater.idle()

##################################### End Definitions #####################################

if __name__ == '__main__':
    main()