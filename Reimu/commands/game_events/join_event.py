import discord
from discord.ext import commands
from discord.ui import Button, View
import datetime
import time
import sqlite3

connection = sqlite3.connect("databases/database.db")
cursor = connection.cursor()


class Game_Event_Join(commands.Cog):

    def __init__(self, client):
        self.client = client
        print('Commands {} is loaded'.format(self.__class__.__name__))

    @commands.command()
    async def ej(self, inter, code: str):
        print("A")

        try:

            channel = inter.author.voice.channel

            if cursor.execute(
                    "SELECT event_code FROM created_events WHERE event_code = '{}'".format(code)).fetchone() is None:
                await inter.send(
                    embed=discord.Embed(
                        title="Ошибка",
                        description="Такого ивента не существует"
                    ), delete_after=5
                )
            else:
                event = cursor.execute("SELECT * FROM created_events WHERE event_code = '{}'".format(code)).fetchone()
                event_channel = self.client.get_channel(event[3])
                await inter.send(
                    embed=discord.Embed(
                        title=f"Присоединение к событию «{event[1]}»",
                        description=f"**Ведущий:** <@{event[0]}>\n**Событие:** {event[1]}\n**Канал:** <#{event[3]}>"
                    )
                )
                await inter.author.move_to(channel=event_channel)
                await event_channel.set_permissions(inter.author, connect=True)
        except:
            await inter.send(
                embed=discord.Embed(
                    title="Ошибка",
                    description="Вы не находитесь в голосовом канале"
                ), delete_after=5
            )


def setup(client):
    client.add_cog(Game_Event_Join(client))
