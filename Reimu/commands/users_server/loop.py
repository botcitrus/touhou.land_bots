from discord.ext import commands, tasks


class Tasks(commands.Cog):
    def __init__(self, bot):
        self.channel3 = None
        self.channel2 = None
        self.channel1 = None
        self.guild = None
        self.bot = bot
        print('Command {} is loaded'.format(self.__class__.__name__))

    @tasks.loop(seconds=300)
    async def len_users(self):
        all_users = len(self.guild.members)
        members = len(([member for member in self.guild.members if not member.bot]))
        bots = len(([member for member in self.guild.members if member.bot]))
        await self.channel1.edit(name=f"📕Всего: {all_users}")
        await self.channel2.edit(name=f"📙Пользователей: {members}")
        await self.channel3.edit(name=f"📔Ботов: {bots}")

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(795606016728760320)
        self.channel1 = self.bot.get_channel(1002146458407018586)
        self.channel2 = self.bot.get_channel(1002146491974037535)
        self.channel3 = self.bot.get_channel(1002146514392596480)
        self.len_users.start()


def setup(bot):
    bot.add_cog(Tasks(bot))
