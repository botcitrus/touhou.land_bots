import discord
from discord.ext import commands
import sqlite3

db = sqlite3.connect('databases/database.db')
cur = db.cursor()


class Leave(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Events {} is loaded'.format(self.__class__.__name__))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if not member.bot:
            channel = self.bot.get_channel(1002565929986695319)
            await channel.send(
                embed=discord.Embed(
                    title="Прощай путник!",
                    description=f"{member.mention} вышел с сервера, надеемся, то он одумается и вернётся к нам",
                    color=0xFFFB00
                ).set_image(
                    url="https://i.pinimg.com/originals/e6/0e/08/e60e0816aa749b55c1591d51033b0225.gif"
                )
            )
        else:
            await self.bot.get_channel(1002998333142466570).send(
                embed=discord.Embed(
                    title="Новый бот!",
                    description=f"Бот вышел, бот: {member.mention}"
                )
            )


def setup(client):
    client.add_cog(Leave(client))
