import discord
from discord.ext import commands
import sqlite3

db = sqlite3.connect('databases/database.db')
cur = db.cursor()


class Voice_event(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Events {} is loaded'.format(self.__class__.__name__))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        try:
            channels = cur.execute("SELECT channel FROM private_voice").fetchone()
            if len(before.channel.members) == 0 and before.channel.id in channels:
                await before.channel.delete()
                cur.execute("DELETE FROM private_voice WHERE channel = {}".format(before.channel.id))
                db.commit()
        except:
            pass

        try:
            if after.channel.id == 866434778264764456:
                role = discord.utils.get(member.guild.roles, id=795671578829652000)
                ower = {member.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                        member: discord.PermissionOverwrite(manage_channels=True, manage_permissions=True),
                        role: discord.PermissionOverwrite(view_channel=True, connect=True, manage_channels=False,
                                                          manage_permissions=False)}
                private_vc = await member.guild.create_voice_channel(name=f"Домик {member.name}",
                                                                     category=member.guild.get_channel(
                                                                         993104434575986698), overwrites=ower)
                cur.execute("INSERT INTO private_voice VALUES (?, ?)", [private_vc.id, member.id])
                db.commit()
                await member.move_to(channel=private_vc)
        except:
            return 


def setup(client):
    client.add_cog(Voice_event(client))
