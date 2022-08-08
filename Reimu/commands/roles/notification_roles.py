import discord
from discord.ext import commands
import discord.ui


class NotificationButtons(discord.ui.View):

    def __init__(self, bump, events, giveaways):
        self.bump = bump
        self.events = events
        self.giveaways = giveaways
        super().__init__(timeout=None)

    @discord.ui.button(emoji="<:n_ahegao:1003245563233456148>", custom_id="giveaway")
    async def b_callback(self, button, interaction):
        if self.giveaways in interaction.user.roles:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Вы отписались от уведомлений о раздачах",
                    description=f"С вас снята роль {self.giveaways.mention}"
                ), ephemeral=True
            )
            await interaction.user.remove_roles(self.giveaways)
        else:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Вы подписались на уведомления о раздачах",
                    description=f"Вам добавлена роль {self.giveaways.mention}"
                ), ephemeral=True
            )
            await interaction.user.add_roles(self.giveaways)

    @discord.ui.button(emoji="<:n_chibi:1003245575300452353>", custom_id="event")
    async def a_callback(self, button, interaction):
        if self.events in interaction.user.roles:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Вы отписались от уведомлений о игровых ивентах",
                    description=f"С вас снята роль {self.events.mention}"
                ), ephemeral=True
            )
            await interaction.user.remove_roles(self.events)
        else:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Вы подписались на уведомления о игровых ивентах",
                    description=f"Вам добавлена роль {self.events.mention}"
                ), ephemeral=True
            )
            await interaction.user.add_roles(self.events)

    @discord.ui.button(emoji="<a:z_gawrgurasin:1003206285421985902>", custom_id="bumps")
    async def e_callback(self, button, interaction):
        if self.bump in interaction.user.roles:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Вы отписались от уведомлений о бампах",
                    description=f"С вас снята роль {self.bump.mention}"
                ), ephemeral=True
            )
            await interaction.user.remove_roles(self.bump)
        else:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Вы подписались на уведомления о бампах",
                    description=f"Вам добавлена роль {self.bump.mention}"
                ), ephemeral=True
            )
            await interaction.user.add_roles(self.bump)


class Notification_roles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Commands {} is loaded'.format(self.__class__.__name__))

    @commands.command()
    @commands.has_any_role(977141423931523092)
    async def notification_roles(self, ctx):
        bump = discord.utils.get(ctx.guild.roles, id=1003214722990080020)
        events = discord.utils.get(ctx.guild.roles, id=1003222259483279462)
        giveaways = discord.utils.get(ctx.guild.roles, id=1003222251581227098)
        embed = discord.Embed(
            title="Роли напоминаний",
            description=f"Нажмите на кнопку что бы получить роли и получать уведомления"
        ).add_field(
            name="Роли",
            value=f"Уведомления о раздачах - <:n_ahegao:1003245563233456148> {giveaways.mention}\nУведомления о игровых ивентах - <:n_chibi:1003245575300452353> {events.mention}\nУведомления о бампе сервера - <a:z_gawrgurasin:1003206285421985902> {bump.mention}"
        )
        await ctx.send(embed=embed, view=NotificationButtons(bump, events, giveaways))

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(795606016728760320)
        bump = discord.utils.get(guild.roles, id=1003214722990080020)
        events = discord.utils.get(guild.roles, id=1003222259483279462)
        giveaways = discord.utils.get(guild.roles, id=1003222251581227098)
        self.bot.add_view(NotificationButtons(bump, events, giveaways))


def setup(client):
    client.add_cog(Notification_roles(client))
