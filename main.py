import os
import discord
import sqlite3
from tables import *
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Connect to the database
conn = sqlite3.connect('game.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS cities
            (id TEXT PRIMARY KEY,
            user_id INTEGER,
            wood INTEGER,
            stone INTEGER,
            food INTEGER,
            lumber_mills INTEGER,
            quarries INTEGER,
            farms INTEGER)''')

bot = discord.Bot()

# Confirms the bot is online
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Sample command
@bot.slash_command()
async def hello(ctx, name: str = None):
    name = name or ctx.author.name
    await ctx.respond(f"Hello {name}!")

# ------ Game Start ------ #

@bot.slash_command()
async def create(ctx):
    id = ctx.author.id
    await ctx.respond(f"User id is {id}")


bot.run(TOKEN)