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

class Voice_event(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Events {} is loaded'.format(self.__class__.__name__))

    channels = [962404759292244028, 795669398412066850, 866434778264764456]

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None and after.channel.id == 994530922479235083:
            role = discord.utils.get(member.guild.roles, id = 992014927906734120)
            ower = {member: discord.PermissionOverwrite(manage_channels = True, manage_permissions = True), role: discord.PermissionOverwrite(view_channel = True, connect = True, manage_channels = False, manage_permissions = False)}
            private_vc = await member.guild.create_voice_channel(name = f"Домик {member.name}", category = member.guild.get_channel(994530742132539452), overwrites = ower)
            cur.execute("INSERT INTO private_voice VALUES (?, ?)", [private_vc.id, member.id])
            db.commit()
            await member.move_to(channel = private_vc)
        elif before.channel is not None and after.channel is None:
            try:
                channels = [962404759292244028, 795669398412066850, 866434778264764456]
                if len(before.channel.members) == 0 and before.channel.id not in channels:
                    await before.channel.delete()
                    cur.execute("DELETE FROM private_voice WHERE channel = {}".format(before.channel.id))
                    db.commit()
                elif before.channel.id == cur.execute("SELECT channel FROM private_voice WHERE id = {}".format(member.id)).fetchone()[0]:
                    await before.channel.delete()
                    cur.execute("DELETE FROM private_voice WHERE id = {}".format(member.id))
                    db.commit()
                else:
                    pass
            except:
                pass


def setup(client):
    client.add_cog(Voice_event(client))