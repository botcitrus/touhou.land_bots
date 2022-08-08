from discord.ext import commands


class Suggestions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Events {} is loaded'.format(self.__class__.__name__))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 1002621364869533887:
            await message.add_reaction('<a:aR_fbLIKE:1003546484874162197>')
            await message.add_reaction('<:ar_dislike:1003546522165727264>')
        else:
            pass


def setup(client):
    client.add_cog(Suggestions(client))
