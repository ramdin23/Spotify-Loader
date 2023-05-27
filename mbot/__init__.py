import logging
from os import environ, mkdir, path, sys
#from dotenv import load_dotenv
from pyrogram import Client
import os
#load_dotenv("config.env")
# Log
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(message)s",
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()],
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)
# Mandatory Variable
try:
    API_ID = int(environ["API_ID"])
    API_HASH = environ["API_HASH"]
    BOT_TOKEN = environ["BOT_TOKEN"]
except KeyError:
    LOGGER.debug("One or More ENV variable not found.")
    sys.exit(1)
    
    
# Optional Variabl
MONGODB = os.environ['MONGODB']
OWNER_IDS = int(environ["OWNER_IDS"])
AUTH_CHATS = environ.get("AUTH_CHATS", "").split()

class Mbot(Client):
    def __init__(self):
        name = self.__class__.__name__.lower()
        super().__init__(
            ":memory:",
            plugins=dict(root=f"{name}/plugins"),
            workdir="./cache/",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            sleep_threshold=30,
        )
    async def start(self):
        global BOT_INFO
        await super().start()
        BOT_INFO = await self.get_me()
        if not path.exists("/tmp/thumbnails/"):
            mkdir("/tmp/thumbnails/")
        for chat in AUTH_CHATS:
            await self.send_photo(
                chat,
                "https://telegra.ph/file/5791b80b0c4349c85c604.jpg",
                "**Bot Was Started.** 🎵",
            )
        LOGGER.info(f"Bot Started As {BOT_INFO.username}\n")
    async def stop(self, *args):
        await super().stop()
        LOGGER.info("Bot Stopped, Bye.")
