from telethon import TelegramClient, events
from config import Config
import logging


import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)
bot_client = TelegramClient("msg-fwd-bot", int(Config.API_ID), Config.APP_API_HASH)
user_client = TelegramClient("msg-fwd-user", int(Config.API_ID), Config.APP_API_HASH)

""""
This is the event handler for when a message is recieved
"""


# chats=Config.TARGET_CHAT_ID,
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


# NewMessage.Event(
#     original_update=UpdateNewChannelMessage(
#         message=Message(
#             id=34,
#             peer_id=PeerChannel(channel_id=2157558482),
#             date=datetime.datetime(
#                 2024, 7, 13, 2, 12, 58, tzinfo=datetime.timezone.utc
#             ),
#             message="this is a test!!!",
#             out=False,
#             mentioned=False,
#             media_unread=False,
#             silent=True,
#             post=False,
#             from_scheduled=False,
#             legacy=False,
#             edit_hide=False,
#             pinned=False,
#             noforwards=False,
#             invert_media=False,
#             offline=False,
#             from_id=PeerUser(user_id=795764923),
#             from_boosts_applied=None,
#             saved_peer_id=None,
#             fwd_from=None,
#             via_bot_id=None,
#             via_business_bot_id=None,
#             reply_to=None,
#             media=None,
#             reply_markup=None,
#             entities=[],
#             views=None,
#             forwards=None,
#             replies=MessageReplies(
#                 replies=0,
#                 replies_pts=41,
#                 comments=False,
#                 recent_repliers=[],
#                 channel_id=None,
#                 max_id=None,
#                 read_max_id=None,
#             ),
#             edit_date=None,
#             post_author=None,
#             grouped_id=None,
#             reactions=None,
#             restriction_reason=[],
#             ttl_period=None,
#             quick_reply_shortcut_id=None,
#             effect=None,
#             factcheck=None,
#         ),
#         pts=41,
#         pts_count=1,
#     ),
#     pattern_match=None,
#     message=Message(
#         id=34,
#         peer_id=PeerChannel(channel_id=2157558482),
#         date=datetime.datetime(2024, 7, 13, 2, 12, 58, tzinfo=datetime.timezone.utc),
#         message="this is a test!!!",
#         out=False,
#         mentioned=False,
#         media_unread=False,
#         silent=True,
#         post=False,
#         from_scheduled=False,
#         legacy=False,
#         edit_hide=False,
#         pinned=False,
#         noforwards=False,
#         invert_media=False,
#         offline=False,
#         from_id=PeerUser(user_id=795764923),
#         from_boosts_applied=None,
#         saved_peer_id=None,
#         fwd_from=None,
#         via_bot_id=None,
#         via_business_bot_id=None,
#         reply_to=None,
#         media=None,
#         reply_markup=None,
#         entities=[],
#         views=None,
#         forwards=None,
#         replies=MessageReplies(
#             replies=0,
#             replies_pts=41,
#             comments=False,
#             recent_repliers=[],
#             channel_id=None,
#             max_id=None,
#             read_max_id=None,
#         ),
#         edit_date=None,
#         post_author=None,
#         grouped_id=None,
#         reactions=None,
#         restriction_reason=[],
#         ttl_period=None,
#         quick_reply_shortcut_id=None,
#         effect=None,
#         factcheck=None,
#     ),
# )
