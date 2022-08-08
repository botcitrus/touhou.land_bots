import discord
from discord.ext import commands
import json
import sqlite3
from discord.ui import Button, View, Select
import random
import traceback
from datetime import date, time, timedelta, datetime

class RequaredArgument(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Errors {} is loaded'.format(self.__class__.__name__))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            db = sqlite3.connect("databases/database.db")
            cur = db.cursor()
            await ctx.reply(embed = discord.Embed(
                title = "Отсутвует обязательный аргумент",
                description = f"{ctx.author.mention}, проверьте заполнили ли вы все обязательные аргументы.\nДля того что бы узнать все аргументы команды используйте команду `+help <command>`"
            ).set_footer(
                text = f"Запрос от {ctx.author} • {datetime.today().strftime('%d.%m.%Y,%H:%M:%S')}",
            )   
            )

def setup(client):
    client.add_cog(RequaredArgument(client))