import discord
from discord.ext import commands
import json
import sqlite3
from discord.ui import Button, View, Select
import random


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
                        value=f"Пользователь - <@{row[0]}>\nУровень - {row[1]}",
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
                            value=f"Пользователь - <@{row[0]}>\nСообщений - {row[1]}",
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
                                value=f"Пользователь - <@{row[0]}>\nНа руках - {row[1]}<a:crystal:996045979084132382>\nВ банке - {row[2]}<a:crystal:996045979084132382>",
                                inline=False
                            )

                        await interaction.response.edit_message(embed=mon_len)


class Rating(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Commands {} is loaded'.format(self.__class__.__name__))

    @commands.command(aliases=['уровень'])
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
            value="1. Уровень\n2. Кол-во сообщений"
        )
        await ctx.reply(embed=embed, view=Leaderboard(ctx.author, ctx.channel))


def setup(client):
    client.add_cog(Rating(client))
