import discord
from discord.ext import commands
import json
import sqlite3
from discord.ui import Button, View, Select
import random
import traceback
from datetime import date, time, timedelta, datetime

class Voice_event(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Events {} is loaded'.format(self.__class__.__name__))

    

def setup(client):
    client.add_cog(Voice_event(client))