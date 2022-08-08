import discord
from discord.ext import commands
import json
import datetime
import sqlite3

db = sqlite3.connect("databases/database.db")
cur = db.cursor()


class Users(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Commands {} is loaded'.format(self.__class__.__name__))

    @commands.command(aliases=['юзер'], help="Показывает детальную информацию о пользователе на платформе дискорд")
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

    @commands.command(aliases=['профиль'], help="Показывает серверную информацию об участнике ()")
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

    @commands.command(aliases=['осебе'])
    @commands.cooldown(1, (3), commands.BucketType.user)
    async def biography(self, ctx, *, text="Отсутствует"):
        author = ctx.message.author
        db = sqlite3.connect("databases/database.db")
        cur = db.cursor()
        if text == "Отсутствует":
            embed = discord.Embed(
                title="Ошибка!",
                description="Вы не написали текст!",
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


def setup(client):
    client.add_cog(Users(client))
