import discord
from discord.ext import commands
import sqlite3

connection = sqlite3.connect("databases/database.db")
cursor = connection.cursor()

"""
1. Аватар,
2. Дата регистрации,
3. Проверка активности,
4. 

"""


class Dev(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Commands {} is loaded'.format(self.__class__.__name__))




def setup(client):
    client.add_cog(Dev(client))