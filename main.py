from telethon import TelegramClient, events
from config import Config
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot_client = TelegramClient("msg-fwd-bot", Config.API_ID, Config.APP_API_HASH)
user_client = TelegramClient("msg-fwd-user", Config.API_ID, Config.APP_API_HASH)

""""
This is the event handler for when a message is recieved
"""


@user_client.on(
    events.NewMessage(
        incoming=True,
        chats=Config.TARGET_CHAT_ID,
        from_users=Config.USER_TO_LISTEN_TO,
    )
)
async def handler(event: events.NewMessage.Event):

    logger.info(f"Received message: {event.raw_text}")
    await bot_client.send_message(Config.USER_TO_FORWARD_TO, event.raw_text)

    logger.info(f"Forwarded message: {event.raw_text}")


if __name__ == "__main__":
    try:
        bot_client.start(bot_token=Config.TELEGRAM_BOT_TOKEN)
        logger.info("Bot client started")

        user_client.start(Config.CLIENT_PHONE_NUMBER)
        logger.info("User client started")

        logger.info("Listening for messages...")

        user_client.run_until_disconnected()
        bot_client.run_until_disconnected()

    except Exception as e:
        # Add some sort of monitoring if this fails??
        logger.error(e)
