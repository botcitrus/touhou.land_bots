import discord
from discord.ext import commands
import json
import sqlite3
from discord.ui import Button, View, Select
import random
import traceback
from datetime import date, time, timedelta, datetime

class MissingAnyRole(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Errors {} is loaded'.format(self.__class__.__name__))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            try:
                embed = discord.Embed(
                    title="Недостаточно прав!",
                    description=f"{ctx.author.mention} у вас нет прав на это действие!"
                )
                await ctx.author.send(embed=embed)
            except:
                embed = discord.Embed(
                    title="Недостаточно прав!",
                    description=f"{ctx.author.mention} у вас нет прав на это действие!"
                )
                await ctx.send(embed=embed)

def setup(client):
    client.add_cog(MissingAnyRole(client))