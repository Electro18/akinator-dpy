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


def create_setting_u(ctx):
  with open("config/users.json", "r") as f:
    data = json.load(f)

  data[str(ctx.author.id)] = {}
  data[str(ctx.author.id)]["child"] = True
  data[str(ctx.author.id)]["lang"] = "en"

  with open("config/users.json", "w") as f:
    json.dump(data, f)

@client.command()
async def start(ctx):
  with open("config/users.json", "r") as f:
    data = json.load(f)
  if str(ctx.author.id) not in data:
    create_setting_u(ctx=ctx)
  with open("config/users.json", "r") as f:
    data = json.load(f)
  
  child = data[str(ctx.author.id)]["child"]
  lang = data[str(ctx.author.id)]["lang"]

  def check(m):
    return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

  q = aki.start_game(language=lang, child_mode=child)
  await ctx.send(lang + "i")

  while aki.progression <= 80:
    em=discord.Embed(title=q, description=f"Progress: {aki.progression}\n\nStep: {aki.step}", color=discord.Color.random())
    await ctx.send(embed=em)
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
    await ctx.send("Yay\n")
  else:
    await ctx.send("Oof\n")



@client.command()
async def language(ctx, lang=None):
  if lang == None:
    await ctx.send("Please state 1 of the following languages: `en`,`ar`,`cn`,`de`,`es`,`fr`,`il`,`it`,`jp`,`kr`,`pl`,`nl`,`pt`,`ru`,`tr`,`id`.")
  else:

    with open("config/users.json", "r") as f:
      data = json.load(f)
    if str(ctx.author.id) not in data:
      create_setting_u(ctx=ctx)
  
    with open("config/users.json", "r") as f:
      data = json.load(f)
  
    data[str(ctx.author.id)]["lang"] = lang
  
    with open("config/users.json", "w") as f:
      json.dump(data, f)
      
    await ctx.send(f"Set lang to {lang}!")


TOKEN=os.getenv("BOT_TOKEN")
client.run(TOKEN)