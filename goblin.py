import logging
import asyncio
from discord.ext import commands

logging.basicConfig(level=logging.INFO)

class PeskyGoblinBot(commands.Bot):

    def __init__(self, db, **kwargs):
        super().__init__(kwargs)
        self.db = db
        if 'channel' not in self.db:
            self.db['channel'] = 'general'
        logging.info(f"init channel {self.db['channel']}")

    def get_channel(self, name):
        return next(
            (x for x in self.get_all_channels() if x.name == name),
            None
        )

    async def do_events(self):
        while True:
            logging.info('sleeping')
            await asyncio.sleep(10)

    async def on_ready(self):
        logging.info(f'Logged in as {self.user}')
        self.loop.create_task(self.do_events())

        #await self.general.send("Tee heee!!")

    async def on_message(self, message):
        print(f'on_message {message}')

    async def create_channel(self, name):
        channel = self.get_channel(name)
        if channel:
            logging.info(f'Channel {name} exists already!')
            return channel
        logging.info(f'Creating a new channel {name}')
        return await self.guilds[0].create_text_channel(name)

    async def on_typing(self, channel, user, when):
        logging.info(f'on_typing {channel} {user} {when}')
        logging.info(f'guild {channel.guild}')

        if channel.name != self.db['channel']:
            return

        new_channel = await self.create_channel("a-goblins-hovel")
        self.db['channel'] = new_channel.name






