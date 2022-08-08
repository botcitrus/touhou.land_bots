import discord
from discord.ext import commands
import sqlite3
import random

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
            if cur.fetchone() is None:
                cur.execute(f"INSERT INTO users (id) VALUES ({member.id})")
            else:
                pass
            db.commit()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 866510473444458496 and message.author.id != 992755518458318998:
            await message.delete()

        if message.author.bot:
            return

        if self.bot.user in message.mentions:
            guildid = message.guild.id
            await message.channel.send(
                embed=discord.Embed(
                    title="Что-то хотели?",
                    description=f">>> Мой перфикс `+`\nЧто бы узнать больше о командах воспользуйтесь `+help`",
                    color=0x2f3136
                )
            )
            return

        try:
            if len(message.content) >= 1:
                a = random.randint(1, 7)
                cur.execute(f"UPDATE users SET messages = messages + 1 WHERE id={message.author.id}")
                cur.execute(f"UPDATE users SET xp = xp + {a} WHERE id={message.author.id}")
            cur.execute(f"SELECT xp FROM users where id={message.author.id}")
            xp_len = cur.fetchone()[0]
            try:
                lvl_user = cur.execute(f"SELECT lvl FROM users where id={message.author.id}").fetchone()[0]
                if lvl_user < 1:
                    if xp_len == 50 or xp_len >= 50:
                        cur.execute(f"UPDATE users SET lvl = lvl + 1 WHERE id={message.author.id}")
                        cur.execute(f"UPDATE users SET xp = 0 WHERE id={message.author.id}")
                    else:
                        pass
                    db.commit()
                else:
                    new_lvl = lvl_user * (1000 * 5 / 100)
                    if xp_len == new_lvl or xp_len >= new_lvl:
                        cur.execute(f"UPDATE users SET lvl = lvl + 1 WHERE id={message.author.id}")
                        cur.execute(f"UPDATE users SET xp = 0 WHERE id={message.author.id}")
                    db.commit()
                db.commit()
            except:
                pass
        except:
            pass


def setup(client):
    client.add_cog(Events(client))
