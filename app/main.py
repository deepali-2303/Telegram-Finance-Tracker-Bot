from telegram.ext import Application, CommandHandler, MessageHandler, filters

from config import settings
from shared.utils.logging import get_logger, setup_logging

setup_logging()
logger = get_logger(__name__)

BOT_TOKEN = settings.BOT_TOKEN


async def start(update, context):
    logger.info("Bot started")
    await update.message.reply_text("Bot connected 🚀")


async def echo(update, context):
    logger.info(f"Received message: {update.message.text}")
    user_text = update.message.text
    await update.message.reply_text(f"You said: {user_text}")


def main():

    app = Application.builder().token(BOT_TOKEN).build()
    logger.info("Application built")
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, echo))
    logger.info("Handlers registered")
    app.run_polling()

    logger.info("Bot is running...")


if __name__ == "__main__":
    main()
