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

  while aki.progression <= 85:
    a = "b"
    em=discord.Embed(title=f"Question {aki.step + 1}", description=f"**{q}**\nPick on option.", color=discord.Color.from_rgb(255,245,0))
    class options(discord.ui.View):
      @discord.ui.button(label="Yes", style=discord.ButtonStyle.green, row=1)
      async def button_callback1(self, button, interaction):
        a = "y"
        for child in self.children:
          child.disabled = True
        await interaction.response.edit_message(view=self)
      @discord.ui.button(label="No", style=discord.ButtonStyle.green, row=1)
      async def button_callback2(self, button, interaction):
        a = "n"
        for child in self.children:
          child.disabled = True
        await interaction.response.edit_message(view=self)
      @discord.ui.button(label="I dont know", style=discord.ButtonStyle.green, row=1)
      async def button_callback3(self, button, interaction):
        a = "idk"
        for child in self.children:
          child.disabled = True
        await interaction.response.edit_message(view=self)
      @discord.ui.button(label="Probably", style=discord.ButtonStyle.green, row=2)
      async def button_callback4(self, button, interaction):
        a = "p"
        for child in self.children:
          child.disabled = True
        await interaction.response.edit_message(view=self)
      @discord.ui.button(label="Probably Not", style=discord.ButtonStyle.green, row=2)
      async def button_callback5(self, button, interaction):
        a = "pn"
        for child in self.children:
          child.disabled = True
        await interaction.response.edit_message(view=self)
      @discord.ui.button(label="Back", style=discord.ButtonStyle.grey, row=3)
      async def button_callback5(self, button, interaction):
        a = "b"
        for child in self.children:
          child.disabled = True
        await interaction.response.edit_message(view=self)
      @discord.ui.button(label="END GAME", style=discord.ButtonStyle.red, row=3)
      async def button_callback(self, button, interaction):
        a = "dkmmdmdfkm"
        for child in self.children:
          child.disabled = True
        await interaction.response.edit_message(view=self)
    await ctx.send(embed=em, view=options())

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