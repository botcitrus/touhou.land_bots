import discord
from discord.ext import commands

from discord.ui import InputText, Modal

import random

import asyncio


class VerefyModal(Modal):

    def __init__(self, bot, verefication_code):
        self.bot = bot
        self.verefication_code = verefication_code
        super().__init__(title="Верификация")

        self.add_item(
            InputText(
                label="Введите код",
                placeholder=f"{self.verefication_code}",
                min_length=4,
                max_length=4,
                style=discord.InputTextStyle.singleline
            )
        )

    async def callback(self, interaction: discord.Interaction):
        verefication_role = discord.utils.get(interaction.guild.roles, id=795671578829652000)
        if int(self.children[0].value) == self.verefication_code:
            await interaction.response.send_message(
                embed=discord.Embed(
                    description="Верефикация успешно пройдена, вам будет открыт доступ к чату через 5 секунд..."
                ), ephemeral=True
            )
            await asyncio.sleep(5)
            await interaction.user.add_roles(verefication_role, reason="Верефикация")
        else:
            await interaction.response.send_message(
                embed=discord.Embed(
                    description="Вы не прошли верефикацию, попробуйте снова..."
                ), ephemeral=True
            )


class VerefyButton(discord.ui.View):

    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label="Верификация", style=discord.ButtonStyle.green, custom_id="persistent_view:green")
    async def a_callback(self, button, interaction):
        verefication_code = random.randint(1000, 9999)
        modal = VerefyModal(self.bot, verefication_code)
        await interaction.response.send_modal(modal)


class Verefy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Commands {} is loaded'.format(self.__class__.__name__))

    @commands.command()
    @commands.has_any_role(977141423931523092)
    async def verefy(self, ctx):
        embed = discord.Embed(
            title="Привет! Ты тут? Тогда...",
            description="<:5251onlinestatus:980381350022496306> Нажми на кнопочку ниже, чтобы пройти верификацию и получить доступ к каналам!\n<:5251onlinestatus:980381350022496306> Я создал этот канал, а также эту кнопочку, чтобы защитить тебя от страшных ботов!",
            color=0x2f3136
        )
        embed.set_image(
            url="https://img1.akspic.ru/crops/8/4/9/7/6/167948/167948-anime-anime_art-ken_kaneki-tokio-oblako-3840x2160.jpg"
        )
        await ctx.send(embed=embed, view=VerefyButton(self.bot))

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(VerefyButton(self.bot))


def setup(client):
    client.add_cog(Verefy(client))
