from discord.ext import commands, tasks
import sqlite3
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

connection = sqlite3.connect("databases/database.db")
cursor = connection.cursor()


class Banner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.guild = None
        print('Commands {} is loaded'.format(self.__class__.__name__))

    @tasks.loop(seconds=10)
    async def banner_update(self):
        voice_users = sum(len(vc.members) for vc in self.guild.voice_channels)
        server_members = len(self.guild.members)
        banner = Image.open("images/banner.png")
        draw = ImageDraw.Draw(banner)
        font = ImageFont.truetype("fonts/banner_font.ttf", size=150)
        draw.text((1254, 529), f"{voice_users}", font=font, fill="white")
        draw.text((1254, 661), f"{server_members}", font=font, fill="white")
        with BytesIO() as ImageBinary:
            banner.save(ImageBinary, "png")
            ImageBinary.seek(0)
            await self.guild.edit(banner=ImageBinary.read())

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(795606016728760320)
        self.banner_update.start()


def setup(client):
    client.add_cog(Banner(client))