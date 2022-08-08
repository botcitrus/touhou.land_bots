import discord
from discord.ext import commands
import sqlite3
from datetime import timedelta

db = sqlite3.connect('databases/database.db')
cur = db.cursor()


class Welcome(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Events {} is loaded'.format(self.__class__.__name__))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(1002571769309298864)
        if not member.bot:
            await channel.send(
                embed=discord.Embed(
                    title="Приветствую путник!",
                    description=f"{member.mention}, ты попал на уютный сервер под названием {member.guild.name}.\nТы {len(member.guild.members)} на сервере.\nРаспологайся, прочитай <#795612558869397544>, выбери <#795625346127888385> и переходи к общению в <#1003562845075689563>",
                    color=0xFFFB00
                ).set_image(
                    url="https://i.pinimg.com/originals/e6/0e/08/e60e0816aa749b55c1591d51033b0225.gif"
                )
            )
        else:
            try:
                dt = timedelta(seconds=3600)
                await member.timeout_for(duration=dt)
                await self.bot.get_channel(1002998333142466570).send(
                    embed=discord.Embed(
                        title="Новый бот!",
                        description=f"Так как присоединился новый бот, для безопасности он был замучен на 1 час, бот: {member.mention}"
                    )
                )
            except:
                await self.bot.get_channel(1002998333142466570).send(
                    embed=discord.Embed(
                        title="Новый бот!",
                        description=f"Так как присоединился новый бот, мне не удалось его замутить, бот: {member.mention}"
                    )
                )


def setup(client):
    client.add_cog(Welcome(client))
