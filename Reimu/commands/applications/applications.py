import discord
from discord.ext import commands
import sqlite3
from discord.ui import InputText, Modal

connection = sqlite3.connect("databases/database.db")
cursor = connection.cursor()


class ModerateModal(Modal):

    def __init__(self, bot, channel):
        self.bot = bot
        self.channel = channel
        super().__init__(title="Заявка на модератора")

        self.add_item(
            InputText(
                label="Ваше имя, возраст и часовой пояс",
                placeholder="Евгений, 18, +7 UTC",
                min_length=1,
                max_length=30,
                style=discord.InputTextStyle.singleline
            )
        )

        self.add_item(
            InputText(
                label="Был ли опыт на других серверах?",
                placeholder="Если да, то на каких?",
                min_length=1,
                max_length=100,
                style=discord.InputTextStyle.long
            )
        )

        self.add_item(
            InputText(
                label="Почему именно ты?",
                placeholder="Потому что я...",
                min_length=1,
                max_length=400,
                style=discord.InputTextStyle.long
            )
        )

        self.add_item(
            InputText(
                label="Сколько времени ты готов уделять серверу?",
                placeholder="3 часа...",
                min_length=1,
                max_length=25,
                style=discord.InputTextStyle.singleline
            )
        )

    async def callback(self, interaction: discord.Interaction):
        await self.channel.send(
            embed=discord.Embed(
                title="Новая заявка на модератора!!!",
                description=f"`{interaction.user}` (`{interaction.user.id}`) подал(а) заявку на ведущего"
            ).add_field(
                name="Ваше имя, возраст и часовой пояс",
                value=f"{self.children[0].value}",
                inline=False
            ).add_field(
                name="Был ли опыт на других серверах?",
                value=f"{self.children[1].value}",
                inline=False
            ).add_field(
                name="Почему именно ты?",
                value=f"{self.children[2].value}",
                inline=False
            ).add_field(
                name="Сколько времени ты готов уделять серверу?",
                value=f"{self.children[3].value}",
                inline=False
            )
        )
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Заявка создана",
                description="Ваша заявка была сформирована и отправлена, администраторы скоро её рассмотрят"
            ), ephemeral=True
        )


class EventerModal(Modal):

    def __init__(self, bot, channel):
        self.bot = bot
        self.channel = channel
        super().__init__(title="Заявка на ведущего")

        self.add_item(
            InputText(
                label="Ваше имя, возраст и часовой пояс",
                placeholder="Евгений, 18, +7 UTC",
                min_length=1,
                max_length=30,
                style=discord.InputTextStyle.singleline
            )
        )

        self.add_item(
            InputText(
                label="Был ли опыт на других серверах?",
                placeholder="Если да, то на каких?",
                min_length=1,
                max_length=100,
                style=discord.InputTextStyle.long
            )
        )

        self.add_item(
            InputText(
                label="Какие ивенты вы умеете вести?",
                placeholder="Codenames, мафия...",
                min_length=1,
                max_length=150,
                style=discord.InputTextStyle.long
            )
        )

        self.add_item(
            InputText(
                label="Почему именно ты?",
                placeholder="Потому что я...",
                min_length=1,
                max_length=400,
                style=discord.InputTextStyle.long
            )
        )

        self.add_item(
            InputText(
                label="Сколько времени ты готов уделять серверу?",
                placeholder="3 часа...",
                min_length=1,
                max_length=25,
                style=discord.InputTextStyle.singleline
            )
        )

    async def callback(self, interaction: discord.Interaction):
        await self.channel.send(
            embed=discord.Embed(
                title="Новая заявка на ведущего!!!",
                description=f"`{interaction.user}` (`{interaction.user.id}`) подал(а) заявку на ведущего"
            ).add_field(
                name="Ваше имя, возраст и часовой пояс",
                value=f"{self.children[0].value}",
                inline=False
            ).add_field(
                name="Был ли опыт на других серверах?",
                value=f"{self.children[1].value}",
                inline=False
            ).add_field(
                name="Какие ивенты вы умеете вести?",
                value=f"{self.children[2].value}",
                inline=False
            ).add_field(
                name="Почему именно ты?",
                value=f"{self.children[3].value}",
                inline=False
            ).add_field(
                name="Сколько времени ты готов уделять серверу?",
                value=f"{self.children[4].value}",
                inline=False
            )
        )
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Заявка создана",
                description="Ваша заявка была сформирована и отправлена, администраторы скоро её рассмотрят"
            ), ephemeral=True
        )


class ButtonsAppil(discord.ui.View):

    def __init__(self, bot, channel):
        self.bot = bot
        self.channel = channel
        super().__init__(timeout=None)

    @discord.ui.button(label="Модератор", emoji="<:AiriLove:1003205141865967708>", custom_id="moder")
    async def a_callback(self, button, interaction):
        modal = ModerateModal(self.bot, self.channel)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="Ведущий", emoji="<:gawrguralove:1003206700125392986>", custom_id="eventer")
    async def b_callback(self, button, interaction):
        modal = EventerModal(self.bot, self.channel)
        await interaction.response.send_modal(modal)


class Req(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Commands {} is loaded'.format(self.__class__.__name__))

    @commands.command()
    @commands.has_any_role(977141423931523092)
    async def nabor(self, ctx):
        channel = self.bot.get_channel(1004424588417056849)
        await ctx.send(
            embed=discord.Embed(
                title="Рискнуть стать частью Staff'a",
                description="Просим при заполнении анкеты не изменять свой никнейм на время набора. Ваша личка должна быть открыта.\nПо причине того, что если Вы нас заинтересуете, то мы не сможем с Вами связаться.\nТакже анкеты, которые будут записаны в шуточной форме - сразу будут удалены."
            ), view=ButtonsAppil(self.bot, channel)
        )

    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(1004424588417056849)
        self.bot.add_view(ButtonsAppil(self.bot, channel))


def setup(client):
    client.add_cog(Req(client))
