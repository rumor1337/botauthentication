import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random
import json

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

data_path = 'validation/data.json'
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='%', intents=intents)

adminRole = "perc30"

@bot.event
async def on_ready():
    print(f"launched successfully")

@bot.command()
async def auth(ctx):
    code = random.randint(10000, 99999)
    await ctx.author.send(f"Your code is: {code}; authenticate at: http://localhost/auth.php")
    
    user_obj = {
        "name": str(ctx.author),
        "user": ctx.author.id,
        "code": code,
        "authenticated": False
    }

    with open(data_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {"users": []}


    found = False
    for u in data["users"]:
        if u["user"] == ctx.author.id:
            u["code"] = code
            u["authenticated"] = False
            found = True
            break

    if found:
        print(f"updated user {ctx.author.id} with new code {code}")
    else:
        data["users"].append(user_obj)

    with open(data_path, 'w') as f:
        json.dump(data, f, indent=2)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)