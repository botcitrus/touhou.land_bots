import discord
from discord.ext import commands
import sqlite3

connection = sqlite3.connect("databases/database.db")
cursor = connection.cursor()


class Dev(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Commands {} is loaded'.format(self.__class__.__name__))

    @commands.command()
    async def a(self, ctx):
        await ctx.send(
            embed=discord.Embed(
                title="Ссылка для приглашения на сервер",
                description=f"https://discord.gg/rjXsGZAkPy - ссылка"
            ).set_footer(
                text="С любовью, создатель"
            )
        )

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(
            embed=discord.Embed(
                title="Понг!",
                description=f"Пинг бота состовляет `{round(self.bot.latency * 1000)}` мс :ping_pong:"
            )
        )


def setup(client):
    client.add_cog(Dev(client))
