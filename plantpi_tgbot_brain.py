#!/usr/bin/env python
# pylint: disable=C0116,W0613

"""
Simple plant watering Bot to drive the pump with Telegram messages.

Usage:
/help to print a better help message.
/pump <pump_index> <duration/amount>
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from dotenv import dotenv_values
import logging
from functools import wraps
import inspect

from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext

from plantpi_waterer import Waterer

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

config = dotenv_values(".env")
print(f"Telegram bot token: '{config['TELEGRAM_BOT_TOKEN']}'")
LIST_OF_ADMINS = config['TELEGRAM_GROUP_ID'].split(',')
print(f"Telegram list of allowed users/groups: {LIST_OF_ADMINS}")


def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        id = None
        print(update.effective_chat)
        if 'group' in update.effective_chat.type:
            id = update.effective_chat.id
        else:
            id = update.effective_user.id
        if str(id) not in LIST_OF_ADMINS:
            print("Unauthorized access denied for {}.".format(id))
            return
        return func(update, context, *args, **kwargs)
    return wrapped


@restricted
def pump(update: Update, context: CallbackContext) -> None:
    """Run the selected watering pump for the desired duration or volume."""
    chat_id = update.message.chat_id
    try:
        pump_index = int(context.args[0])
        duration = context.args[1]

        if duration.isnumeric():
            duration = float(duration)

        print(
            f"Water the plants with pump {pump_index} for duration/amount: {duration}")

        with Waterer() as waterer:
            waterer.pump(pump_index, duration)

        update.message.reply_text(f"Plants have been watered!")

    except (IndexError, ValueError):
        update.message.reply_text(
            'Usage: /pump <pump_index> <duration/amount>')


@restricted
def help_command(update: Update, _) -> None:
    help_txt = inspect.cleandoc("""
    This Bot is a convenient telegram bot to control the watering system on our balcony\.

    Usage instructions:
    `/help` \- print this message\.
    `/pump <pump_index> <duration/amount>`
    Pump index is currently either `0` or `1`\.
    If the value given to `duration/amount` is a `float`/`integer`, it is interpreted as seconds the pump should be active\.
    If the value given to `duration/amount` contains '`ml`', '`dl`' or '`l`' in the end, it is interpreted as the amount that should be pumped through the pump\. Note, that the amount is divided per each nozzle output\.

    Contact @Pingviinituutti if you have problems :\)
    """)
    update.message.reply_text(help_txt, parse_mode=ParseMode.MARKDOWN_V2)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(config['TELEGRAM_BOT_TOKEN'])

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("pump", pump))

    # # on non command i.e message - echo the message on Telegram
    # dispatcher.add_handler(MessageHandler(
    #     Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling(poll_interval=5)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
