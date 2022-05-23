from logging import PlaceHolder
import discord
from discord.ext import commands
import akinator
import os
import asyncio
import requests
import json


def get_prefix(client, message):
  url = f"https://db-api.r4nd0md3v.repl.co/get/prefix/{message.guild.id}"
  r = requests.get(url=url)
  response = r.json()
  if response["success"] == True:
    return response["prefix"]

intents = discord.Intents.all()
client = commands.Bot(command_prefix=commands.when_mentioned_or(get_prefix), intents=intents, case_insensitive=True, strip_after_prefix=True)

aki = akinator.Akinator()

@client.event
async def on_ready():
  print(f'Logged in as {client.user} (ID: {client.user.id})')
  print('------')


@client.command()
async def changeprefix(ctx, *, prefix=None):
  if prefix == None:
    prefix = ""
  elif prefix.lower() == "reset":
    url = f"https://db-api.r4nd0md3v.repl.co/reset/prefix/{ctx.guild.id}"
    r = requests.get(url=url)
    response = r.json()
    if response["success"] == True:
      await ctx.message.reply("Successfully reset the prefix!")

  if prefix.lower() != "reset":
    url = f"https://db-api.r4nd0md3v.repl.co/add/prefix/{ctx.guild.id}/{prefix}"
    r = requests.get(url=url)
    response = r.json()
    if response["success"] == True:
      await ctx.message.reply(f"Changed prefix to `{prefix}` successfully!")


@client.command()
async def start(ctx, language="en", child_mode:bool = True):
  premessage = ctx.message
  playagain = True

  def check(m):
    return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

  while playagain == True:
    async with ctx.typing():
      await asyncio.sleep(0)
    try:
      q = aki.start_game(language,child_mode)
    except akinator.InvalidLanguageError:
      await ctx.message.reply("Sorry I dont know how to speak that language! :sob:")

    while aki.progression <= 90:
      async with ctx.typing():
        await asyncio.sleep(0)
      em=discord.Embed(title=f"Question {aki.step + 1}", description=f"**{q}**\n[yes (**y**) / no (**n**) / idk (**i**) / probably (**p**) / probably not (**pn**)]\n[back (**b**) / stop (**s**)]", color=discord.Color.from_rgb(255,245,0))
      await premessage.reply(embed=em)
  
      try:
        message = message = await client.wait_for("message", check=check, timeout=120)
        premessage = message
        a = message.content
      except asyncio.exceptions.CancelledError:
        await premessage.reply("Oof you took too long to respond. :alarm_clock:")
  
      if a.lower() == "back" or a.lower() == "b":
        try:
          q = aki.back()
        except akinator.CantGoBackAnyFurther:
          await premessage.reply("Go back to where? This is your first question. :face_with_monocle:")
          pass
      elif a.lower() == "stop" or a.lower() == "s":
        await premessage.reply("Stoped the game!")
        aki.close()
        pass
      else:
        try:
          q = aki.answer(a)
        except  akinator.InvalidAnswerError:
          await premessage.reply("Hmm are you sure this is a valid answers? :thinking:")
          pass

    await premessage.reply("🤔")
  
    async with ctx.typing():
      await asyncio.sleep(0)
    aki.win()
  
    em = discord.Embed(title=aki.first_guess["name"], description=aki.first_guess["description"] + "\nRanked: **#" + aki.first_guess["ranking"] + "**\n\n[yes (**y**) / no (**b**)]\n[back (**b**)]", color=discord.Color.from_rgb(255,245,0))
    em.set_image(url=aki.first_guess["absolute_picture_path"])
    em.set_author(name="Is this your charecter?")
    await premessage.reply(embed=em)
  
    correct = message = await client.wait_for("message", check=check)
    premessage = correct
    a = correct.content
  
    async with ctx.typing():
      await asyncio.sleep(0)

    if a.lower() == "yes" or a.lower() == "y":
      em = discord.Embed(title="Yay, Got another one right!", description="Want to play one more time? :upside_down:\n\n[yes (**y**) / no (**n**)", color=discord.Color.from_rgb(255,245,0))
      await premessage.reply(embed=em)
      another = message = await client.wait_for("message", check=check)
      a = another.content
      premessage = another
      if a.lower() == "y" or a.lower() == "yes":
        playagain = True
      else:
        playagain = False
        await premessage.reply("Ok =(")
    else:
      em = discord.Embed(title="Oof, Got one wrong... :disappointed:", description="Want me to try one more time? :upside_down:\n\n[yes (**y**) / no (**n**)", color=discord.Color.from_rgb(255,245,0))
      await premessage.reply(embed=em)
      another = message = await client.wait_for("message", check=check)
      a = another.content
      premessage = another
      if a.lower == "y" or a.lower() == "yes":
        playagain = True
      else:
        playagain = False
        await premessage.reply("Ok =(")



TOKEN=os.getenv("BOT_TOKEN")
client.run(TOKEN)