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
async def start(ctx):

  def check(m):
    return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

  q = aki.start_game()

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

  em = discord.Embed(title=aki.first_guess["name"], description=f"Description: " + aki.first_guess["description"] + "\n\nRanking: " + aki.first_guess["ranking"], color = discord.Color.random())
  em.set_footer(text="Am I correct? Respond with yes or no.", icon_url=client.user.avatar_url)
  em.set_image(url=aki.first_guess["absolute_picture_path"])
  await ctx.send(embed=em)

  correct = message = await client.wait_for("message", check=check)
  a = message.content

  if a.lower() == "yes" or a.lower() == "y":
    await ctx.send("Yay\n")
  else:
    await ctx.send("Oof\n")



TOKEN=os.getenv("BOT_TOKEN")
client.run(TOKEN)