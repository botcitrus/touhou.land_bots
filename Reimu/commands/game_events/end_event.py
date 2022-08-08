import discord
from discord.ext import commands
from discord.ui import Button, View
import datetime
import time
import sqlite3

connection = sqlite3.connect("databases/database.db")
cursor = connection.cursor()

events = ["Codnames", "Who am I?", "Garticphone", "Aliases", "Данетки", "Просмотр", "Свояк", "JackBox", "Monopoly",
          "Бункер", "Намёк понял", "Шпион", "Poker"]


class Game_Event_End(commands.Cog):

    def __init__(self, client):
        self.client = client
        print('Commands {} is loaded'.format(self.__class__.__name__))

    @commands.command()
    async def event_end(self, inter, code: str):

        if cursor.execute("SELECT channel FROM created_events WHERE event_code = '{}' AND eventer = {}".format(code,
                                                                                                               inter.author.id)).fetchone() is None:
            await inter.send(
                embed=discord.Embed(
                    title="Ошибка",
                    description="Такого ивента не существует"
                ), ephemeral=True
            )
        else:
            event = cursor.execute("SELECT * FROM created_events WHERE event_code = '{}'".format(code)).fetchone()
            event_channel = self.client.get_channel(event[3])
            await inter.send(
                embed=discord.Embed(
                    title=f"Завершение события «{event[1]}»",
                    description=f"**Ведущий:** <@{event[0]}>\n**Событие:** {event[1]}\n**Код:** {event[2]}"
                )
            )
            await event_channel.delete()
            cursor.execute(
                "DELETE FROM created_events WHERE event_code = '{}' AND eventer = {}".format(code, inter.author.id))
            connection.commit()


def setup(client):
    client.add_cog(Game_Event_End(client))
