import discord
from discord.ext import commands, tasks
import sqlite3
from discord.ui import View, Button, InputText, Modal
from config.settings import settings
from pyqiwip2p import QiwiP2P
import random
from datetime import *
from dateutil.relativedelta import relativedelta

db = sqlite3.connect("databases/database.db")
cur = db.cursor()
p2p = QiwiP2P(auth_key=settings["QIWItoken"])


async def create_p2p_bill(user, price, interaction, donate_type):
    try:
        comment = str(user) + "_" + str(random.randint(1000, 9999))

        bill = p2p.bill(amount=price, lifetime=15, comment=comment)

        cur.execute("INSERT INTO donate VALUES (?, ?, ?, ?)", [user, price, bill.bill_id, donate_type])
        db.commit()

        view = View()
        button = Button(label="Оплатить", emoji="<:gawrgurahug:1003206584928833536>", url=bill.pay_url,
                        style=discord.ButtonStyle.green)
        view.add_item(button)

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Оплата",
                description=f"Для оплаты нажмите на кнопку ниже"
            ), view=view, ephemeral=True
        )
    except Exception as e:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Ошибка!",
                description=f"Ошибочка получилась :c\n```py\n{e}```"
            ), ephemeral=True
        )


class SponsorModal(Modal):

    def __init__(self, bot, channel):
        self.bot = bot
        self.channel = channel
        super().__init__(title="Спонсорство", timeout=None)

        self.add_item(
            InputText(
                label="Длительность",
                placeholder=f"Кол - во месяцев",
                min_length=1,
                max_length=10,
                style=discord.InputTextStyle.singleline
            )
        )

    async def callback(self, interaction: discord.Interaction):
        price = 100 * int(self.children[0].value)
        await create_p2p_bill(interaction.user.id, price, interaction, "SPONSOR")


class CrystalModal(Modal):

    def __init__(self, bot, channel):
        self.bot = bot
        self.channel = channel
        super().__init__(title="Кристалы", timeout=None)

        self.add_item(
            InputText(
                label="Количество",
                placeholder=f"Вводите кол-во рублей | 1 руб - 200 кристалов",
                min_length=1,
                max_length=10,
                style=discord.InputTextStyle.singleline
            )
        )

    async def callback(self, interaction: discord.Interaction):
        price = int(self.children[0].value)
        await create_p2p_bill(interaction.user.id, price, interaction, "CRYSTAL")


class AnySummModal(Modal):

    def __init__(self, bot, channel):
        self.bot = bot
        self.channel = channel
        super().__init__(title="Любая сумма", timeout=None)

        self.add_item(
            InputText(
                label="Сумма",
                placeholder=f"Вводите сумму в рублях",
                min_length=1,
                max_length=10,
                style=discord.InputTextStyle.singleline
            )
        )

    async def callback(self, interaction: discord.Interaction):
        price = int(self.children[0].value)
        await create_p2p_bill(interaction.user.id, price, interaction, "ANY_SUMM")


class DonateButtons(discord.ui.View):

    def __init__(self, bot, channel):
        self.bot = bot
        self.channel = channel
        super().__init__(timeout=None)

    @discord.ui.button(label="Стать спонсором", style=discord.ButtonStyle.green,
                       emoji="<:gawrgurahug:1003206584928833536>", custom_id="sponsor")
    async def sponsor_callback(self, button, interaction):
        modal = SponsorModal(self.bot, self.channel)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="Купить кристалы", style=discord.ButtonStyle.green,
                       emoji="<:AiriLove:1003205141865967708>", custom_id="crystals")
    async def crystal_callback(self, button, interaction):
        modal = CrystalModal(self.bot, self.channel)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="Любая сумма", style=discord.ButtonStyle.green,
                       emoji="<:gawrguralove:1003206700125392986>", custom_id="any_summ")
    async def any_summ_callback(self, button, interaction):
        modal = AnySummModal(self.bot, self.channel)
        await interaction.response.send_modal(modal)


class Donate(commands.Cog):

    def __init__(self, bot):
        self.sponsor_role = None
        self.donate_channel = None
        self.bot = bot
        print('Commands {} is loaded'.format(self.__class__.__name__))

    @tasks.loop(seconds=10)
    async def donate_check(self):
        for bill in cur.execute("SELECT * FROM donate").fetchall():
            try:
                if str(p2p.check(bill_id=bill[2]).status) == "PAID":
                    if bill[3] == "SPONSOR":
                        await self.donate_channel.send(
                            content=f"Пользователь {self.bot.get_user(bill[0]).mention} оформил спонсорство на {str(bill[1])[:-2]} месяц(а/ев)")
                        add_time = bill[1] // 100
                        date_d = str(date.today() + relativedelta(months=+add_time))
                        cur.execute("INSERT INTO sponsor VALUES (?, ?)", [bill[0], date_d])
                        cur.execute("DELETE FROM donate WHERE bill_id = '{}'".format(bill[2]))
                        sponsor = self.bot.get_user(bill[0])
                        await sponsor.add_roles(self.sponsor_role)
                        db.commit()
                    elif bill[3] == "CRYSTAL":
                        await self.donate_channel.send(
                            content=f"Пользователь {self.bot.get_user(bill[0])} купил {bill[1] * 200} кристаллов <a:crystal:996045979084132382>")
                        cur.execute("UPDATE users SET hands = hands + {} WHERE id = {}".format(bill[1] * 200, bill[0]))
                        cur.execute("DELETE FROM donate WHERE bill_id = '{}'".format(bill[2]))
                        db.commit()
                    elif bill[3] == "ANY_SUMM":
                        await self.donate_channel.send(
                            content=f"Пользователь {self.bot.get_user(bill[0]).mention} поддержал сервер на сумму {bill[1]} рублей")
                elif str(p2p.check(bill_id=bill[2]).status) == "WAITING":
                    pass
                elif str(p2p.check(bill_id=bill[2]).status) == "EXPIRED":
                    cur.execute("DELETE FROM donate WHERE bill_id = '{}'".format(bill[2]))
                db.commit()
            except Exception as e:
                print(e)

    @tasks.loop(seconds=300)
    async def sponsor_check(self):
        try:
            for sponsor in cur.execute("SELECT * FROM sponsor").fetchall():
                sponsor_user = self.bot.get_user(sponsor[0])
                if str(date.today()) >= sponsor[1]:
                    await sponsor_user.remove_roles(self.sponsor_role)
                    cur.execute("DELETE FROM sponsor WHERE user_id = '{}'".format(sponsor[0]))
                else:
                    pass
        except Exception as e:
            print(e)

    @commands.command()
    async def f(self, ctx):
        channel = self.bot.get_channel(995963795623125052)
        await ctx.send(
            embed=discord.Embed(
                title="Донатик",
                description="> Приветствую, дорогой друг! Как ты уже понял, тут мы собираем денюжку для развития проекта. Если ты хочешь поддержать нас, помочь развитию сервера и получить плюшки, то ниже мы оставим реквизиты для поддержки."
            ).add_field(
                name="Бустер",
                value="> - Роль <@&797058853460115508>\n> - Доступ к новому чату\n> - Приватный голосовой чат в <#993104434575986698>",
                inline=False
            ).add_field(
                name="Спонсор - 100 руб/месяц",
                value="> - роль <@&1004725698830815232>\n> - Доступ к новому чату\n> - Приватный голосовой чат в <#993104434575986698>",
                inline=False
            ).add_field(
                name="Кристалы - 1 руб/200 кристаллов",
                value="> Купи столько, сколько тебе нужно",
                inline=False
            ).add_field(
                name=" ⁣ ",
                value="> - Для возможности покупки необходимо нажать на одну из кнопок ниже.\n> - Покупка происходит исключительно по кнопкам ниже.",
                inline=False
            ).add_field(
                name=" ⁣ ",
                value="> По всем вопросам обращайтесь в <#803681111628316683>  или к любому из <@&795606283339563018>"
            ).set_image(
                url="https://cdn.discordapp.com/attachments/977920877100412928/1005091991660531722/67db9bc74436da8f.png"
            ), view=DonateButtons(self.bot, channel)
        )

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(795606016728760320)
        print(guild)
        self.donate_channel = self.bot.get_channel(799161810485116929)
        self.sponsor_role = discord.utils.get(guild.roles, id=1004725698830815232)
        self.donate_check.start()
        self.sponsor_check.start()
        self.bot.add_view(DonateButtons(self.bot, self.donate_channel))


def setup(client):
    client.add_cog(Donate(client))
