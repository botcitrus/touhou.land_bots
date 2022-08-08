import discord
from discord.ext import commands
import sqlite3
import datetime as dt
import random


class Game(commands.Cog, name="Game", description="Команды для того что бы весело провести время (Может и не очень)"):
    def __init__(self, bot):
        self.bot = bot
        print('Commands {} is loaded'.format(self.__class__.__name__))

    @commands.command(aliases=['слоты'],
                      help="Испытай удачу в слотах, уйди со всем или проиграй всё (ОСТОРОЖНО, ЗАТЯГИВАЕТ)")
    @commands.cooldown(1, (3), commands.BucketType.user)
    async def slots(self, ctx, cash: int, game: int):
        author = ctx.message.author
        db = sqlite3.connect("databases/database.db")
        cur = db.cursor()
        bal = cur.execute("SELECT hands FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        summ = cash * game
        if summ > bal:
            await ctx.send(
                embed=discord.Embed(
                    title="Ошибка",
                    description="недостаточно средств",
                    color=0xd75050
                ).set_footer(
                    text=f"Запрос от {author} • {dt.datetime.now().strftime('%d.%m.%Y,%H:%M:%S')}"
                )
            )
        elif cash < 100 or cash > 1000000:
            await ctx.send(
                embed=discord.Embed(
                    color=0xd75050,
                    title="Ошибка",
                    description="Минимальная ставка 100\nМаксимальная ставка 1000000"
                ).set_footer(
                    text=f"Запрос от {author} • {dt.datetime.now().strftime('%d.%m.%Y,%H:%M:%S')}"
                )
            )
        elif game > 6:
            await ctx.send(
                embed=discord.Embed(
                    color=0xd75050,
                    title="Ошибка",
                    description="максимальное кол-во игр 6"
                ).set_footer(
                    text=f"Запрос от {author} • {dt.datetime.now().strftime('%d.%m.%Y,%H:%M:%S')}"
                )
            )
        else:

            lose = [
                "|:dart:|:tickets:|:four_leaf_clover:|\n|:8ball:|:game_die:|:dart:|:arrow_left:\n|:accordion:|:four_leaf_clover:|:game_die:|",
                "|:8ball:|:accordion:|:tickets:|\n|:dart:|:8ball:|:dart:|:arrow_left:\n|:game_die:|:four_leaf_clover:|:tickets:|",
                "|:tickets:|:tickets:|:accordion:|\n|:8ball:|:game_die:|:four_leaf_clover:|:arrow_left:\n|:dart:|:8ball:|:game_die:|",
                "|:game_die:|:dart:|:accordion:|\n|:tickets:|:four_leaf_clover:|:8ball:|:arrow_left:\n|:dart:|:four_leaf_clover:|:game_die:|"]
            win = [
                "|:dart:|:game_die:|:8ball:|\n|:four_leaf_clover:|:four_leaf_clover:|:four_leaf_clover:|:arrow_left:\n|:accordion:|:dart:|:tickets:|",
                "|:game_die:|:8ball:|:accordion:|\n|:dart:|:dart:|:dart:|:arrow_left:\n|:accordion:|:four_leaf_clover:|:game_die:|",
                "|:dart:|:8ball:|:four_leaf_clover:|\n|:tickets:|:tickets:|:tickets:|:arrow_left:\n|:8ball:|:game_die:|:four_leaf_clover:|"]

            games = 0
            znwin = 0
            znlose = 0
            sum = 0
            emb = discord.Embed(title="Слоты", description=f"Вы поставили на слоты: {cash} <:Money:984020799230988318>",
                                color=ctx.author.color)
            while games < game:
                chance = random.randint(1, 6)
                if chance == 3:
                    znwin += 1
                    games += 1
                    ras = cash // 100 * 200
                    cur.execute("UPDATE users SET hands = hands + {} WHERE id = {}".format(ras, ctx.author.id))
                    db.commit()
                    emb.add_field(name=":tada:СЛОТ:tada:", value="{}\nВыигрыш: {}".format(random.choice(win), ras))
                    emb.set_thumbnail(url=ctx.author.avatar)
                    emb.set_footer(
                        text=f"Запрос от {author} • {dt.datetime.now().strftime('%d.%m.%Y,%H:%M:%S')}"
                    )
                    zn = random.randint(1, 4)
                    sum += ras
                else:
                    games += 1
                    znlose += 1
                    cur.execute("UPDATE users SET hands = hands - {} WHERE id = {}".format(cash, ctx.author.id))
                    db.commit()
                    emb.add_field(name="СЛОТ", value="{}\nПроигрыш: {}".format(random.choice(lose), cash))
                    emb.set_thumbnail(url=ctx.author.avatar)
                    emb.set_footer(
                        text=f"Запрос от {author} • {dt.datetime.now().strftime('%d.%m.%Y,%H:%M:%S')}"
                    )
                    zn = random.randint(1, 4)
                    sum -= cash

            cur.execute("SELECT hands FROM users WHERE id = {}".format(ctx.author.id))
            bal = cur.fetchone()[0]
            emb.add_field(name=f"Игр: {game}",
                          value=f"Проиграно: {znlose}\nВыиграно: {znwin}\nПрофит: {sum}\nБаланс: <:Money:984020799230988318> {bal}")
            await ctx.send(embed=emb)

    @commands.command(aliases=['рулетка'], help="Русская рулетка, попробуй, если кишка не тонка")
    @commands.cooldown(1, (3), commands.BucketType.user)
    async def rulet(self, ctx, cash: int, shot: int):
        db = sqlite3.connect("databases/database.db")
        cur = db.cursor()
        cur.execute("SELECT hands FROM users WHERE id = {}".format(ctx.author.id))
        bal = cur.fetchone()[0]
        if bal < cash:
            await ctx.send(embed=discord.Embed(
                color=0xd75050,
                title="Ошибка",
                description="недостаточно средств"
            ).set_footer(
                text=f"Запрос от {ctx.author} • {dt.datetime.now().strftime('%d.%m.%Y,%H:%M:%S')}"
            )
            )
        elif cash < 100:
            await ctx.send(embed=discord.Embed(
                color=0xd75050,
                title="Ошибка",
                description="минимальная ставка 100"
            ).set_footer(
                text=f"Запрос от {ctx.author} • {dt.datetime.now().strftime('%d.%m.%Y,%H:%M:%S')}"
            )
            )
        elif shot > 5:
            await ctx.send(embed=discord.Embed(
                color=0xd75050,
                title="Ошибка",
                description="максимальное патрон игр 5"
            ).set_footer(
                text=f"Запрос от {ctx.author} • {dt.datetime.now().strftime('%d.%m.%Y,%H:%M:%S')}"
            )
            )
        else:
            chane = random.randint(1, 6)
            if shot == 1:
                shots = [1]
                win = cash // 100 * 5
            elif shot == 2:
                shots = [1, 2]
                win = cash // 100 * 25
            elif shot == 3:
                shots = [1, 2, 3]
                win = cash
            elif shot == 4:
                shots = [1, 2, 3, 4]
                win = cash * 2
            else:
                shots = [1, 2, 3, 4, 5]
                win = cash * 5

            if chane in shots:
                cur.execute("UPDATE users SET hands = hands - {} WHERE id = {}".format(cash, ctx.author.id))
                db.commit()
                emb = discord.Embed(title="ПРОИГРЫШ", color=0xd75050)
                for row in cur.execute("SELECT hands FROM users WHERE id = {}".format(ctx.author.id)):
                    emb.add_field(name=f"Вы проиграли: <:Money:984020799230988318> {cash}",
                                  value="Ваш баланс: {} <:Money:984020799230988318>".format((row[0])))
                emb.set_thumbnail(url='https://media.tenor.com/images/3f96a250ace5aeaddb9341fc2c4a858f/tenor.gif')
                emb.set_footer(text=f"{dt.datetime.now().strftime('%d.%b.%Y,%H:%M:%S')}")
                await ctx.send(embed=emb)
            else:
                cur.execute("UPDATE users SET hands = hands + {} WHERE id = {}".format(win, ctx.author.id))
                db.commit()
                emb = discord.Embed(title="ПОБЕДА", color=0x59d750)
                for row in cur.execute("SELECT hands FROM users WHERE id = {}".format(ctx.author.id)):
                    emb.add_field(name=f"Вы выиграли 5% от ставки <:Money:984020799230988318> {win}",
                                  value="Ваш баланс: {} <:Money:984020799230988318>".format((row[0])))
                emb.set_thumbnail(url='https://media.tenor.com/images/3f96a250ace5aeaddb9341fc2c4a858f/tenor.gif')
                emb.set_footer(text=f"{dt.datetime.now().strftime('%d.%b.%Y,%H:%M:%S')}")
                await ctx.send(embed=emb)

    @commands.command(aliases=['монетка'], help="Подкинь монеточку и, возможно выйграй приз")
    @commands.cooldown(1, (3), commands.BucketType.user)
    async def bf(self, ctx, cash: int, mon: str):
        author = ctx.message.author
        db = sqlite3.connect("databases/database.db")
        cur = db.cursor()
        cur.execute("SELECT hands FROM users WHERE id = {}".format(ctx.author.id))
        bal = cur.fetchone()[0]
        mon_list = ["h", "t"]
        if bal < cash:
            await ctx.send(embed=discord.Embed(
                color=0xd75050,
                title="Ошибка",
                description="недостаточно средств"
            ).set_footer(
                text=f"Запрос от {author} • {dt.datetime.now().strftime('%d.%m.%Y,%H:%M:%S')}"
            )
            )
        elif cash < 100 or cash > 1000000:
            await ctx.send(embed=discord.Embed(
                color=0xd75050,
                title="Ошибка",
                description="Минимальная ставка 100\nМаксимальная ставка 1000000"
            ).set_footer(
                text=f"Запрос от {author} • {dt.datetime.now().strftime('%d.%m.%Y,%H:%M:%S')}"
            )
            )
        elif not mon in mon_list:
            await ctx.send(embed=discord.Embed(
                color=0xd75050,
                title="Ошибка",
                description="`h` или `t`"
            ).set_footer(
                text=f"Запрос от {author} • {dt.datetime.now().strftime('%d.%m.%Y,%H:%M:%S')}"
            )
            )
        else:
            meaning = random.choice(mon_list)
            img = "none"
            win = cash // 2
            if meaning == "t":
                img = "https://nadeko-pictures.nyc3.digitaloceanspaces.com/other/coins/tails.png"
            else:
                img = "https://nadeko-pictures.nyc3.digitaloceanspaces.com/other/coins/heads.png"
            if mon == meaning:
                cur.execute("UPDATE users SET hands = hands + {} WHERE id = {}".format(win, ctx.author.id))
                db.commit()
                cur.execute("SELECT hands FROM users WHERE id = {}".format(ctx.author.id))
                bal = cur.fetchone()[0]
                await ctx.send(
                    embed=discord.Embed(
                        title="Вы выиграли!",
                        description=f"Поздравляю, вы выиграли {win} <:Money:984020799230988318>\nНа счету: {bal}<:Money:984020799230988318>"
                    ).set_image(
                        url=img
                    ).set_footer(
                        text=f"Запрос от {author} • {dt.datetime.now().strftime('%d.%m.%Y,%H:%M:%S')}"
                    )
                )
            else:
                cur.execute("UPDATE users SET hands = hands - {} WHERE id = {}".format(cash, ctx.author.id))
                db.commit()
                cur.execute("SELECT hands FROM users WHERE id = {}".format(ctx.author.id))
                bal = cur.fetchone()[0]
                await ctx.send(
                    embed=discord.Embed(
                        title="Вы проиграли",
                        description=f"Увы, вы проиграли {cash} <:Money:984020799230988318>\nНа счету: {bal}<:Money:984020799230988318>"
                    ).set_image(
                        url=img
                    ).set_footer(
                        text=f"Запрос от {author} • {dt.datetime.now().strftime('%d.%m.%Y,%H:%M:%S')}"
                    )
                )


def setup(client):
    client.add_cog(Game(client))
