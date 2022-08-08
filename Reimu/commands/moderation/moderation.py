import discord
from discord.ext import commands
from discord.ui import Button, View
import sqlite3
from datetime import timedelta, datetime


class Warns(discord.ui.View):
    def __init__(self, author, member, channel, guild, limit):
        self.author = author
        self.member = member
        self.channel = channel
        self.guild = guild
        self.limit = limit
        super().__init__(timeout=60)

    @discord.ui.button(style=discord.ButtonStyle.gray, emoji="◀")
    async def stop_callback(self, button, interaction):
        db = sqlite3.connect("databases/database.db")
        cur = db.cursor()
        if self.author.id == interaction.user.id and interaction.channel == self.channel:
            await interaction.response.defer()
            while True:
                if self.limit <= 0:
                    return
                    pass
                else:
                    if self.limit < 5:
                        self.limit = 0
                    else:
                        self.limit -= 10
                        emb = discord.Embed(
                            color=0xff66c9,
                            title="warn list"
                        )
                        for row in cur.execute(
                                "SELECT con, id, adm, reason, date FROM warn WHERE guild = {} AND id = {} ORDER BY _rowid_ ASC LIMIT {},5".format(
                                        self.guild.id, self.member.id, self.limit)):
                            emb.add_field(name=f" №{row[0]} | ID пользователя: {row[1]}",
                                          value=f"Пользователь: <@{row[1]}>\nВыдал: <@{row[2]}>\nПричина: {row[3]}\nДата выдачи: {row[4]}",
                                          inline=False)
                    return await interaction.message.edit(embed=emb)
        else:
            pass

    @discord.ui.button(style=discord.ButtonStyle.grey, emoji="▶")
    async def forward_callback(self, button, interaction):
        db = sqlite3.connect("databases/database.db")
        cur = db.cursor()
        if self.author.id == interaction.user.id and interaction.channel == self.channel:
            await interaction.response.defer()
            while True:
                list_one = []
                kol = 0
                for row in cur.execute(
                        "SELECT id FROM warn WHERE guild = {} AND id = {} ORDER BY _rowid_ LIMIT {}, 5".format(
                                self.guild.id, self.member.id, self.limit)):
                    kol += 1
                    row1 = row[0]
                    row2 = list_one.append(list_one)
                if self.limit < 5:
                    self.limit = 5
                if len(list_one) == 0:
                    return
                else:
                    emb = discord.Embed(color=0xff66c9, title="warn list")
                    for row in cur.execute(
                            "SELECT con, id, adm, reason, date FROM warn WHERE guild = {} AND id = {} ORDER BY _rowid_ ASC LIMIT {},5".format(
                                    self.guild.id, self.member.id, self.limit)):
                        emb.add_field(name=f" №{row[0]} | ID пользователя: {row[1]}",
                                      value=f"Пользователь: <@{row[1]}>\nВыдал: <@{row[2]}>\nПричина: {row[3]}\nДата выдачи: {row[4]}",
                                      inline=False)
                    self.limit += kol
                    return await interaction.message.edit(embed=emb)
        else:
            pass


class Moderation(commands.Cog, name="Moderation",
                 description="Команды которые помогут модераторам и админам следить за порядком на сервере"):

    def __init__(self, bot):
        self.bot = bot
        print('Commands {} is loaded'.format(self.__class__.__name__))

    @commands.command(aliases=['кик'], help="Выгнать пользователя с сервера")
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @commands.cooldown(1, (3), commands.BucketType.user)
    async def kick(self, ctx, member: discord.Member, *, reason: str = "Отсутствует"):
        author = ctx.message.author
        message = ctx.message
        if member and member.top_role.position >= ctx.author.top_role.position or member and member.top_role.position == ctx.author.top_role.position:
            embed = discord.Embed(
                title="Ошибка!",
                description=f"{author.mention}, ваша роль ниже или равна роли {member.mention}",
                color=0x2f3136
            )
            embed.set_image(url="https://c.tenor.com/EfhPfbG0hnMAAAAC/slap-handa-seishuu.gif")
            embed.set_footer(
                text=f"Запрос от {author}"
            )
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(
                title="Вы уверены?",
                description=f"Вы уверены что хотите выгнать {member}?\nНажмите кнопку да если уверены | иначе нажмите кнопку нет",
                color=0x2f3136
            )
            embed.set_footer(
                text=f"Запрос от {author}"
            )

            emb = discord.Embed(title="Подтверждено",
                                description=f"Пользователь {member.mention} был выгнан с сервера!",
                                color=0x2f3136
                                )
            emb.add_field(
                name="Причина:",
                value=f"{reason}",
                inline=True
            )
            emb.add_field(
                name="ID пользователя:",
                value=member.id,
                inline=True
            )
            emb.set_footer(
                text=f"Запрос от {ctx.author} • {datetime.today().strftime('%d.%m.%Y,%H:%M:%S')}",
            )

            embe = discord.Embed(
                title="Действие отменено",
                description="Вы отменили действие, пользователь не будет выгнан",
                color=0x2f3136
            )
            embe.add_field(
                name="Причина:",
                value=f"{reason}",
                inline=True
            )
            embe.add_field(
                name="ID пользователя:",
                value=member.id,
                inline=True
            )
            embe.set_footer(
                text=f"Запрос от {ctx.author} • {datetime.today().strftime('%d.%m.%Y,%H:%M:%S')}",
            )

            button1 = Button(label="Да", style=discord.ButtonStyle.red, emoji="<:NoAccept:980379958293725205>")
            button2 = Button(label="Нет", style=discord.ButtonStyle.green, emoji="<:ReactionAccept:980379958717341726>")

            async def button_callback(interaction):
                if interaction.user == author:
                    await member.kick(reason=reason)
                    await interaction.response.edit_message(embed=emb)

            button1.callback = button_callback

            async def button_callback(interaction):
                if interaction.user == author:
                    await interaction.response.edit_message(embed=embe)

            button2.callback = button_callback

            view = View()
            view.add_item(button1)
            view.add_item(button2)
            await ctx.reply(embed=embed, view=view)

    @commands.command(aliases=['бан'], help="Забанить пользователя на сервере")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.cooldown(1, (3), commands.BucketType.user)
    async def ban(self, ctx, member: discord.Member, *, reason: str = "Отсутствует"):
        author = ctx.message.author
        message = ctx.message
        if member and member.top_role.position >= ctx.author.top_role.position or member and member.top_role.position == ctx.author.top_role.position:
            embed = discord.Embed(
                title="Ошибка!",
                description=f"{author.mention}, ваша роль ниже или равна роли {member.mention}",
                color=0x2f3136
            )
            embed.set_image(
                url="https://c.tenor.com/EfhPfbG0hnMAAAAC/slap-handa-seishuu.gif"
            )
            embed.set_footer(
                text=f"Запрос от {author}"
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Вы уверены?",
                description=f"Вы уверены что хотите забанить {member.mention}?\nНажмите кнопку да если уверены | иначе нажмите кнопку нет",
                color=0x2f3136
            )
            embed.set_footer(
                text=f"Запрос от {ctx.author} • {datetime.today().strftime('%d.%m.%Y,%H:%M:%S')}",
            )

            emb = discord.Embed(title="Подтверждено",
                                description=f"Пользователь {member.mention} был забанен на сервере!",
                                color=0x2f3136
                                )
            emb.add_field(
                name="Причина:",
                value=f"{reason}",
                inline=True
            )
            emb.add_field(
                name="ID пользователя:",
                value=member.id,
                inline=True
            )
            emb.set_footer(
                text=f"Запрос  от {author}"
            )
            emb.set_footer(
                text=f"Запрос от {ctx.author} • {datetime.today().strftime('%d.%m.%Y,%H:%M:%S')}",
            )

            embe = discord.Embed(
                title="Действие отменено",
                description="Вы отменили действие, пользователь не будет забанен",
                color=0x2f3136
            )
            embe.add_field(
                name="Причина:",
                value=f"{reason}",
                inline=True
            )
            embe.add_field(
                name="ID пользователя:",
                value=member.id,
                inline=True
            )
            embe.set_footer(
                text=f"Запрос от {ctx.author} • {datetime.today().strftime('%d.%m.%Y,%H:%M:%S')}",
            )

            button1 = Button(label="Да", style=discord.ButtonStyle.red, emoji="<:NoAccept:980379958293725205>")
            button2 = Button(label="Нет", style=discord.ButtonStyle.green, emoji="<:ReactionAccept:980379958717341726>")

            async def button_callback(interaction):
                if interaction.user == author:
                    await member.ban(reason=reason)
                    await interaction.response.edit_message(embed=emb, view=None)

            button1.callback = button_callback

            async def button_callback(interaction):
                if interaction.user == author:
                    await interaction.response.edit_message(embed=embe, view=None)

            button2.callback = button_callback

            view = View()
            view.add_item(button1)
            view.add_item(button2)
            await ctx.reply(embed=embed, view=view)

    @commands.command(aliases=['разбан'], help="Разбанить пользователя на сервере")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.cooldown(1, (3), commands.BucketType.user)
    async def unban(self, ctx, id: int, reason="Отсутствует"):
        author = ctx.message.author
        member = await self.bot.fetch_user(id)
        embed = discord.Embed(
            title='Пользователь был разбанен',
            description=f'Пользователь <@{id}> был разбанен.',
            color=0x2f3136
        )
        embed.add_field(
            name="Причина:",
            value=f"{reason}",
            inline=True
        )
        embed.add_field(
            name="ID пользователя:",
            value=member.id,
            inline=True
        )
        embed.set_footer(
            text=f"Запрос от {ctx.author} • {datetime.today().strftime('%d.%m.%Y,%H:%M:%S')}",
        )
        await ctx.reply(embed=embed)
        await ctx.guild.unban(member)

    @commands.command(aliases=["мут", "замутить"], help="Забрать право писать и говорить на n-ое количество времени")
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    @commands.cooldown(1, (3), commands.BucketType.user)
    async def mute(self, ctx, member: discord.Member, time: str, *, reason: str = "Отсутствует"):
        dt = time[-1]
        seconds = int(time.strip()[:-1])
        if member.id == ctx.author.id:
            await ctx.send(
                embed=discord.Embed(
                    title="Ошибка!",
                    discord="Вы не можете себя замутить!",
                    color=0x2f3136
                ).set_footer(
                    text=f"Запрос от {ctx.author} • {datetime.today().strftime('%d.%m.%Y,%H:%M:%S')}"
                )
            )
        elif member.top_role >= ctx.author.top_role:
            await ctx.send(
                embed=discord.Embed(
                    title="Ошибка!",
                    discord="Вы не можете замутить пользователя роль которого выше или равна вашей!",
                    color=0x2f3136
                ).set_footer(
                    text=f"Запрос от {ctx.author} • {datetime.today().strftime('%d.%m.%Y,%H:%M:%S')}"
                )
            )
        else:
            if dt == "m" or dt == "м":
                seconds *= 60
            elif dt == "h" or dt == "ч":
                seconds *= 3600
            elif dt == "d" or dt == "д":
                seconds *= 86400
            else:
                await ctx.send(
                    embed=discord.Embed(
                        title="Ошибка!",
                        description="Такое измерение времени нельзя использовать\nИспользуйте команду `help` или документацию что бы узнать как пользоватся данной командой",
                        color=0x2f3136
                    ).set_footer(
                        text=f"Запрос от {ctx.author} • {datetime.today().strftime('%d.%m.%Y,%H:%M:%S')}"
                    )

                )
                return
            dt = timedelta(seconds=seconds)
            await member.timeout_for(duration=dt, reason=reason)
            emb = discord.Embed(
                color=0x2f3136,
                title="Пользователь был замучен",
                description=f"Замутил: {ctx.author.mention}\nПользователь: {member.mention}\nВремя: {time}\nПричина: {reason}")
            emb.set_footer(
                text=f"Запрос от {ctx.author} • {datetime.today().strftime('%d.%m.%Y,%H:%M:%S')}",
            )
            await ctx.send(embed=emb)

    @commands.command(aliases=["размут", "размутить"], help="Вернуть право писать и говорить")
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    @commands.cooldown(1, (3), commands.BucketType.user)
    async def unmute(self, ctx, member: discord.Member, reason="Отсутствует"):
        await member.remove_timeout()
        await ctx.send(
            embed=discord.Embed(
                color=0x2f3136,
                title="Пользователь был размучен",
                description=f"Размутил: {ctx.author.mention}\nПользователь: {member.mention}\nПричина: {reason}"
            ).set_footer(
                text=f"Запрос от {ctx.author} • {datetime.today().strftime('%d.%m.%Y,%H:%M:%S')}",
            )
        )

    @commands.command(aliases=["варн", "пред", "предупредить", "предупреждение"],
                      help="Выдать пользователю предупреждение на сервере")
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason: str = "Отсутствует"):
        db = sqlite3.connect("databases/database.db")
        cur = db.cursor()
        if member.id == ctx.author.id:
            await ctx.reply(
                embed=discord.Embed(
                    title="Ошибка!",
                    description="Вы не можете выдать варн себе"
                )
                .set_footer(
                    text=f"Запрос от {ctx.author} • {datetime.today().strftime('%d.%m.%Y,%H:%M:%S')}",
                )
            )
        elif member.top_role >= ctx.author.top_role:
            await ctx.send(
                embed=discord.Embed(
                    title="Ошибка!",
                    description="Ваша роль ниже или равна роли пользователя которому вы хотите снять варн!"
                )
                .set_footer(
                    text=f"Запрос от {ctx.author} • {datetime.today().strftime('%d.%m.%Y,%H:%M:%S')}",
                )
            )
        else:
            con = cur.execute("SELECT con FROM warn WHERE guild = {}".format(ctx.guild.id)).fetchone()
            if con == None:
                con = 0
                cur.execute("INSERT INTO warn VALUES(?, ?, ?, ?, ?, ?)", (
                (ctx.guild.id), (con + 1), (member.id), (ctx.author.id), (reason),
                (datetime.today().replace(microsecond=0))))
            else:
                con = cur.execute("SELECT MAX(con) FROM warn WHERE guild = {}".format(ctx.guild.id)).fetchone()[0]
                cur.execute("INSERT INTO warn VALUES(?, ?, ?, ?, ?, ?)", (
                (ctx.guild.id), (con + 1), (member.id), (ctx.author.id), (reason),
                (datetime.today().replace(microsecond=0))))
            db.commit()
            await ctx.send(embed=discord.Embed(
                color=0xc82d2d,
                title="Предупреждение",
                description=f"Выдал: {ctx.author.mention}\nПользователь: {member.name}\nПричина: {reason}"
            ))

    @commands.command(aliases=["сп", "снятьпред"], help="Снять предупреждение по номеру случая")
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    async def unwarn(self, ctx, con: int):
        db = sqlite3.connect("databases/database.db")
        cur = db.cursor()
        idu = cur.execute("SELECT id FROM warn WHERE guild = {} AND con = {}".format(ctx.guild.id, con)).fetchone()[0]
        member = ctx.guild.get_member(idu)
        pr = cur.execute("SELECT con FROM warn WHERE guild = {} AND con = {}".format(ctx.guild.id, con)).fetchone()
        if pr == None:
            await ctx.send("такая запись отсутствует")
        if member.id == ctx.author.id:
            await ctx.send(
                embed=discord.Embed(
                    title="Ошибка!",
                    description="Вы не можете снять варн с себя"
                )
                .set_footer(
                    text=f"Запрос от {ctx.author} • {datetime.today().strftime('%d.%m.%Y,%H:%M:%S')}",
                )
            )
        elif member.top_role >= ctx.author.top_role:
            await ctx.send(
                embed=discord.Embed(
                    title="Ошибка!",
                    description="Ваша роль ниже или равна роли пользователя которому вы хотите снять варн!"
                )
                .set_footer(
                    text=f"Запрос от {ctx.author} • {datetime.today().strftime('%d.%m.%Y,%H:%M:%S')}",
                )
            )
        else:
            cur.execute("DELETE FROM warn WHERE guild = {} AND con = {}".format(ctx.guild.id, con))
            db.commit()
            await ctx.send(embed=discord.Embed(
                color=0x33db58,
                title="Варн был снят",
                description=f"**Администратор {ctx.author.mention}\nПользователь: {member}**"
            ))

    @commands.command(aliases=["варны"], help="Посмотреть варны пользователя")
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    async def warns(self, ctx, member: discord.Member):
        db = sqlite3.connect("databases/database.db")
        cur = db.cursor()
        emb = discord.Embed(color=0xff66c9, title="WARN LIST")
        idu = cur.execute("SELECT id FROM warn WHERE guild = {} AND id = {}".format(ctx.guild.id, member.id)).fetchone()
        if not idu:
            return await ctx.reply(
                embed=discord.Embed(
                    title="Отсутствуют",
                    description="У пользователя нет варнов"
                ).set_footer(
                    text=f"Запрос от {ctx.author} • {datetime.today().strftime('%d.%m.%Y,%H:%M:%S')}",
                )
            )
        for row in cur.execute(
                "SELECT con, id, adm, reason, date FROM warn WHERE guild = {} AND id = {} ORDER BY _rowid_ ASC LIMIT 5".format(
                        ctx.guild.id, member.id)):
            emb.add_field(name=f" №{row[0]} | ID пользователя: {row[1]}",
                          value=f"Пользователь: <@{row[1]}>\nВыдал: <@{row[2]}>\nПричина: {row[3]}\nДата выдачи: {row[4]}",
                          inline=False)
        limit = 5
        await ctx.send(embed=emb, view=Warns(ctx.author, member, ctx.channel, ctx.guild, limit))

    @commands.command(aliases=["моиварны"], help="Посмотреть свои    варны")
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    async def my_warns(self, ctx):
        db = sqlite3.connect("databases/database.db")
        cur = db.cursor()
        emb = discord.Embed(color=0xff66c9, title="WARN LIST")
        member = ctx.author
        idu = cur.execute("SELECT id FROM warn WHERE guild = {} AND id = {}".format(ctx.guild.id, member.id)).fetchone()
        if not idu:
            return await ctx.reply(
                embed=discord.Embed(
                    title="Отсутствуют",
                    description="У вас нет варнов"
                ).set_footer(
                    text=f"Запрос от {ctx.author} • {datetime.today().strftime('%d.%m.%Y,%H:%M:%S')}",
                )
            )
        for row in cur.execute(
                "SELECT con, id, adm, reason, date FROM warn WHERE guild = {} AND id = {} ORDER BY _rowid_ ASC LIMIT 5".format(
                        ctx.guild.id, member.id)):
            emb.add_field(name=f" №{row[0]} | ID пользователя: {row[1]}",
                          value=f"Пользователь: <@{row[1]}>\nВыдал: <@{row[2]}>\nПричина: {row[3]}\nДата выдачи: {row[4]}",
                          inline=False)
            emb.set_footer(
                text=f"Запрос от {ctx.author} • {datetime.today().strftime('%d.%m.%Y,%H:%M:%S')}",
            )
        limit = 5
        await ctx.send(embed=emb, view=Warns(ctx.author, member, ctx.channel, ctx.guild, limit))

    @commands.command(aliases=['очистить'], help="Очитьстить n-ое количество сообщений")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.cooldown(1, (3), commands.BucketType.user)
    async def clear(self, ctx, amount: int = 0):
        author = ctx.message.author
        message = ctx.message
        if amount > 100 or amount < 1:
            embed = discord.Embed(
                title="Ошибка",
                description=f"{author.mention} нельзя указать меньше 1 и более 100 сообщений для удаления",
                color=0x2f3136
            )
            embed.set_footer(
                text=f"Запрос от {ctx.author} • {datetime.today().strftime('%d.%m.%Y,%H:%M:%S')}",
            )
            await ctx.reply(embed=embed)
        elif amount > 0 and amount < 101:
            await ctx.channel.purge(limit=amount + 1)
            embed = discord.Embed(
                title="Сообщения удалены",
                description=f"Было удалено {amount} сообщений.",
                color=0x2f3136
            )
            embed.set_footer(
                text=f"Запрос от {ctx.author} • {datetime.today().strftime('%d.%m.%Y,%H:%M:%S')}",
            )
            await ctx.send(embed=embed)
        elif amount == 0:
            embed = discord.Embed(
                title="Укажите количество сообщений!",
                description=f"{author.mention}, укажите колличество сообщений для удаления (макс 100)",
                color=0x2f3136
            )
            embed.set_footer(
                text=f"Запрос от {ctx.author} • {datetime.today().strftime('%d.%m.%Y,%H:%M:%S')}",
            )
            await ctx.reply(embed=embed)


def setup(client):
    client.add_cog(Moderation(client))
