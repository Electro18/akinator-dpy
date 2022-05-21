from logging import PlaceHolder
import discord
from discord.ext import commands
import akinator
import os
import asyncio


intents = discord.Intents.all()
client = commands.Bot(command_prefix=commands.when_mentioned_or('?'), intents=intents)

aki = akinator.Akinator()

@client.event
async def on_ready():
  print(f'Logged in as {client.user} (ID: {client.user.id})')
  print('------')


@client.command()
async def start(ctx, language="en", child_mode=True):
  async with ctx.typing():
    await asyncio.sleep(0)

  def check(m):
    return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

  q = aki.start_game(language,child_mode)
  premessage = ctx.message
  playagain = True

  while playagain == True:
    while aki.progression <= 85:
      async with ctx.typing():
        await asyncio.sleep(0)
      em=discord.Embed(title=f"Question {aki.step + 1}", description=f"**{q}**\n[yes (**y**) / no (**n**) / idk (**i**) / probably (**p**) / probably not (**pn**)]\n[back (**b**) / stop (**s**)]", color=discord.Color.from_rgb(255,245,0))
      await premessage.reply(embed=em)
  
      message = message = await client.wait_for("message", check=check, timeout=5)
      premessage = message
      a = message.content
  
      if a.lower() == "back" or a.lower() == "b":
        try:
          q = aki.back()
        except akinator.CantGoBackAnyFurther:
          await ctx.send("Go back to where? This is your first question. :face_with_monocle:")
          pass
      elif a.lower() == "stop" or a.lower() == "s":
        aki.close()
        await ctx.message.reply("Stoped the game!")
        pass
      else:
        q = aki.answer(a)
  
    async with ctx.typing():
      await asyncio.sleep(0)
    aki.win()
  
    em = discord.Embed(title=aki.first_guess["name"], description=aki.first_guess["description"] + "\nRanked: **#" + aki.first_guess["ranking"] + "**\n\n[yes (**y**) / no (**b**)]\n[back (**b**)]", color=discord.Color.from_rgb(255,245,0))
    em.set_image(url=aki.first_guess["absolute_picture_path"])
    em.set_author(text="Is this your charecter?")
    await ctx.send(embed=em)
  
    correct = message = await client.wait_for("message", check=check)
    premessage = correct
    a = correct.content
  
    async with ctx.typing():
      await asyncio.sleep(0)

    if a.lower() == "yes" or a.lower() == "y":
      em = discord.Embed(title="Yay, Got another one right!", description="Want to one more time? :upside_down:\n\n[yes (**y**) / no (**n**)", color=discord.Color.from_rgb(255,245,0))
      await premessage.reply(embed=em)
      another = message = await client.wait_for("message", check=check)
      a = another.content
      premessage = another
      if a.lower == "y" or a.lower() == "yes":
        playagain = True
      else:
        playagain = False
        await another.reply("Ok =(")
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
        await another.reply("Ok =(")



TOKEN=os.getenv("BOT_TOKEN")
client.run(TOKEN)