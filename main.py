import discord
import os

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_messagett(message):
    print(message)
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    await message.channel.send(f"{message.author.name} said '{message.content}'")

client.run(os.getenv('TOKEN'))