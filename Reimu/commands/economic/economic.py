import discord
from discord.ext import commands
import sqlite3
import datetime as dt
from discord.ui import InputText, Modal, Button, View
from datetime import datetime
import random

db = sqlite3.connect("databases/database.db")
cur = db.cursor()


class BuyButtons(discord.ui.Button):
    def __init__(self, label, inter, limit, role_id):
        super().__init__(label=label, style=discord.ButtonStyle.primary, emoji="🛒", row=0)
        self.inter = inter
        self.limit = limit
        self.label = label
        self.role_id = role_id

    async def callback(self, interaction):
        if interaction.user == self.inter.author:
            print(self.role_id)
            const = cur.execute("SELECT const FROM shop WHERE role_id = {}".format(self.role_id)).fetchone()[0]
            author = cur.execute("SELECT id FROM shop WHERE role_id = {}".format(self.role_id)).fetchone()[0]
            if const > cur.execute("SELECT hands FROM users WHERE id = {}".format(self.inter.author.id)).fetchone()[0]:
                await interaction.response.send_message(content=f"{self.inter.author.mention}", embed=discord.Embed(
                    title="Покупка не совершилась",
                    description="у вас не достаточно средств"
                ), ephemeral=True)
            else:
                role = self.inter.guild.get_role(self.role_id)
                if role in self.inter.author.roles:
                    await interaction.response.send_message(content=f"{self.inter.author.mention}", embed=discord.Embed(
                        title="Покупка не совершилась",
                        description="у вас уже имеется данный лот"
                    ), ephemeral=True)
                else:
                    cur.execute("UPDATE users SET hands = hands - {} WHERE id = {}".format(const, self.inter.author.id))
                    cur.execute("UPDATE users SET hands = hands + {} WHERE id = {}".format(const, author))
                    cur.execute("UPDATE shop SET quantity = quantity + 1 WHERE role_id = {}".format(self.role_id))
                    db.commit()
                    await self.inter.author.add_roles(role)
                    await interaction.response.edit_message(content=f"{self.inter.author.mention}", embed=discord.Embed(
                        title="Сделка совершена",
                        description=f"{self.inter.author.mention} купил слот под №{self.label} - {role.mention}"
                    ), view=None)


class Button_back(discord.ui.Button):
    def __init__(self, pages, inter, limit, current_page, sorting, sort, con_one):
        super().__init__(emoji="◀️", row=2)
        self.pages = pages
        self.inter = inter
        self.limit = limit
        self.current_page = current_page
        self.sorting = sorting
        self.sort = sort
        self.con_one = con_one

    async def callback(self, interaction):
        if interaction.user == self.inter.author:
            self.current_page -= 1
            self.limit -= 5
            self.con_one = self.limit
            if self.current_page < 1:
                self.con_one = len(self.pages) * 5 - 5
                self.current_page = len(self.pages)
                self.limit = len(self.pages) * 5 - 5
            view = discord.ui.View()
            for x in cur.execute(
                    "SELECT id, role_id, const, quantity, _rowid_ FROM shop ORDER BY {} {} LIMIT {},5".format(
                            self.sorting, self.sort, self.limit)):
                self.con_one += 1
                view.add_item(BuyButtons(str(self.con_one), self.inter, self.limit, role_id=x[1]))

            view.add_item(Shop_select(self.inter))
            view.add_item(Button_back(self.pages, self.inter, self.limit, self.current_page, self.sorting, self.sort,
                                      self.con_one))
            view.add_item(Button_close(self.inter))
            view.add_item(Button_forward(self.pages, self.inter, self.limit, self.current_page, self.sorting, self.sort,
                                         self.con_one))

            await interaction.response.edit_message(content=f"{self.inter.author.mention}",
                                                    embed=self.pages[self.current_page - 1], view=view)


class Button_close(discord.ui.Button):
    def __init__(self, inter):
        super().__init__(emoji="🗑", row=2)
        self.inter = inter

    async def callback(self, interaction):
        if interaction.user == self.inter.author:
            await interaction.response.defer()
            await interaction.edit_original_message(embed=discord.Embed(
                title="Удаление сообщение..."
            ), view=None)
            await interaction.delete_original_message()


class Button_forward(discord.ui.Button):
    def __init__(self, pages, inter, limit, current_page, sorting, sort, con_one):
        super().__init__(emoji="▶️", row=2)
        self.pages = pages
        self.inter = inter
        self.limit = limit
        self.current_page = current_page
        self.sorting = sorting
        self.sort = sort
        self.con_one = con_one

    async def callback(self, interaction):
        if interaction.user == self.inter.author:
            self.current_page += 1
            self.limit += 5
            if self.current_page > len(self.pages):
                self.current_page = 1
                self.con_one = 0
                self.limit = 0

            view = discord.ui.View()
            for x in cur.execute(
                    "SELECT id, role_id, const, quantity, _rowid_ FROM shop ORDER BY {} {} LIMIT {},5".format(
                            self.sorting, self.sort, self.limit)):
                self.con_one += 1
                view.add_item(BuyButtons(label=str(self.con_one), inter=self.inter, limit=self.limit, role_id=x[1]))

            view.add_item(Shop_select(self.inter))
            view.add_item(Button_back(self.pages, self.inter, self.limit, self.current_page, self.sorting, self.sort,
                                      self.con_one))
            view.add_item(Button_close(self.inter))
            view.add_item(Button_forward(self.pages, self.inter, self.limit, self.current_page, self.sorting, self.sort,
                                         self.con_one))

            await interaction.response.edit_message(content=f"{self.inter.author.mention}",
                                                    embed=self.pages[self.current_page - 1], view=view)


class Shop_select(discord.ui.Select):
    def __init__(self, inter):
        options = [
            discord.SelectOption(label='Сначала старые'),
            discord.SelectOption(label='Сначала новые'),
            discord.SelectOption(label='Сначала дорогие'),
            discord.SelectOption(label='Сначала дешевые'),
            discord.SelectOption(label='Сначала популярные')
        ]
        super().__init__(placeholder='Фильтр', min_values=1, max_values=1, options=options, row=1)
        self.inter = inter

    async def callback(self, interaction):
        if interaction.user == self.inter.author:
            view = discord.ui.View()
            emb = discord.Embed(
                title="Магазин ролей"
            )
            if self.values[0] == 'Сначала старые':
                sorting = '_rowid_'
                sort = 'ASC'
            elif self.values[0] == 'Сначала новые':
                sorting = '_rowid_'
                sort = 'DESC'
            elif self.values[0] == 'Сначала дорогие':
                sorting = 'const'
                sort = 'DESC'
            elif self.values[0] == 'Сначала дешевые':
                sorting = 'const'
                sort = 'ASC'
            else:
                sorting = 'quantity'
                sort = 'DESC'

            con_one = 0
            n = 0
            pages = []
            limit = 0
            for x in cur.execute(
                    "SELECT id, role_id, const, quantity, _rowid_ FROM shop ORDER BY {} {} LIMIT 5".format(sorting,
                                                                                                           sort)):
                con_one += 1
                view.add_item(BuyButtons(label=str(con_one), inter=self.inter, limit=limit, role_id=x[1]))

            s = 0
            for x in cur.execute("SELECT id, role_id, const, quantity, _rowid_ FROM shop"):
                s += 1

            a = s // 5
            if s % 5 != 0:
                a += 1

            b = 0
            con_two = 0
            for x in cur.execute(
                    "SELECT id, role_id, const, quantity, _rowid_ FROM shop ORDER BY {} {}".format(sorting, sort)):
                con_two += 1
                n += 1
                emb.add_field(
                    name=f" ⁣ ",
                    value=f"**{con_two}) {self.inter.guild.get_role(x[1]).mention} \nВладелец: <@{x[0]}> \nЦена: {x[2]} \nКуплена {x[3]} раз **",
                    inline=False
                )
                if n == 5:
                    b += 1
                    emb.set_thumbnail(url=self.inter.author.display_avatar)
                    emb.set_footer(text=f"Страница {b}/{a}")
                    pages.append(emb)
                    emb = discord.Embed(
                        title="Магазин ролей"
                    )
                    n = 0

            if n < 5 and n != 0:
                emb.set_thumbnail(url=self.inter.author.display_avatar)
                emb.set_footer(text=f"Страница {b + 1}/{a}")
                pages.append(emb)

            current_page = 1
            view.add_item(Shop_select(self.inter))
            view.add_item(Button_back(pages, self.inter, limit, current_page, sorting, sort, con_one))
            view.add_item(Button_close(self.inter))
            view.add_item(Button_forward(pages, self.inter, limit, current_page, sorting, sort, con_one))

            await interaction.response.edit_message(embed=pages[0], view=view)


class LotModal(Modal):
    def __init__(self, bot, author, guild) -> None:
        self.bot = bot
        self.author = author
        self.guild = guild
        super().__init__(title="Создать лот")

        self.add_item(
            InputText(
                label="Название роли",
                placeholder="Напишите название которое хотите присвоить роли",
                min_length=3,
                max_length=30,
                style=discord.InputTextStyle.singleline
            )
        )

        self.add_item(
            InputText(
                label="Цвет формата RGB",
                placeholder="255 255 255",
                max_length=11,
                style=discord.InputTextStyle.singleline
            )
        )

        self.add_item(
            InputText(
                label="Цена",
                placeholder="Напишите цену роли | макс. цена 2000000",
                max_length=7,
                style=discord.InputTextStyle.singleline
            )
        )

    async def callback(self, interaction: discord.Interaction):
        color = self.children[1].value
        rgb = color.split()
        db = sqlite3.connect("databases/database.db")
        cur = db.cursor()
        if int(rgb[0]) > 255 or int(rgb[0]) < 0 or int(rgb[1]) > 255 or int(rgb[1]) < 0 or int(rgb[2]) > 255 or int(
                rgb[2]) < 0:
            embed = discord.Embed(
                title="Ошибка!",
                description="Интенсивность цвета не может быть выше 255 и ниже 0"
            )
            embed.set_footer(
                text=f"Запрос от {self.author} • {datetime.today().strftime('%d.%m.%Y,%H:%M:%S')}",
            )
        elif int(self.children[2].value) > 2000000 or int(self.children[2].value) > \
                cur.execute("SELECT hands FROM users WHERE id = {}".format(self.author.id)).fetchone()[0]:
            embed = discord.Embed(
                title="Ошибка!",
                description="У вам недостаточно денег <a:crystal:996045979084132382>"
            )
            embed.set_footer(
                text=f"Запрос от {self.author} • {datetime.today().strftime('%d.%m.%Y,%H:%M:%S')}",
            )
        else:
            perms = discord.Permissions(read_messages=True)
            role = await self.guild.create_role(name=f"{self.children[0].value}", permissions=perms,
                                                color=discord.Color.from_rgb(int(rgb[0]), int(rgb[1]), int(rgb[2])))

            cur.execute(f"INSERT INTO shop VALUES({self.author.id}, {role.id}, {int(self.children[2].value)}, 0)")
            cur.execute(
                "UPDATE users SET hands = hands - {} WHERE id = {}".format(self.children[2].value, self.author.id))
            db.commit()

            embed = discord.Embed(color=0x50d7ad, title="Новый лот",
                                  description=f"Создан лот: {role.mention}\nПродавец: {self.author.mention}\nСтоимость: {int(self.children[2].value)} <a:crystal:996045979084132382>")
            embed.set_footer(
                text=f"Запрос от {self.author} • {datetime.today().strftime('%d.%m.%Y,%H:%M:%S')}",
            )
            await self.author.add_roles(role)

        await interaction.response.edit_message(embed=embed, view=None)


class Ecomomic(commands.Cog, name="Economic",
               description="Комманды экономики для того что бы весело провести время и выделится на сервере ролью которой (возможно) ни у кого нет"):
    def __init__(self, bot):
        self.bot = bot
        print('Commands {} is loaded'.format(self.__class__.__name__))

    @commands.command(aliases=["перевести", "заплатить", "перевод", "отправить", "отдать"],
                      help="Команда для того что бы перевести деньги другому участнику")
    @commands.cooldown(1, (3), commands.BucketType.user)
    async def pay(self, ctx, member: discord.Member, *, cash: int):
        author = ctx.message.author
        db = sqlite3.connect("databases/database.db")
        cur = db.cursor()
        if not member.bot:
            cur.execute("SELECT id FROM users WHERE id = {}".format(ctx.author.id))
            user = cur.fetchone()
            if user == None:
                await ctx.send(embed=discord.Embed(
                    color=0x2f3136,
                    title="Пользователь отсутствует в базе данных, попросите пользователя написать любое сообщения для занесения в нее"
                ).set_footer(text=f"Запрос от {author} • {dt.datetime.now().strftime('%d.%m.%Y,%H:%M:%S')}"))
            elif member == ctx.author:
                await ctx.send(embed=discord.Embed(
                    color=0x2f3136,
                    title="Вы не можете отправлять деньги себе!"
                ).set_footer(text=f"Запрос от {author} • {dt.datetime.now().strftime('%d.%m.%Y,%H:%M:%S')}"))
            elif cash <= 0:
                await ctx.send(embed=discord.Embed(
                    color=0x2f3136,
                    title="Вы не можете отправить такую сумму"
                ).set_footer(text=f"Запрос от {author} • {dt.datetime.now().strftime('%d.%m.%Y,%H:%M:%S')}"))
            else:
                bal = cur.execute("SELECT hands FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
                if bal < cash:
                    embed = discord.Embed(
                        color=0x2f3136,
                        description="Недостаточно средств для перевода"
                    )
                    embed.set_footer(text=f"Запрос от {author} • {dt.datetime.now().strftime('%d.%m.%Y,%H:%M:%S')}")
                    await ctx.send(embed=embed)
                else:
                    cur.execute("UPDATE users SET hands = hands - {} WHERE id = {}".format(cash, ctx.author.id))
                    cur.execute("UPDATE users SET hands = hands + {} WHERE id = {}".format(cash, member.id))
                    db.commit()
                    emb = discord.Embed(
                        color=0x2f3136,
                        title="Успешный перевод <:ReactionAccept:980379958717341726>",
                        description=f"Отправитель: {ctx.author.mention}\nПолучатель: {member.mention}\nСумма: {cash}<a:crystal:996045979084132382>"
                    )
                    emb.set_thumbnail(
                        url="https://c.tenor.com/ESnMVcKWPjQAAAAi/prismagica-heart.gif"
                    )
                    emb.set_footer(text=f"Запрос от {author} • {dt.datetime.now().strftime('%d.%m.%Y,%H:%M:%S')}")
                    try:
                        await ctx.send(embed=emb)
                    except:
                        emb.set_footer(text=f"{ctx.author} • {dt.datetime.now().strftime('%d.%m.%Y,%H:%M:%S')}")
        else:
            await ctx.send(embed=discord.Embed(
                color=0xd75050,
                title="Вы не можете отправлять деньги ботам!"
            ).set_footer(text=f"Запрос от {author} • {dt.datetime.now().strftime('%d.%m.%Y,%H:%M:%S')}"))

    @commands.command(aliases=["вывести"],
                      help="Вывести определённую сумму с банка на руки <a:crystal:996045979084132382>")
    @commands.cooldown(1, (3), commands.BucketType.user)
    async def withdout(self, ctx, summ: str):
        author = ctx.message.author
        db = sqlite3.connect("databases/database.db")
        cur = db.cursor()
        bank_summ = cur.execute("SELECT bank FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        hands_summ = cur.execute("SELECT hands FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        if bank_summ <= 0:
            embed = discord.Embed(
                title="Ошибка!",
                description=f"Недостаточно средств!\nДенег в банке: {bank_summ}<a:crystal:996045979084132382>\nДенег на руках: {hands_summ}<a:crystal:996045979084132382>",
                color=0x2f3136
            )
            embed.set_thumbnail(
                url="https://c.tenor.com/ESnMVcKWPjQAAAAi/prismagica-heart.gif"
            )
            embed.set_footer(
                text=f"Запрос от {author} • {dt.datetime.now().strftime('%d.%m.%Y,%H:%M:%S')}"
            )
            await ctx.reply(embed=embed)
        elif summ == "all" and bank_summ <= 0 or summ == "все" and bank_summ <= 0:
            embed = discord.Embed(
                title="Ошибка!",
                description=f"Недостаточно средств!\nДенег в банке: {bank_summ}<a:crystal:996045979084132382>\nДенег на руках: {hands_summ}<a:crystal:996045979084132382>",
                color=0x2f3136
            )
            embed.set_thumbnail(
                url="https://c.tenor.com/ESnMVcKWPjQAAAAi/prismagica-heart.gif"
            )
            embed.set_footer(
                text=f"Запрос от {author} • {dt.datetime.now().strftime('%d.%m.%Y,%H:%M:%S')}"
            )
            await ctx.reply(embed=embed)
        elif summ == "all" or summ == "все":
            cur.execute("UPDATE users SET bank = bank - {} WHERE id = {}".format(bank_summ, ctx.author.id))
            cur.execute("UPDATE users SET hands = hands + {} WHERE id = {}".format(bank_summ, ctx.author.id))
            db.commit()
            bank_summa = cur.execute("SELECT bank FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
            hands_summ = cur.execute("SELECT hands FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
            embed = discord.Embed(
                title="Вывод",
                description=f"Вы вывели все <a:crystal:996045979084132382> с банка\nДенег в банке: {bank_summa}<a:crystal:996045979084132382>\nДенег на руках: {hands_summ}<a:crystal:996045979084132382>",
                color=0x2f3136
            )
            embed.set_thumbnail(
                url="https://c.tenor.com/ESnMVcKWPjQAAAAi/prismagica-heart.gif"
            )
            embed.set_footer(
                text=f"Запрос от {author}"
            )
            await ctx.reply(embed=embed)
        else:
            cur.execute("UPDATE users SET bank = bank - {} WHERE id = {}".format(summ, ctx.author.id))
            cur.execute("UPDATE users SET hands = hands + {} WHERE id = {}".format(summ, ctx.author.id))
            db.commit()
            bank_summa = cur.execute("SELECT bank FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
            hands_summ = cur.execute("SELECT hands FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
            embed = discord.Embed(
                title="Вывод",
                description=f"Вы вывели `{summ}` <a:crystal:996045979084132382> с банка\nДенег в банке: {bank_summa}<a:crystal:996045979084132382>\nДенег на руках: {hands_summ}<a:crystal:996045979084132382>",
                color=0x2f3136
            )
            embed.set_thumbnail(
                url="https://c.tenor.com/ESnMVcKWPjQAAAAi/prismagica-heart.gif"
            )
            embed.set_footer(
                text=f"Запрос от {author} • {dt.datetime.now().strftime('%d.%m.%Y,%H:%M:%S')}"
            )
            await ctx.reply(embed=embed)

    @commands.command(aliases=["dep", "положить"],
                      help="Положить определённую сумму с рук в банк <a:crystal:996045979084132382>")
    @commands.cooldown(1, (3), commands.BucketType.user)
    async def deposit(self, ctx, summ: str):
        author = ctx.message.author
        db = sqlite3.connect("databases/database.db")
        cur = db.cursor()
        bank_summ = cur.execute("SELECT bank FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        hands_summ = cur.execute("SELECT hands FROM users WHERE  id = {}".format(ctx.author.id)).fetchone()[0]
        if hands_summ <= 0:
            embed = discord.Embed(
                title="Ошибка!",
                description=f"Недостаточно средств!\nДенег в банке: {bank_summ}<a:crystal:996045979084132382>\nДенег на руках: {hands_summ}<a:crystal:996045979084132382>"
            )
            embed.set_thumbnail(
                url="https://c.tenor.com/ESnMVcKWPjQAAAAi/prismagica-heart.gif"
            )
            embed.set_footer(
                text=f"Запрос от {author} • {dt.datetime.now().strftime('%d.%m.%Y,%H:%M:%S')}"
            )
            await ctx.reply(embed=embed)
        elif summ == "all" and hands_summ <= 0 or summ == "все" and hands_summ <= 0:
            embed = discord.Embed(
                title="Ошибка!",
                description=f"Недостаточно средств!\nДенег в банке: {bank_summ}<a:crystal:996045979084132382>\nДенег на руках: {hands_summ}<a:crystal:996045979084132382>"
            )
            embed.set_thumbnail(
                url="https://c.tenor.com/ESnMVcKWPjQAAAAi/prismagica-heart.gif"
            )
            embed.set_footer(
                text=f"Запрос от {author} • {dt.datetime.now().strftime('%d.%m.%Y,%H:%M:%S')}"
            )
            await ctx.reply(embed=embed)
        elif summ == "all" or summ == "все":
            cur.execute("UPDATE users SET bank = bank + {} WHERE id = {}".format(hands_summ, ctx.author.id))
            cur.execute("UPDATE users SET hands = hands - {} WHERE id = {}".format(hands_summ, ctx.author.id))
            db.commit()
            bank_summa = cur.execute("SELECT bank FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
            hands_summ = cur.execute("SELECT hands FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
            embed = discord.Embed(
                title="Внос",
                description=f"Вы положили все <a:crystal:996045979084132382> в банк\nДенег в банке: {bank_summa}<a:crystal:996045979084132382>\nДенег на руках: {hands_summ}<a:crystal:996045979084132382>"
            )
            embed.set_thumbnail(
                url="https://c.tenor.com/ESnMVcKWPjQAAAAi/prismagica-heart.gif"
            )
            embed.set_footer(
                text=f"Запрос от {author}"
            )
            await ctx.reply(embed=embed)
        else:
            cur.execute("UPDATE users SET bank = bank + {} WHERE id = {}".format(summ, ctx.author.id))
            cur.execute("UPDATE users SET hands = hands - {} WHERE id = {}".format(summ, ctx.author.id))
            db.commit()
            bank_summa = cur.execute("SELECT bank FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
            hands_summ = cur.execute("SELECT hands FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
            embed = discord.Embed(
                title="Внос",
                description=f"Вы положили `{summ}` <a:crystal:996045979084132382> в банк\nДенег в банке: {bank_summa}<a:crystal:996045979084132382>\nДенег на руках: {hands_summ}<a:crystal:996045979084132382>"
            )
            embed.set_thumbnail(
                url="https://c.tenor.com/ESnMVcKWPjQAAAAi/prismagica-heart.gif"
            )
            embed.set_footer(
                text=f"Запрос от {author} • {dt.datetime.now().strftime('%d.%m.%Y,%H:%M:%S')}"
            )
            await ctx.reply(embed=embed)

    @commands.command(aliases=["выдать", "добавить", "начислить"],
                      help="Выдать определённому пользователю n-ое колличество валюты <a:crystal:996045979084132382>")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, (3), commands.BucketType.user)
    async def addmoney(self, ctx, member: discord.Member, summ: int):
        author = ctx.message.author
        db = sqlite3.connect("databases/database.db")
        cur = db.cursor()
        cur.execute("UPDATE users SET hands = hands + {} WHERE id = {}".format(summ, member.id))
        db.commit()
        cur.execute("SELECT hands FROM users WHERE id = {}".format(member.id))
        balance = cur.fetchone()[0]
        await ctx.reply(
            embed=discord.Embed(
                title="Успешно",
                description=f"Вы вы добавили {summ} на баланс пользователю {member.mention}\nЕго баланс: {balance}"
            )
            .set_footer(
                text=f"Запрос от {author} • {dt.datetime.now().strftime('%d.%m.%Y,%H:%M:%S')}"
            )
        )

    @commands.command(name="shop", aliases=["магазин", "купить", "sh", "s", "buy"],
                      help="Купить роль в магазине за определённую сумму (до 5000 <a:crystal:996045979084132382>)",
                      description="None")
    @commands.cooldown(1, (3), commands.BucketType.user)
    async def shop(self, inter):
        emb = discord.Embed(
            title="Магазин ролей"
        )
        if cur.execute("SELECT * FROM shop").fetchone() == None:
            return await inter.send(
                embed=discord.Embed(
                    title="На сервере отсутствуют роли",
                    color=0x2f3136
                ), ephemeral=True
            )

        view = discord.ui.View()
        n = 0
        pages = []
        limit = 0
        sorting = '_rowid_'
        sort = 'ASC'
        con_one = limit
        for x in cur.execute(
                "SELECT id, role_id, const, quantity, _rowid_ FROM shop ORDER BY {} {} LIMIT 5".format(sorting, sort)):
            con_one += 1
            view.add_item(BuyButtons(label=str(con_one), inter=inter, limit=limit, role_id=x[1]))

        s = 0
        for x in cur.execute("SELECT id, role_id, const, quantity, _rowid_ FROM shop"):
            s += 1

        a = s // 5
        if s % 5 != 0:
            a += 1

        b = 0
        con_two = 0
        for x in cur.execute(
                "SELECT id, role_id, const, quantity, _rowid_ FROM shop ORDER BY {} {}".format(sorting, sort)):
            n += 1
            con_two += 1
            emb.add_field(
                name=f" ⁣ ",
                value=f"**{con_two}) {inter.guild.get_role(x[1]).mention} \nВладелец: <@{x[0]}> \nЦена: {x[2]} \nКуплена {x[3]} раз **",
                inline=False
            )
            if n == 5:
                b += 1
                emb.set_thumbnail(url=inter.author.display_avatar)
                emb.set_footer(text=f"Страница {b}/{a}")
                pages.append(emb)
                emb = discord.Embed(
                    title="Магазин ролей"
                )
                n = 0

        if n < 5 and n != 0:
            emb.set_thumbnail(url=inter.author.display_avatar)
            emb.set_footer(text=f"Страница {b + 1}/{a}")
            pages.append(emb)

        current_page = 1
        view.add_item(Shop_select(inter))
        view.add_item(Button_back(pages, inter, limit, current_page, sorting, sort, con_one))
        view.add_item(Button_close(inter))
        view.add_item(Button_forward(pages, inter, limit, current_page, sorting, sort, con_one))
        await inter.send(content=f"{inter.author.mention}", embed=pages[0], view=view)

    @commands.command(name="addlot", aliases=["новыйлот", "newlot"],
                      help="Добовляет новый лот в магазин за определённую плату", description="None")
    @commands.cooldown(1, (3), commands.BucketType.user)
    @commands.has_any_role(977141423931523092, 795606283339563018)
    async def addlot(self, ctx):
        lotButton = Button(label="Создать лот", style=discord.ButtonStyle.gray, emoji="<:plus:986553043464106024>")

        async def button_callback(interaction):
            if ctx.author.id == interaction.user.id:
                modal = LotModal(self.bot, ctx.author, ctx.guild)
                await interaction.response.send_modal(modal)

        lotButton.callback = button_callback
        view = View()
        view.add_item(lotButton)
        emb = discord.Embed(
            title="Добавить новый лот",
            description="Для добовления нового лота нажмите кнопку и заполните данные во всплывшем окне"
        )
        emb.set_footer(
            text=f"Запрос от {ctx.author} • {datetime.today().strftime('%d.%m.%Y,%H:%M:%S')}",
        )
        await ctx.send(embed=emb, view=view)

    @commands.command(aliases=["работать", "зарабатывать", "работа"],
                      help="Заработать денег на работе <a:crystal:996045979084132382>")
    @commands.cooldown(1, (28800), commands.BucketType.user)
    async def work(self, ctx):
        author = ctx.message.author

        gold = random.randint(80, 160)
        cur.execute("UPDATE users SET hands = hands + {} WHERE id = {}".format(gold, ctx.author.id))
        db.commit()
        for row in cur.execute("SELECT hands FROM users WHERE id = {}".format(ctx.author.id)):
            emb = discord.Embed(color=0x50d7ad, title="Работа",
                                description=f"\nВы заработали: {gold} <a:crystal:996045979084132382>\nБаланс: {row[0]} <a:crystal:996045979084132382>\n")
        emb.set_footer(text=f"Запрос от {author} • {dt.datetime.now().strftime('%d.%m.%Y, %H:%M:%S')}")
        emb.set_thumbnail(
            url='https://media1.tenor.com/images/5c74cfecbfdbb1b36cced28bff9584d2/tenor.gif?itemid=25407710')
        await ctx.send(embed=emb)

    @work.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            hours = error.retry_after // 3600
            minutes = (error.retry_after % 3600) // 60
            seconds = error.retry_after % 60
            return await ctx.send(embed=discord.Embed(
                description=f"Вы уже работали, приходите через: **{hours:.0f} ч. {minutes:.0f} мин. {seconds:.0f} сек.**",
                colour=0xd75050
            ))


def setup(client):
    client.add_cog(Ecomomic(client))

