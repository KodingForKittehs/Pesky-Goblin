import asyncio
import logging
import random
from discord.ext import commands

logging.basicConfig(level=logging.INFO)

class PeskyGoblinBot(commands.Bot):

    idle_messages = [
        '_rummages through a small bag._',
        '_sniffs curiously at a pile of dirt._'
    ]

    def __init__(self, db, **kwargs):
        super().__init__(kwargs)
        self.db = db

    def get_channel(self, name):
        logging.info(f'get_channel: lookup {name}')
        for channel in self.get_all_channels():
            logging.info(f'get_channel: {channel.name}')

        return next(
            (x for x in self.get_all_channels() if x.name == name),
            None
        )

    async def do_idle_action(self):
        rando = random.randrange(len(self.idle_messages))
        message = self.idle_messages[rando]
        await self.current_channel.send(message)

    async def do_heartbeats(self):
        while True:
            await self.do_idle_action()

            logging.info('sleeping')
            await asyncio.sleep(100)

    async def on_ready(self):
        logging.info(f'Logged in as {self.user}')

        if 'channel' not in self.db:
            self.db['channel'] = 'general'
        self.current_channel = self.get_channel(self.db['channel'])
        logging.info(f"init channel {self.db['channel']}")

        self.loop.create_task(self.do_heartbeats())

        #await self.general.send("Tee heee!!")

    async def on_message(self, message):
        print(f'on_message {message.author} {message.content}')

    async def create_channel(self, name):
        channel = self.get_channel(name)
        if channel:
            logging.info(f'Channel {name} exists already!')
            return channel
        logging.info(f'Creating a new channel {name}')
        return await self.guilds[0].create_text_channel(name)

    async def move(self, channel):
        self.current_channel = await self.create_channel(channel)
        self.db['channel'] = self.current_channel.name

    async def on_typing(self, channel, user, when):
        logging.info(f'on_typing {channel} {user} {when}')
        logging.info(f'guild {channel.guild}')

        if channel.name != self.db['channel']:
            return

        self.move('a-goblins-hovel')






