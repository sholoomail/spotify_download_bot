import logging
import os

from telegram import Update
from telegram.ext import (
    Updater, CommandHandler, CallbackContext
)

import command_hanlders

logger = logging.getLogger(__name__)


def setup_logging():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)


def start(update: Update, context: CallbackContext):
    update.effective_message.reply_text("Hello....!!\nThis is the @TM_SpotifyBot. This Bot was created by @TM_Adminz, the genius of the world.")
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Available Commands:\n/playlist\n/song\n/album\n\nSend Link Like This,\n/playlist [url]\n\nExample:\n/playlist https://open.spotify.com/playlist/37i9dQZF1DZ06evO2GbnbB?si=bTc1lwG2T9mv-XA_vP0Psg"
    )


def error(update: Update, context: CallbackContext, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    TOKEN = os.environ.get('TOKEN')
    APP_NAME = os.environ.get('APP_NAME')

    # Port is given by Heroku
    PORT = os.environ.get('PORT')

    # Set up the Updater

    updater = Updater(TOKEN, use_context=True, )
    dp = updater.dispatcher
    # Add handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_error_handler(error)

    dp.add_handler(CommandHandler(
        'playlist',
        command_hanlders.send_playlist_songs,
        pass_args=True,
        pass_job_queue=True,
        pass_chat_data=True)
    )
    dp.add_handler(CommandHandler(
        'song',
        command_hanlders.send_single_track,
        pass_args=True,
        pass_job_queue=True,
        pass_chat_data=True)
    )
    dp.add_handler(CommandHandler(
        'album',
        command_hanlders.send_album_songs,
        pass_args=True,
        pass_job_queue=True,
        pass_chat_data=True)
    )

    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.set_webhook(f"https://{APP_NAME}.herokuapp.com/{TOKEN}")
    updater.idle()


if __name__ == "__main__":
    main()
