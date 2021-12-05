import os
import logging
from replit import db
import goblin

logging.basicConfig(level=logging.INFO)
bot = goblin.PeskyGoblinBot(db=db, command_prefix='!')

@bot.command()
async def test(ctx):
    logging.info(f'commandola')
    await ctx.send("test response")

@bot.command(name="reload", help="Reloads goblin module from most recent source")
async def reload(ctx):
    reload(goblin)
    print("Reloaded goblin")

if __name__ == "__main__":
    bot.run(os.getenv('TOKEN'))