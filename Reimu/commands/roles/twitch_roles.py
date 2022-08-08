import discord
from discord.ext import commands
import discord.ui


class TwitchButton(discord.ui.View):

    def __init__(self, bot, ttv):
        self.bot = bot
        self.ttv = ttv
        super().__init__(timeout=None)

    @discord.ui.button(emoji="<:lastPage:1002271989366538302>", custom_id="a", disabled=True)
    async def b_callback(self, button, interaction):
        pass

    @discord.ui.button(emoji="<a:Twitch:1002964617653399582>", custom_id="twitch")
    async def a_callback(self, button, interaction):
        if self.ttv in interaction.user.roles:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Вы отписались от уведомлений о стримах",
                    description=f"С вас снята роль {self.ttv.mention}"
                ), ephemeral=True
            )
            await interaction.user.remove_roles(self.ttv)
        else:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Вы подписались на уведомления о стримах",
                    description=f"Вам добавлена роль {self.ttv.mention}"
                ), ephemeral=True
            )
            await interaction.user.add_roles(self.ttv)

    @discord.ui.button(emoji="<:firstPage:1002272225023512736>", custom_id="d", disabled=True)
    async def e_callback(self, button, interaction):
        pass


class Twitch_roles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Commands {} is loaded'.format(self.__class__.__name__))

    @commands.command()
    @commands.has_any_role(977141423931523092)
    async def twitch_roles(self, ctx):
        await ctx.message.delete()
        ttv = discord.utils.get(ctx.guild.roles, id=881475727168503818)
        await ctx.send(
            embed=discord.Embed(
                title="Уведомление о стримах",
                description=f"Нажмите на кнопку что бы получить роль {ttv.mention} и получать уведомления о стримах"
            ).add_field(
                name="Стримы",
                value="Вы будете получать уведомления о стримах таких людей как:\n`BTMC`\n`zxcursed`\n`shadowraze`\n`mrekk`\n`whitecat`\nЭто не полный список\n\nТак же будут уведомления о стримах создателя :3"
            ), view=TwitchButton(self.bot, ttv)
        )

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(795606016728760320)
        ttv = discord.utils.get(guild.roles, id=881475727168503818)
        self.bot.add_view(TwitchButton(self.bot, ttv))


def setup(client):
    client.add_cog(Twitch_roles(client))
