import os, discord, sqlite3, time, asyncio, random
from discord.ext import commands
from dotenv import load_dotenv
import timers, costs, helpers

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Global time variables
prev_time = None
total_time = 0

# Connect to the database
conn = sqlite3.connect('game.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS cities(
            discord_id TEXT PRIMARY KEY,
            wood INTEGER,
            stone INTEGER,
            food INTEGER,
            lumber_mills INTEGER,
            quarries INTEGER,
            farms INTEGER)""")

bot = discord.Bot()

# ----- Buttons ----- #
# Wood Button
### TODO: Implement button clearing on timeout ###
class WoodView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=30)
        self.ctx = ctx
        
    @discord.ui.button(label="Wood", style=discord.ButtonStyle.primary, emoji='🪓')
    async def button_callback(self, button, interaction):
        embed = helpers.success_embed_creator(self.ctx, "Collect Wood", "Press the button to gather wood!")
        weighted_list = [1] * 7 + [2] * 2 + [3] * 1
        amount = random.choice(weighted_list)
        c.execute("UPDATE cities SET wood = wood + ? where discord_id = ?", (amount, self.ctx.author.id))
        conn.commit()
        c.execute("SELECT wood FROM cities WHERE discord_id = ?", (self.ctx.author.id,))
        wood = c.fetchone()[0]
        embed.add_field(name = "Wood Collected!", value=f"You collected {amount} wood! You have {wood} wood!")
        await interaction.response.edit_message(embed=embed)
        
# Confirms the bot is online
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Sample command
@bot.slash_command()
async def hello(ctx, name: str = None):
    name = name or ctx.author.name
    discord_id = ctx.author.id
    await ctx.respond(f"Hello {name}!  Your ID is {discord_id}")

# ------ Game Start ------ #
# /start command
# Starts a game for the user if they have not started it before, returns an error if they have
@bot.slash_command(description = "Start a game!")
async def start(ctx):
    discord_id = ctx.author.id
    # Check if user exists
    c.execute("SELECT * FROM cities WHERE discord_id = ? ", (discord_id,))
    user_exists = c.fetchone() is not None
    if user_exists:
        embed = helpers.fail_embed_creator(ctx, "Error", "You already have a city!")
        await ctx.respond(embed=embed)
    else:
        c.execute("INSERT INTO cities (discord_id, wood, stone, food, lumber_mills, quarries, farms) VALUES (?, ?, ?, ?, ?, ?, ?)", (
            discord_id, 0, 0, 0, 0, 0, 0))
        conn.commit()
        embed = helpers.success_embed_creator(ctx, "Game Started", "Welcome to your city! Do /wood to start generating some wood!")
        await ctx.respond(embed=embed)

# /wood command
# Creates a button the player can press to generate 1 wood
@bot.slash_command(description = "Click the button to get some wood")
async def wood(ctx):
    discord_id = ctx.author.id
    # Check if user exists
    c.execute("SELECT * FROM cities WHERE discord_id = ? ", (discord_id,))
    user_exists = c.fetchone() is not None
    if user_exists:
        embed = helpers.success_embed_creator(ctx, "Collect Wood", "Press the button to gather wood!")
        await ctx.respond(embed=embed, view=WoodView(ctx=ctx))
    else:
        embed = helpers.fail_embed_creator(ctx, "Error", "You do not have a city! Use /start to create one!")
        await ctx.respond(embed=embed)

# ----- Game Loop ----- #
async def game_loop():
    global prev_time, total_time
    await bot.wait_until_ready()
    while not bot.is_closed():
        current_time = time.time() * 1000
        if prev_time is None:
            prev_time = current_time
        delta_time = current_time - prev_time
        total_time += delta_time
        prev_time = current_time
        await update_game(delta_time, total_time)
        await asyncio.sleep(2)
async def update_game(delta_time, total_time):
    pass
    
if __name__ == "__main__":
    bot.loop.create_task(game_loop())
    bot.run(TOKEN)