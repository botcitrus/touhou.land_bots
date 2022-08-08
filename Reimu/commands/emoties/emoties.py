import discord
from discord.ext import commands
import random


class Emoties(commands.Cog, name="Emoties",
              description="Обнимайтесь, тыкайте другдруга, деритесь и делайте все, что захотите"):

    def __init__(self, bot):
        self.bot = bot
        print('Commands {} is loaded'.format(self.__class__.__name__))

    @commands.command(pass_context=True, help="Обнять пользователя")
    @commands.cooldown(1, (3), commands.BucketType.user)
    async def hug(self, ctx, *, member: discord.Member):
        author = ctx.message.author
        message = ctx.message
        urls = ['https://c.tenor.com/mB_y2KUsyuoAAAAC/cuddle-anime-hug.gif',
                'https://c.tenor.com/mB_y2KUsyuoAAAAM/cuddle-anime-hug.gif',
                'https://acegif.com/wp-content/gif/anime-hug-83.gif',
                'https://acegif.com/wp-content/gif/anime-hug-59.gif',
                'https://acegif.com/wp-content/gif/anime-hug-38.gif',
                'https://acegif.com/wp-content/gif/anime-hug-49.gif',
                'https://acegif.com/wp-content/gif/anime-hug-86.gif',
                'https://acegif.com/wp-content/gif/anime-hug-79.gif',
                'https://acegif.com/wp-content/gif/anime-hug-14.gif',
                'https://acegif.com/wp-content/gif/anime-hug-27.gif',
                'https://c.tenor.com/DVOTqLcB2jUAAAAC/anime-hug-love.gif',
                'https://c.tenor.com/1T1B8HcWalQAAAAC/anime-hug.gif']
        r = random.randint(0, 11)

        if member == author:
            embed = discord.Embed(description=f"{author}, ты не можешь обнять себя")
            embed.set_image(url="https://c.tenor.com/EfhPfbG0hnMAAAAC/slap-handa-seishuu.gif")
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(
                description=f"**{author}"[:-5] + "**" + " " + f"_крепко обнял(а)_ **{member}"[:-5] + "**")
            embed.set_image(url=urls[r])
            await ctx.reply(embed=embed)

    @commands.command(pass_context=True, help="Поцеловать пользователя")
    @commands.cooldown(1, (3), commands.BucketType.user)
    async def kiss(self, ctx, *, member: discord.Member):
        author = ctx.message.author
        urls = ['https://acegif.com/wp-content/uploads/anime-kissin-13.gif',
                'https://acegif.com/wp-content/uploads/anime-kissin-10.gif',
                'https://acegif.com/wp-content/uploads/anime-kissin-8.gif',
                'https://acegif.com/wp-content/uploads/anime-kissin-5.gif',
                'https://acegif.com/wp-content/uploads/anime-kissin-3.gif',
                'https://acegif.com/wp-content/uploads/anime-kissin-15.gif',
                'https://c.tenor.com/I8kWjuAtX-QAAAAC/anime-ano.gif',
                'https://c.tenor.com/g9HjxRZM2C8AAAAC/anime-love.gif']
        z = random.randint(0, 7)

        if member == author:
            embed = discord.Embed(description=f"{author}, ты не можешь поцеловать себя")
            embed.set_image(url="https://c.tenor.com/EfhPfbG0hnMAAAAC/slap-handa-seishuu.gif")
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(
                description=f"**{author}"[:-5] + "**" + " " + f"_страстно поцеловал(а)_ **{member}"[:-5] + "**")
            embed.set_image(url=f"{urls[z]}")
            await ctx.reply(embed=embed)

    @commands.command(help="Ударить пользователя")
    @commands.cooldown(1, (3), commands.BucketType.user)
    async def punch(self, ctx, *, member: discord.Member):
        author = ctx.message.author
        message = ctx.message

        urls = ['https://i.gifer.com/7zBH.gif', 'https://c.tenor.com/4p2gwNLsxBEAAAAC/whizzy-imposterfox.gif',
                'https://c.tenor.com/jwFPDvtss7QAAAAC/anime-umaru.gif',
                'https://c.tenor.com/DVaAis_eedAAAAAC/orochimaru-tsunade.gif',
                'https://c.tenor.com/o8RbiF5-9dYAAAAC/killua-hxh.gif',
                'https://c.tenor.com/PMCDFLsJodEAAAAC/fight-fighting.gif',
                'https://c.tenor.com/aEX1wE-WrEMAAAAC/anime-right-in-the-stomach.gif',
                'https://c.tenor.com/kWtHiHKx0EYAAAAC/naruto-vs.gif',
                'https://c.tenor.com/UH8Jnl1W3CYAAAAd/anime-punch-anime.gif']

        f = random.randint(0, 8)

        uebok = await self.bot.fetch_user(350697963426676758)

        if author == uebok:
            await ctx.reply("Нет пошел нахуй!")
        if member == author:
            embed = discord.Embed(description=f"{author}, ты не можешь ударить себя (это же больно)")
            embed.set_image(url="https://c.tenor.com/EfhPfbG0hnMAAAAC/slap-handa-seishuu.gif")
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(description=f"**{author}"[:-5] + "**" + " " + f"_ударил(а)_ **{member}"[:-5] + "**")
            embed.set_image(url=f"{urls[f]}")
            await ctx.reply(embed=embed)

    @commands.command(help="Погладить пользователя")
    @commands.cooldown(1, (3), commands.BucketType.user)
    async def pat(self, ctx, *, member: discord.Member):
        author = ctx.message.author
        message = ctx.message

        urls = [
            'http://pristor.ru/wp-content/uploads/2018/07/Красивые-и-прикольные-аниме-гифки-GIF-анимация-сборка-17.gif',
            'https://pa1.narvii.com/6097/1c34e123b5d9820aad9f934c484b3cab88049ab1_hq.gif',
            'https://c.tenor.com/G14pV-tr0NAAAAAC/anime-head.gif',
            'https://pixelbox.ru/wp-content/uploads/2021/11/girls-gif-discord-pixelbox.ru-57.gif',
            'https://pa1.narvii.com/7381/6b517a6b130cba6da8d3770da14c057f355b92e0r1-540-303_hq.gif',
            'https://cdn.discordapp.com/attachments/894002938316460052/894003148237197312/rkBZkRttW.gif',
            'https://c.tenor.com/Dbg-7wAaiJwAAAAC/aharen-aharen-san.gif',
            'https://c.tenor.com/lnoDyTqMk24AAAAC/anime-anime-headrub.gif']

        t = random.randint(0, 7)

        if member == author:
            embed = discord.Embed(description=f"{author}, ты не можешь погладить себя")
            embed.set_image(url="https://c.tenor.com/EfhPfbG0hnMAAAAC/slap-handa-seishuu.gif")
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(description=f"**{author}"[:-5] + "**" + " " + f"_погладил(а)_ **{member}"[:-5] + "**")
            embed.set_image(url=f"{urls[t]}")
            await ctx.reply(embed=embed)

    @commands.command(help="Курить")
    @commands.cooldown(1, (3), commands.BucketType.user)
    async def smoke(self, ctx):
        author = ctx.message.author
        message = ctx.message

        urls = ['https://c.tenor.com/yqKNJzeJZqQAAAAC/kanamewo-smoking.gif',
                'https://c.tenor.com/f273OHcGvYkAAAAC/smoking-anime.gif',
                'https://c.tenor.com/Kmq7jfEn63wAAAAC/anime-smoking.gi',
                'https://c.tenor.com/E2hzqsid1MEAAAAC/anime-smoking.gif',
                'https://c.tenor.com/PvxFlV5UDa4AAAAC/anime-smoking.gif',
                'https://c.tenor.com/jSV1NctKHboAAAAC/anime-sharing.gif',
                'https://c.tenor.com/DI7x6eNuoFwAAAAC/smoke-anime.gif']

        e = random.randint(0, 6)

        embed = discord.Embed(description=f"**{author}"[:-5] + "**" + " _курит_")
        embed.set_image(url=f"{urls[e]}")
        await ctx.reply(embed=embed)

    @commands.command(help="Грустить")
    @commands.cooldown(1, (3), commands.BucketType.user)
    async def sad(self, ctx):
        author = ctx.message.author
        message = ctx.message

        urls = ['https://c.tenor.com/9tOtlaOMTP8AAAAC/sad-cry.gif',
                'https://c.tenor.com/IytNA-LCSTMAAAAC/aesthetic.gif',
                'https://c.tenor.com/oMtGf2HXOcAAAAAC/sad-anime.gif',
                'https://c.tenor.com/CdwDXdGptlsAAAAC/anime-sad-sad.gif',
                'https://c.tenor.com/A0g9Rrx4aNsAAAAC/sad-angry.gif',
                'https://c.tenor.com/hI4mkMsniFYAAAAC/sanji-one-piece.gif']

        w = random.randint(0, 5)

        embed = discord.Embed(description=f"**{author}"[:-5] + "**" + " _грустит_")
        embed.set_image(url=f"{urls[w]}")
        await ctx.reply(embed=embed)

    @commands.command(help="Злиться на пользователя")
    @commands.cooldown(1, (3), commands.BucketType.user)
    async def angry(self, ctx, member: discord.Member = None):
        author = ctx.message.author
        message = ctx.message

        urls = ['https://c.tenor.com/MvKZZ7JCkUMAAAAM/anime-angry.gif',
                'https://c.tenor.com/e94jYOfCH2YAAAAM/hxh-anime.gif',
                'https://c.tenor.com/X3x3Y2mp2W8AAAAM/anime-angry.gif',
                'https://c.tenor.com/rzDkOlEDun0AAAAM/hayase-nagatoro-nagatoro-angry.gif',
                'https://c.tenor.com/HzZIzXahdw0AAAAM/one-punch-man-saitama.gif',
                'https://c.tenor.com/X3x3Y2mp2W8AAAAC/anime-angry.gif',
                'https://c.tenor.com/XfT1-01KEPAAAAAC/anime-angry.gif']

        w = random.randint(0, 6)

        if member == None:
            embed = discord.Embed(description=f"{author.name} _злится_")
            embed.set_image(url=f"{urls[w]}")
            await ctx.reply(embed=embed)
        elif member == author:
            embed = discord.Embed(description=f"{author.name} _злится на себя_")
            embed.set_image(url=f"{urls[w]}")
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(description=f"**{author}"[:-5] + "**" + f" _злится на_ **{member}"[:-5] + "**")
            embed.set_image(url=f"{urls[w]}")
            await ctx.reply(embed=embed)

    @commands.command(help="Укусить пользователя")
    @commands.cooldown(1, (3), commands.BucketType.user)
    async def bite(self, ctx, member: discord.Member):
        author = ctx.message.author
        message = ctx.message

        urls = ['https://c.tenor.com/noV5mMA7T8oAAAAS/loli-bite.gif',
                'https://c.tenor.com/4j3hMz-dUz0AAAAM/anime-love.gif',
                'https://c.tenor.com/Xpv7HTk-DIYAAAAM/mad-angry.gif',
                'https://c.tenor.com/TwP8Vv8acSkAAAAM/the-melancholy-of-haruhi-suzumiya-biting-ear.gif',
                'https://c.tenor.com/DjvVtKrojMwAAAAM/anime-acchi-kocchi.gif',
                'https://c.tenor.com/JMqUl2FWtDYAAAAC/bite-hurt.gif']

        w = random.randint(0, 5)

        if member == author:
            embed = discord.Embed(description=f"{author.mention}, ты не можешь укусить себя")
            embed.set_image(url="https://c.tenor.com/EfhPfbG0hnMAAAAC/slap-handa-seishuu.gif")
            await message.delete()
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(description=f"**{author}"[:-5] + "**" + " " + f"_укусил(а)_ **{member}"[:-5] + "**")
            embed.set_image(url=f"{urls[w]}")
            await ctx.reply(embed=embed)

    @commands.command(help="Похлопать")
    @commands.cooldown(1, (3), commands.BucketType.user)
    async def clap(self, ctx, member: discord.Member = None):
        author = ctx.message.author
        message = ctx.message

        urls = ["https://c.tenor.com/jncqY9-RbqcAAAAd/mushoku-tensei-roxy.gif",
                "https://c.tenor.com/9KYyvVXuROkAAAAC/nagatoro-clap.gif",
                "https://c.tenor.com/tyb15RWixEYAAAAC/puck-anime.gif",
                "https://c.tenor.com/zVvMxtmpRaMAAAAC/taiga-asaka-clapping.gif",
                "https://c.tenor.com/2RMlQdkpG1cAAAAC/clapping-anime.gif",
                "https://c.tenor.com/2RMlQdkpG1cAAAAC/clapping-anime.gif",
                "https://c.tenor.com/L0gGeWVPmzQAAAAC/reaction-proud.gif",
                "https://c.tenor.com/r645OeLxJscAAAAC/anime-clap.gif"]

        w = random.randint(1, 7)

        if member == None:
            embed = discord.Embed(description=f"{author}"[:-5] + " _похлопал_")
            embed.set_image(url=urls[w])
            await ctx.reply(embed=embed)
        elif member == author:
            embed = discord.Embed(description=f"{author}"[:-5] + " _похлопал себе хорошенькому_")
            embed.set_image(url=urls[w])
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(description=f"**{author}"[:-5] + "**" + " " + f"_похлопал(а)_ **{member}"[:-5] + "**")
            embed.set_image(url=urls[w])
            await ctx.reply(embed=embed)

    @commands.command(help="Покормить пользователя")
    @commands.cooldown(1, (3), commands.BucketType.user)
    async def feed(self, ctx, *, member: discord.Member):
        author = ctx.message.author
        message = ctx.message
        urls = ["https://i.kym-cdn.com/photos/images/original/001/082/775/c24.gif",
                "https://c.tenor.com/JHqOKnXVNDQAAAAC/azunom-feed.gif",
                "https://c.tenor.com/WlNZ9l4eMjwAAAAC/sick-anime.gif", "https://c.tenor.com/Kpw8-sodxCcAAAAC/feed.gif",
                "https://c.tenor.com/Nk-Eq8_ZiNwAAAAC/index-toaru.gif"]
        w = random.randint(0, 4)

        embed = discord.Embed(description=f"**{author.namr}" + "**" + " " + f"_покормил_ **{member}"[:-5] + "**")
        embed.set_image(url=urls[w])
        await ctx.reply(embed=embed)

    @commands.command(help="Танцевать")
    @commands.cooldown(1, (3), commands.BucketType.user)
    async def dance(self, ctx):
        author = ctx.message.author
        urls = ['https://c.tenor.com/LP6rGpITvlsAAAAC/chill.gif', 'https://i.gifer.com/bQ.gif',
                'https://c.tenor.com/oOrsGFrf-6wAAAAC/dance-dance-moves.gif',
                'https://c.tenor.com/xBh07rz9GHYAAAAd/nezuko-kamado-nezuko.gif',
                'https://c.tenor.com/mKTS5nbF1zcAAAAC/cute-anime-dancing.gif']
        rand = random.randint(0, 4)

        embed = discord.Embed(description=f"**{author}"[:-5] + "**" + " _танцует_")
        embed.set_image(url=f'{urls[rand]}')
        await ctx.reply(embed=embed)


def setup(client):
    client.add_cog(Emoties(client))