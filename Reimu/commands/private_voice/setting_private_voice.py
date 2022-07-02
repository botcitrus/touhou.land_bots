from pydoc import cli
import discord
from discord.ext import commands

from discord.ui import InputText, Modal

import random

import sqlite3

import asyncio

class private_voice_buttons(discord.ui.View):

    def __init__(self):
        super().__init__(timeout = None)

    @discord.ui.Button(label = )

class Setting_private(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Commands {} is loaded'.format(self.__class__.__name__))

    @commands.command()
    @commands.has_any_role(977141423931523092)
    async def setting_voice(self, ctx):
        await ctx.send(embed = discord.Embed(
            title = "Управление приватными комнатами",
            description = '''Вы можете изменить конфигурацию своей комнаты с помощью взаимодействий.
                                
                                <> — назначить нового создателя комнаты
                                <> — ограничить/выдать доступ к комнате
                                <> — задать новый лимит участников
                                <> — закрыть/открыть комнату
                                <> — изменить название комнаты
                                <> — скрыть/открыть комнату
                                <> — выгнать участника из комнаты
                                <> — ограничить/выдать право говорить'''
            ).set_image(
                url = "https://img3.akspic.ru/crops/2/3/6/9/4/149632/149632-noch-anime-atmosfera-vselennaya-kosmos-3840x2160.jpg"
            )
        )

def setup(client):
    client.add_cog(Setting_private(client))