import discord
from discord.ext import commands
import sqlite3
import random
from datetime import date, time, timedelta, datetime
import math
from discord.ui import InputText, Modal, Button, View

connection = sqlite3.connect("databases/database.db")
cursor = connection.cursor()

events = ["Codnames", "Who am I?", "Garticphone", "Aliases", "Данетки", "Просмотр", "Своя игра", "JackBox", "Monopoly",
          "Бункер", "Намёк понял", "Шпион", "Poker", "Мафия"]


class Game_Event_Create(commands.Cog):

    def __init__(self, client):
        self.client = client
        print('Commands {} is loaded'.format(self.__class__.__name__))

    @commands.command()
    async def create_event(self, inter, event: str, time: str):

        if event in events:

            about_event = \
            cursor.execute("SELECT about_event FROM events WHERE event_name = '{}'".format(event)).fetchone()[0]
            image = cursor.execute("SELECT event_gif FROM events WHERE event_name = '{}'".format(event)).fetchone()[0]
            awards = cursor.execute("SELECT awards FROM events WHERE event_name = '{}'".format(event)).fetchone()[0]

            member = discord.utils.get(inter.guild.roles, id=795671578829652000)

            ower = {member: discord.PermissionOverwrite(connect=False)}
            events_channel_news = self.client.get_channel(1003226500201451550)
            event_category = self.client.get_channel(1003228111724367872)
            channel = await inter.guild.create_voice_channel(name=f"{event}", category=event_category, overwrites=ower)

            pas = ''
            for x in range(6):
                pas = pas + random.choice(list('1234567890abcdefghigklmnopqrstuvyxwz'))

            cursor.execute(f"INSERT INTO created_events VALUES ({inter.author.id}, '{event}', '{pas}', {channel.id})")
            connection.commit()

            h = time[:-3]
            m = time[-2:]
            h = int(h)
            m = int(m)
            time_obj = datetime.today().replace(hour=h, minute=m, second=0, microsecond=0)

            today = datetime.today()

            if time_obj < today:
                time_obj = time_obj + timedelta(days=1)
            else:
                pass

            time_obj = time_obj.timestamp()

            time_event = math.floor(time_obj)

            await events_channel_news.send("<@&1003222259483279462>", embed=discord.Embed(
                title=f"Событие «{event}» - <t:{time_event}:t>",
                description=f"```{about_event}```"
            ).add_field(
                name=" ⁣ ",
                value=f"**Ведущий:** {inter.author.mention}\n**Время:** <t:{time_event}:t>",
                inline=False
            ).add_field(
                name=" ⁣ ",
                value=f"**Комната мероприятия:** [Лобби](https://discord.com/channels/795606016728760320/1003228870528479303)",
                inline=False
            ).add_field(
                name="**Награда:**",
                value=f"{awards} валюты"
            ).set_image(
                url=f"{image}"
            ),
                                           )
            await inter.send(inter.author.mention,
                             embed=discord.Embed(
                                 title=f"Ивент «{event}» создан",
                                 description=f"Код: {pas}\nКанал ивента: {channel.mention}"
                             ).set_footer(
                                 text="Уведомление об ивенте успешно отправлено!"
                             )
                             )
        else:
            await inter.send(inter.author.mention,
                             embed=discord.Embed(
                                 title=f"Ивент «{event}» не создан",
                                 description=f"Такого ивента нет"
                             )
                             )


def setup(client):
    client.add_cog(Game_Event_Create(client))
