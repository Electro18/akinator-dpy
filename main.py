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
async def start(ctx, language=None, child_mode=True):

  def check(m):
    return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

  q = aki.start_game(language,child_mode)

  continueG = True

  while aki.progression <= 85 and continueG == True:
    continueG = False
    em=discord.Embed(title=f"Question {aki.step + 1}", description=f"**{q}**\nPick on option.", color=discord.Color.from_rgb(255,245,0))
    class SelecAnswers(discord.ui.View):
      @discord.ui.select(
        placeholder = "Choose an Option!",
        min_values = 1,
        max_values = 1,
        options = [
          discord.SelectOption(
            label="Yes"
          ),
          discord.SelectOption(
            label="No"
          ),
          discord.SelectOption(
            label="I don't know"
          ),
          discord.SelectOption(
            label="Probably"
          ),
          discord.SelectOption(
            label="Probably Not"
          ),
          discord.SelectOption(
            label="Back"
          ),
          discord.SelectOption(
            label="End Game"
          ),
        ]
      )
      async def select_callback(self, select, interaction):
        if a.lower() == "back":
          try:
            q = aki.back()
          except akinator.CantGoBackAnyFurther:
            await ctx.send("Cannot go back!")
            pass
        else:
          q = aki.answer(a)
        continueG = True
        await interaction.delete_original_message()

    await ctx.send(embed=em, view=SelecAnswers())
        

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