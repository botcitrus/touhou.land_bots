import discord
from discord.ext import commands
import sqlite3

db = sqlite3.connect("databases/database.db")
cur = db.cursor()


class Leaderboard(discord.ui.View):
    def __init__(self, author, channel):
        self.author = author
        self.channel = channel
        super().__init__()

    @discord.ui.select(placeholder='Выберите раздел', min_values=1, max_values=1, options=[
        discord.SelectOption(label='По уровню', description='Сортировка по уровню', emoji='🏆'),
        discord.SelectOption(label='По кол-ву сообщений', description='Сортировка по кол-ву сообщений', emoji='💬'),
        discord.SelectOption(label='По кол-ву валюты', description='Сортировка по кол-ву валюты',
                             emoji='<a:crystal:996045979084132382>'),
    ])
    async def select_callback(self, select, interaction):
        db = sqlite3.connect("databases/database.db")
        cur = db.cursor()
        if self.author.id == interaction.user.id and interaction.channel == self.channel:
            if select.values[0] == 'По уровню':
                lvl_rank = discord.Embed(
                    title="Таблица лидеров по уровню",
                    description="Выведена таблица лидеров по уровню (Топ 5)",
                    color=self.author.color
                )
                con = 0

                lvl_rank.set_thumbnail(
                    url="https://i.pinimg.com/originals/72/4c/7c/724c7cc8c61a0a8820e7d6867bbdb421.gif"
                )
                for row in cur.execute(f"SELECT id, lvl FROM users WHERE lvl > -1 ORDER BY lvl DESC LIMIT 5"):
                    con += 1
                    lvl_rank.add_field(
                        name=f"{con} место",
                        value=f"Пользователь - <@{row[0]}>\nУровень - `{row[1]}`",
                        inline=False
                    )
                await interaction.response.edit_message(embed=lvl_rank)
            else:
                if select.values[0] == 'По кол-ву сообщений':
                    mess_len = discord.Embed(
                        title="Таблица лидеров по кол-ву сообщений",
                        description="Выведена таблица лидеров по кол-ву сообщений (Топ 5)",
                        color=self.author.color
                    )

                    mess_len.set_thumbnail(
                        url="https://i.pinimg.com/originals/72/4c/7c/724c7cc8c61a0a8820e7d6867bbdb421.gif"
                    )
                    con = 0
                    for row in cur.execute(
                            f"SELECT id, messages FROM users WHERE messages > -1 ORDER BY messages DESC LIMIT 5"):
                        con += 1
                        mess_len.add_field(
                            name=f"{con} место",
                            value=f"Пользователь - <@{row[0]}>\nСообщений - `{row[1]}`",
                            inline=False
                        )

                    await interaction.response.edit_message(embed=mess_len)
                else:
                    if select.values[0] == 'По кол-ву валюты':
                        mon_len = discord.Embed(
                            title="Таблица лидеров по кол-ву сообщений",
                            description="Выведена таблица лидеров по кол-ву денег на руках (Топ 5)",
                            color=self.author.color
                        )

                        mon_len.set_thumbnail(
                            url="https://i.pinimg.com/originals/72/4c/7c/724c7cc8c61a0a8820e7d6867bbdb421.gif"
                        )
                        con = 0
                        for row in cur.execute(
                                f"SELECT id, hands, bank FROM users WHERE hands > -1 ORDER BY hands DESC LIMIT 5"):
                            con += 1
                            mon_len.add_field(
                                name=f"{con} место",
                                value=f"Пользователь - <@{row[0]}>\nНа руках - `{row[1]}`<a:crystal:996045979084132382>\nВ банке - `{row[2]}`<a:crystal:996045979084132382>",
                                inline=False
                            )

                        await interaction.response.edit_message(embed=mon_len)


class Users(commands.Cog, name="Users",
            description="Команды для просмотра |Рейтинга|Профиля|Информации|Таблицы лидеров| и взаимодействия со своим профилем"):

    def __init__(self, bot):
        self.bot = bot
        print('Commands {} is loaded'.format(self.__class__.__name__))

    @commands.command(aliases=['юзер'], help="Показывает детальную информацию о пользователе на платформе дискорд",
                      description="None")
    @commands.cooldown(1, (3), commands.BucketType.user)
    async def user(self, ctx, member: discord.Member = None):
        author = ctx.message.author
        if type(member) is int:
            member = await self.bot.get_user(member)
        if member == None:
            member = ctx.author
        message = ctx.message
        t = member.status
        if t == discord.Status.online:
            d = "<:5251onlinestatus:980381350022496306> В сети"

        if t == discord.Status.offline:
            d = "<:2179offlinestatus:980382190288375848> Не в сети"

        if t == discord.Status.idle:
            d = "<:4572discordidle:980381585432018994> Нет на месте"

        if t == discord.Status.dnd:
            d = "<:discord_dnd:980384459780149278> Не беспокоить"

        if t == discord.Status.invisible:
            d = "<:2179offlinestatus:980382190288375848> Инвиз"

        if t == discord.Status.streaming:
            d = "<:streaming:982290617122033785> Стримит"

        act = member.activity
        if act == "None":
            act = "Активность отсутствует"
        embed = discord.Embed(
            title=f"Информация о пользователе {member.name}",
            colour=0x2f3136
        )
        embed.add_field(
            name="<:DiscordServerStaff:980380004762390558> Основная информация о пользователе",
            value=f">>> • Имя пользователя: {member}\n• Id пользователя: {member.id}\n• Статус пользователя: {d}\n• Активность пользователя: {act}\n• <:killua_bcalendario:980388309375279125>Присоеденился: <t:{int(member.joined_at.timestamp()):F>}>\n• <:killua_bcalendario:980388309375279125>Аккаунт создан: <t:{int(member.created_at.timestamp()):F>}>",
            inline=False
        )
        embed.set_footer(
            text=f"Запрос от {author}"
        )
        embed.set_thumbnail(
            url=member.avatar
        )
        try:
            await ctx.reply(embed=embed)
        except:
            embed.set_thumbnail(
                url="https://i.pinimg.com/564x/1a/63/c2/1a63c2a0db3993a951bd86f6d7648175.jpg"
            )
            await ctx.reply(embed=embed)

    @commands.command(aliases=['профиль'], help="Показывает серверную информацию об участнике", description="None")
    @commands.cooldown(1, (3), commands.BucketType.user)
    async def profile(self, ctx, member: discord.Member = None):
        author = ctx.message.author
        if member == None:
            member = author
        embed = discord.Embed(
            title=f"Информация о {member.name}",
            description="Был выведен профиль участника:\nДля добовления описания используйте команду `biography`",
            colour=0x2f3136
        )
        for row in cur.execute(
                f"SELECT messages, lvl, xp, hands, bank, biography, spouse FROM users WHERE id = {member.id}"):
            embed.add_field(
                name="**__Рейтинговая информация пользователя:__**",
                value="↳",
                inline=False
            )
            embed.add_field(
                name="Кол-во сообщений:",
                value=f"> `{row[0]}`<:messagesfront3:984011645040885780>",
                inline=True
            )
            embed.add_field(
                name="Уровень:",
                value=f"> `{row[1]}`<:trophy_platinum:984011657569239080>",
                inline=True
            )
            embed.add_field(
                name="Опыт:",
                value=f"> `{row[2]}`<:ExperiencePointXP:984011635050045461>",
                inline=True
            )
            embed.add_field(
                name="**__Банковская информация пользователя:__**",
                value="↳",
                inline=False
            )
            embed.add_field(
                name="На руках",
                value=f"> `{row[3]}` <a:crystal:996045979084132382>",
                inline=True
            )
            embed.add_field(
                name="Банк",
                value=f"> `{row[4]}` <:bankcards:984013312922628106>",
                inline=True
            )
            embed.add_field(
                name="ID пользователя",
                value=f"> `{member.id}`",
                inline=True
            )
            embed.add_field(
                name="**__Семейная информация пользователя:__**",
                value="↳",
                inline=False
            )
            if row[6] == None:
                embed.add_field(
                    name="В браке с:",
                    value=f"`Одинок(а)`",
                    inline=False
                )
            else:
                embed.add_field(
                    name="В браке с:",
                    value=f"<@{row[6]}>",
                    inline=False
                )
            embed.add_field(
                name="О себе:",
                value=f"```{row[5]}```",
                inline=False
            )
        embed.set_thumbnail(
            url=member.avatar
        )
        try:
            await ctx.reply(embed=embed)
        except:
            embed.set_thumbnail(
                url="https://i.pinimg.com/originals/72/4c/7c/724c7cc8c61a0a8820e7d6867bbdb421.gif"
            )
            await ctx.reply(embed=embed)

    @commands.command(aliases=['осебе'], help="Устанавливает ваше описание в профиле")
    @commands.cooldown(1, (3), commands.BucketType.user)
    async def biography(self, ctx, *, text):
        author = ctx.message.author
        db = sqlite3.connect("databases/database.db")
        cur = db.cursor()
        cur.execute(f"UPDATE users SET biography = '{text}' WHERE id={author.id}")
        db.commit()
        embed = discord.Embed(
            title="Биография установлена!",
            description=f"Вы установили текст для раздела `О себе`\nВаш текст:\n```{text}```",
            color=0x2f3136
        )
        embed.set_thumbnail(
            url="https://c.tenor.com/ESnMVcKWPjQAAAAi/prismagica-heart.gif"
        )
        embed.set_footer(
            text=f"Запрос от {author}"
        )
        await ctx.reply(embed=embed)

    @commands.command(aliases=['уровень'], help="Выдать пользователю определённый уровень")
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, (3), commands.BucketType.user)
    async def level(self, ctx, member: discord.Member, *, lvl: int):
        author = ctx.message.author
        db = sqlite3.connect("databases/database.db")
        cur = db.cursor()
        if lvl < 0:
            embed = discord.Embed(
                title="Ошибка!",
                description="Был указан невозможный уровень либо он не был указан вообще!",
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
            cur.execute(f"UPDATE users SET lvl = {lvl}, xp = 0 WHERE id={member.id}")
            db.commit()
            embed = discord.Embed(
                title="Уровень установлен!",
                description=f"Вы установили {lvl} уровень для {member.mention}",
                color=0x2f3136
            )
            embed.set_thumbnail(
                url="https://c.tenor.com/ESnMVcKWPjQAAAAi/prismagica-heart.gif"
            )
            embed.set_footer(
                text=f"Запрос от {author}"
            )
            await ctx.reply(embed=embed)

    @commands.command(aliases=['лидеры'])
    @commands.cooldown(1, (3), commands.BucketType.user)
    async def leaderboard(self, ctx):
        author = ctx.message.author
        embed = discord.Embed(
            title="Выберите раздел",
            description="Выберете раздел таблицы лидеров, который хотите увидеть",
            color=ctx.author.color
        )
        embed.add_field(
            name="Разделы:",
            value="<:trophy_platinum:984011657569239080> Уровень\n<:messagesfront3:984011645040885780> Кол-во сообщений\n<a:crystal:996045979084132382> По количеству денег"
        )
        await ctx.reply(embed=embed, view=Leaderboard(ctx.author, ctx.channel))


def setup(client):
    client.add_cog(Users(client))
