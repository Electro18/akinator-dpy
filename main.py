import discord
from discord.ext import commands
import akinator
import os
import json


intents = discord.Intents.all()
client = commands.Bot(command_prefix=commands.when_mentioned_or('?'), intents=intents)

aki = akinator.Akinator()

@client.event
async def on_ready():
  print(f'Logged in as {client.user} (ID: {client.user.id})')
  print('------')


@client.command()
async def start(ctx):
  with open("config/users.json", "r") as f:
    data = json.load(f)
  if ctx.author.id not in data:
    data[ctx.author.id] = {}
    data[ctx.author.id]["child"] = True
    data[ctx.author.id]["lang"] = "en"
    with open("config/users.json", "w") as f:
      json.dump(data, f)
  
  child = data[ctx.author.id]["child"]
  lang = data[ctx.author.id]["lang"]

  def check(m):
    return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

  q = aki.start_game()

  while aki.progression <= 80:
    await ctx.send(q)
    message = await client.wait_for("message", check=check)
    a = message.content

    if a.lower() == "b" or a.lower() == "back":
      try:
        q = aki.back()
      except akinator.CantGoBackAnyFurther:
        await ctx.send("Cannot go back!")
        pass
    else:
      q = aki.answer(a)

  aki.win()

  await ctx.send(f"It's {aki.first_guess['name']} ({aki.first_guess['description']})! Was I correct?\n{aki.first_guess['absolute_picture_path']}\n\t")

  correct = message = await client.wait_for("message", check=check)
  a = message.content

  if a.lower() == "yes" or a.lower() == "y":
    print("Yay\n")
  else:
    print("Oof\n")


TOKEN=os.getenv("BOT_TOKEN")
client.run(TOKEN)