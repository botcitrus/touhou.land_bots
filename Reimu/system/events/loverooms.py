import discord
from discord.ext import commands
import sqlite3

db = sqlite3.connect('databases/database.db')
cur = db.cursor()


class Loverooms(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Events {} is loaded'.format(self.__class__.__name__))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        try:
            channels = cur.execute("SELECT channel FROM loverooms").fetchone()
            if before.channel is not None:
                if len(before.channel.members) == 0 and before.channel.id in channels:
                    await before.channel.delete()
                    cur.execute("DELETE FROM loverooms WHERE channel = {}".format(before.channel.id))
                    db.commit()
        except:
            pass

        try:
            if after.channel.id == 1003607477201412178:
                try:
                    role = discord.utils.get(member.guild.roles, id=795671578829652000)
                    channel_name = cur.execute(
                        "SELECT room FROM loveprofile WHERE first_member = {} OR second_member = {}".format(member.id,
                                                                                                            member.id)).fetchone()[
                        0]
                    first = cur.execute(
                        "SELECT first_member FROM loveprofile WHERE first_member = {} OR second_member = {}".format(
                            member.id, member.id)).fetchone()[0]
                    second = cur.execute(
                        "SELECT second_member FROM loveprofile WHERE first_member = {} OR second_member = {}".format(
                            member.id, member.id)).fetchone()[0]
                    first_member = self.bot.get_user(first)
                    second_member = self.bot.get_user(second)
                    ower = {
                        member.guild.default_role: discord.PermissionOverwrite(view_channel=False, connect=False),
                        role: discord.PermissionOverwrite(view_channel=True, connect=False, manage_channels=False,
                                                          manage_permissions=False),
                        first_member: discord.PermissionOverwrite(view_channel=True, manage_channels=True,
                                                                  manage_permissions=True, connect=True),
                        second_member: discord.PermissionOverwrite(view_channel=True, manage_channels=True,
                                                                   manage_permissions=True, connect=True)
                    }
                    love_room = await member.guild.create_voice_channel(name=channel_name,
                                                                        category=member.guild.get_channel(
                                                                            1002482179516923984), overwrites=ower,
                                                                        user_limit=2)
                    cur.execute("INSERT INTO loverooms VALUES (?)", [love_room.id])
                    db.commit()
                    await member.move_to(channel=love_room)
                except:
                    await member.move_to(channel=None)
        except:
            return


def setup(client):
    client.add_cog(Loverooms(client))
