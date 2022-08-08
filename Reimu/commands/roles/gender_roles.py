import discord
from discord.ext import commands
import discord.ui  

class GenderButtons(discord.ui.View):

    def __init__(self, trap, kun, tyan):
        self.trap = trap
        self.kun = kun
        self.tyan = tyan
        super().__init__(timeout = None)

    @discord.ui.button(emoji = "<:n_lot:1003212019907964969>", custom_id="trap")
    async def b_callback(self, button, interaction):
        if self.trap in interaction.user.roles:
            await interaction.response.send_message(
                embed = discord.Embed(
                    description = f"С вас снята роль {self.trap.mention}"
                ), ephemeral=True
            )
            await interaction.user.remove_roles(self.trap)
        else:
            await interaction.response.send_message(
                embed = discord.Embed(
                    description = f"Вам добавлена роль {self.trap.mention}"
                ), ephemeral=True 
            )
            await interaction.user.add_roles(self.trap)
        if self.kun in interaction.user.roles:
            await interaction.user.remove_roles(self.kun)
        else:
            pass
        if self.tyan in interaction.user.roles:
            await interaction.user.remove_roles(self.tyan)
        else:
            pass


    @discord.ui.button(emoji = "<:n_break:1003212039767982100>", custom_id="kun")
    async def a_callback(self, button, interaction):
        if self.kun in interaction.user.roles:
            await interaction.response.send_message(
                embed = discord.Embed(
                    description = f"С вас снята роль {self.kun.mention}"
                ), ephemeral=True
            )
            await interaction.user.remove_roles(self.kun)
        else:
            await interaction.response.send_message(
                embed = discord.Embed(
                    description = f"Вам добавлена роль {self.kun.mention}"
                ), ephemeral=True 
            )
            await interaction.user.add_roles(self.kun)
        if self.trap in interaction.user.roles:
            await interaction.user.remove_roles(self.trap)
        else:
            pass
        if self.tyan in interaction.user.roles:
            await interaction.user.remove_roles(self.tyan)
        else:
            pass

    @discord.ui.button(emoji = "<:n_frigh:1003211997845925998>", custom_id="tyan")
    async def e_callback(self, button, interaction):
        if self.tyan in interaction.user.roles:
            await interaction.response.send_message(
                embed = discord.Embed(
                    description = f"С вас снята роль {self.tyan.mention}"
                ), ephemeral=True
            )
            await interaction.user.remove_roles(self.tyan)
        else:
            await interaction.response.send_message(
                embed = discord.Embed(
                    description = f"Вам добавлена роль {self.tyan.mention}"
                ), ephemeral=True 
            )
            await interaction.user.add_roles(self.tyan)
        if self.trap in interaction.user.roles:
            await interaction.user.remove_roles(self.trap)
        else:
            pass
        if self.kun in interaction.user.roles:
            await interaction.user.remove_roles(self.kun)
        else:
            pass


class Gender_roles(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        print('Commands {} is loaded'.format(self.__class__.__name__))


    @commands.command()
    @commands.has_any_role(977141423931523092)
    async def gender_roles(self, ctx):
        await ctx.message.delete()
        trap = discord.utils.get(ctx.guild.roles, id = 812565100464439347)
        kun = discord.utils.get(ctx.guild.roles, id = 795727804284141588)
        tyan = discord.utils.get(ctx.guild.roles, id = 795727892574634024)
        await ctx.send(
            embed = discord.Embed(
                title = "Гендерные роли",
                description = f"Выберите роль вашего пола нажав на кнопку ниже"
            ).add_field(
                name = "Роли", 
                value = f"<:n_lot:1003212019907964969> - {trap.mention}\n<:n_break:1003212039767982100> - {kun.mention}\n<:n_frigh:1003211997845925998> - {tyan.mention}"
            ), view = GenderButtons(trap, kun, tyan)
        )
    
    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(795606016728760320)
        trap = discord.utils.get(guild.roles, id = 812565100464439347)
        kun = discord.utils.get(guild.roles, id = 795727804284141588)
        tyan = discord.utils.get(guild.roles, id = 795727892574634024)
        self.bot.add_view(GenderButtons(trap, kun, tyan))
    
    
def setup(client):
    client.add_cog(Gender_roles(client))

