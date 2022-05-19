import discord
from discord.ext import commands
import akinator
import os


intents = discord.Intents.all()
client = commands.Bot(command_prefix=commands.when_mentioned_or('?'), intents=intents)

@client.event
async def on_ready():
  print(f'Logged in as {client.user} (ID: {client.user.id})')
  print('------')


TOKEN=os.getenv("BOT_TOKEN")
client.run(TOKEN)