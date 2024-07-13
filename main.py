from telethon import TelegramClient, events
from config import Config
import logging, asyncio

STARTUP_RETRIES = 3
RETRY_DELAY = 5  # in seconds, can be changed to 0 for testing
START_TIMEOUT = 30

logging.basicConfig(
    level=logging.INFO,  # Use DEBUG level to get more detailed logs
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)
bot_client = TelegramClient("msg-fwd-bot", int(Config.API_ID), Config.APP_API_HASH)
user_client = TelegramClient("msg-fwd-user", int(Config.API_ID), Config.APP_API_HASH)

"""
This is the event handler for when a message is received
"""


@user_client.on(
    events.NewMessage(
        incoming=True,
        from_users=Config.USER_TO_LISTEN_TO,
    )
)
async def handler(event: events.NewMessage.Event):
    logger.info(f"Received message: {event.raw_text}")
    await bot_client.send_message(Config.USER_TO_FORWARD_TO, event.raw_text)
    logger.info(f"Forwarded message: {event.raw_text}")


async def start_bot_client():
    for attempt in range(STARTUP_RETRIES):
        try:
            await asyncio.wait_for(
                bot_client.start(bot_token=Config.TELEGRAM_BOT_TOKEN), START_TIMEOUT
            )
            logger.info("Bot client started")
            await bot_client.send_message(
                Config.USER_TO_FORWARD_TO, "Bot Client Started 🤖🚀"
            )
            return
        except asyncio.TimeoutError:
            logger.error(
                f"Bot client start timed out on attempt {attempt + 1}/{STARTUP_RETRIES}"
            )
        except Exception as e:
            logger.error(
                f"Failed to start bot client on attempt {attempt + 1}/{STARTUP_RETRIES}: {e}"
            )
        await asyncio.sleep(RETRY_DELAY)

    raise RuntimeError("Failed to start bot client after multiple attempts")


async def start_user_client():
    for attempt in range(STARTUP_RETRIES):
        try:
            await asyncio.wait_for(
                user_client.start(phone=Config.CLIENT_PHONE_NUMBER), START_TIMEOUT
            )
            await bot_client.send_message(
                Config.USER_TO_FORWARD_TO, "User Client Started 🤸🚀"
            )
            logger.info("User client started")
            return
        except Exception as e:
            logger.error(
                f"Failed to start user client on attempt {attempt + 1}/{STARTUP_RETRIES}: {e}"
            )
            await bot_client.send_message(
                Config.USER_TO_FORWARD_TO,
                f"Failed to start user client on attempt {attempt + 1}/{STARTUP_RETRIES}: \n {e}",
            )
        await asyncio.sleep(RETRY_DELAY)

    await bot_client.send_message(
        Config.USER_TO_FORWARD_TO,
        "❌ Failed to start user client after multiple attempts ❌",
    )
    raise RuntimeError("Failed to start user client after multiple attempts")


async def main():
    await start_bot_client()
    await start_user_client()

    logger.info("Listening for messages...")

    await asyncio.gather(
        user_client.run_until_disconnected(), bot_client.run_until_disconnected()
    )


if __name__ == "__main__":
    try:

        asyncio.get_event_loop().run_until_complete(main())
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        logger.error(
            "Bot shutting down due to errors. Please check the logs for more details."
        )
        exit(1)
