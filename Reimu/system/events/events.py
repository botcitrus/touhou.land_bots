import discord
from discord.ext import commands
import json
import sqlite3
from discord.ui import Button, View, Select
import random
import traceback
from datetime import date, time, timedelta, datetime

db = sqlite3.connect('databases/database.db')
cur = db.cursor()

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Events {} is loaded'.format(self.__class__.__name__))

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        db = sqlite3.connect("databases/database.db")
        cur = db.cursor() 
        
        if not member.bot:
            cur.execute(f"SELECT id FROM users where id={member.id}")
            if cur.fetchone() is None:
                cur.execute(f"INSERT INTO users (id) VALUES ({member.id})")
            else:
                pass
            db.commit()
        else:
            pass

    @commands.Cog.listener()
    async def on_ready(self):
        db = sqlite3.connect("databases/database.db")
        cur = db.cursor()
        guild = self.bot.get_guild(795606016728760320)
        for member in guild.members:
            cur.execute(f"SELECT id FROM users where id={member.id}")
            if cur.fetchone()==None:
                cur.execute(f"INSERT INTO users (id) VALUES ({member.id})")
            else:
                pass
            db.commit()


def setup(client):
    client.add_cog(Events(client))