import discord
from discord.ext import commands
import json
from discord.ext.commands import MissingPermissions, Bot
from discord.ui import InputText, Modal, Button, View
import sqlite3
from datetime import date, time, timedelta, datetime
import asyncio

db = sqlite3.connect("databases/database.db") 
cur = db.cursor()


class LotModal(Modal):
    def __init__(self, bot, author, guild) -> None:
        self.bot = bot
        self.author = author
        self.guild = guild
        super().__init__(title="Создать лот")

        self.add_item(
            InputText(
                label="Название роли",
                placeholder = "Напишите название которое хотите присвоить роли",
                min_length = 3,
                max_length = 10,
                style=discord.InputTextStyle.singleline
            )
        )

        self.add_item(
            InputText(
                label="Цвет формата RGB",
                placeholder = "255 255 255",
                max_length = 11,
                style=discord.InputTextStyle.singleline
            )
        )

        self.add_item(
            InputText(
                label="Цена",
                placeholder = "Напишите цену роли | макс. цена 5000",
                max_length = 11,
                style=discord.InputTextStyle.singleline
            )
        )

    async def callback(self, interaction: discord.Interaction):
        color = self.children[1].value
        rgb = color.split()
        db = sqlite3.connect("databases/database.db")
        cur = db.cursor()
        if int(rgb[0]) > 255 or int(rgb[0]) < 0 or int(rgb[1]) > 255 or int(rgb[1]) < 0 or int(rgb[2]) > 255 or int(rgb[2]) < 0:
            embed = discord.Embed(
                title = "Ошибка!",
                description = "Интенсивность цвета не может быть выше 255 и ниже 0"
            )
            embed.set_footer(
                text = f"Запрос от {self.author} • {datetime.today().strftime('%d.%m.%Y,%H:%M:%S')}",
            )
        elif int(self.children[2].value) > 5000:
            embed = discord.Embed(
                title = "Ошибка!",
                description = "Цена не может привышать 5000 <:Money:984020799230988318>"
            )
            embed.set_footer(
                text = f"Запрос от {self.author} • {datetime.today().strftime('%d.%m.%Y,%H:%M:%S')}",
            )
        else:
            perms = discord.Permissions(read_messages  = True)
            role = await self.guild.create_role(name=f"{self.children[0].value}", permissions=perms, color = discord.Color.from_rgb(int(rgb[0]), int(rgb[1]), int(rgb[2])))
            con = cur.execute("SELECT con FROM shop").fetchone()
            if con == None:
                con = 0
            else:
                con = cur.execute("SELECT MAX(con) FROM shop WHERE").fetchone()[0]

            cur.execute(f"INSERT INTO shop VALUES({con+1}, {role.id}, {self.author.id}, {int(self.children[2].value)}, 0)")
            cur.execute("UPDATE users SET hands = hands - 10000 WHERE id = {}".format(self.author.id))
            db.commit()
            
            embed = discord.Embed(color = 0x50d7ad, title = "Новый лот", description = f"Создан лот: {role.mention}\nПродавец: {self.author.mention}\nСтоимость: {int(self.children[2].value)} <:Money:984020799230988318>")
            embed.set_footer(
                text = f"Запрос от {self.author} • {datetime.today().strftime('%d.%m.%Y,%H:%M:%S')}",
            )
            await self.author.add_roles(role)

        await interaction.response.edit_message(embed = embed, view = None)

class Addlot(commands.Cog):

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        print('Commands {} is loaded'.format(self.__class__.__name__))

    @commands.command()
    @commands.cooldown(1, (3), commands.BucketType.user)
    async def addlot(self, ctx):
        db = sqlite3.connect("databases/database.db")
        cur = db.cursor()
        cur.execute("SELECT hands FROM users WHERE id = {}".format(ctx.author.id))
        bal = cur.fetchone()[0]
        if 10000 > bal:
            await ctx.send(
                embed = discord.Embed(
                    title = "Неудачно",
                    description = f"{ctx.author.mention}, на вашем счету недостаточно денег для создания лота"
                )
                .set_footer(
                    text = f"Запрос от {ctx.author} • {datetime.today().strftime('%d.%m.%Y,%H:%M:%S')}"
                )
            )
        else:
            lotButton = Button(label = "Создать лот", style=discord.ButtonStyle.gray, emoji = "<:plus:986553043464106024>")
            async def button_callback(interaction):
                if ctx.author.id == interaction.user.id:
                    modal = LotModal(self.bot, ctx.author, ctx.guild)
                    await interaction.response.send_modal(modal)
            lotButton.callback = button_callback
            view = View()
            view.add_item(lotButton)
            emb = discord.Embed(
                title = "Добавить новый лот",
                description = "Для добовления нового лота нажмите кнопку и заполните данные во всплывшем окне"
            )
            emb.set_footer(
                text = f"Запрос от {ctx.author} • {datetime.today().strftime('%d.%m.%Y,%H:%M:%S')}",
            )
            await ctx.send(embed = emb, view = view)

def setup(client):
    client.add_cog(Addlot(client))