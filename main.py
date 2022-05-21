from logging import PlaceHolder
import discord
from discord.ext import commands
import akinator
import os


intents = discord.Intents.all()
client = commands.Bot(command_prefix=commands.when_mentioned_or('?'), intents=intents)

aki = akinator.Akinator()

@client.event
async def on_ready():
  print(f'Logged in as {client.user} (ID: {client.user.id})')
  print('------')


@client.command()
async def start(ctx, language="en", child_mode=True):

  def check(m):
    return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

  q = aki.start_game(language,child_mode)

  while aki.progression <= 85:
    em=discord.Embed(title=f"Question {aki.step + 1}", description=f"**{q}**\n[yes (**y**) / no (**n**) / idk (**i**) / probably (**p**) / probably not (**pn**)]\n[back (**b**) / stop (**s**)]", color=discord.Color.from_rgb(255,245,0))
    em.set_footer(text="Respond in 120 seconds!", icon_url=client.user.avatar_url)
    await ctx.message.reply(embed=em)

    message = message = await client.wait_for("message", check=check, timeout=120)
    a = message.content

    if a.lower() == "back" or a.lower() == "b":
      try:
        q = aki.back()
      except akinator.CantGoBackAnyFurther:
        await ctx.send("Cannot go back!")
        pass
    elif a.lower() == "stop" or a.lower() == "s":
      await ctx.message.reply("Currently making this feautre so.... Sorry?")
      pass
    else:
      q = aki.answer(a)
        

  aki.win()

  em = discord.Embed(title=aki.first_guess["name"], description=f"Description: " + aki.first_guess["description"] + "\n\nRanking: " + aki.first_guess["ranking"], color = discord.Color.random())
  em.set_footer(text="Am I correct? Respond with yes or no.", icon_url=client.user.avatar_url)
  em.set_image(url=aki.first_guess["absolute_picture_path"])
  await ctx.send(embed=em)

  correct = message = await client.wait_for("message", check=check)
  a = correct.content

  if a.lower() == "yes" or a.lower() == "y":
    await ctx.send("Yay\n")
  else:
    await ctx.send("Oof\n")



TOKEN=os.getenv("BOT_TOKEN")
client.run(TOKEN)