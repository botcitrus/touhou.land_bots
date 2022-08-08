import discord
from discord.ext import commands

from datetime import datetime

import sqlite3

connection = sqlite3.connect("databases/database.db")
cursor = connection.cursor()


class YesOrNo(discord.ui.View):
    def __init__(self, inter, author, member):
        super().__init__(timeout=None)

        self.inter = inter
        self.author = author
        self.member = member

    async def interaction_check(self, interaction):
        if interaction.user == self.member:
            return True
        else:
            return False

    @discord.ui.button(label="Согласиться", style=discord.ButtonStyle.gray)
    async def yes(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        marry_name = f"{self.author.display_name} & {self.member.display_name}"
        date = datetime.now().strftime('%d.%m.%Y')
        cursor.execute("UPDATE users SET hands = hands - 25000 WHERE id = ?", [self.inter.author.id])
        cursor.execute("UPDATE users SET spouse = ? WHERE id = ?", [self.member.id, self.inter.author.id])
        cursor.execute("UPDATE users SET spouse = ? WHERE id = ?", [self.inter.author.id, self.member.id])
        marryed = discord.utils.get(interaction.guild.roles, id=1003607227166376016)
        await self.author.add_roles(marryed)
        await self.member.add_roles(marryed)
        love_room = f"{self.member.name}💗{self.inter.author.name}"

        cursor.execute("INSERT INTO loveprofile VALUES (?, ?, ?, ?, ?, ?, ?)",
                       [marry_name, self.author.id, self.member.id, date, 0, 0, love_room])
        connection.commit()

        embed = discord.Embed(title='Заключить брак',
                              description=f'Поздравляем, {self.member.mention} и {self.inter.author.mention} с заключением брака!\nСо счета {self.inter.author.mention} было списано `2500` <a:crystal:996045979084132382>',
                              color=0x2f3136)
        embed.set_thumbnail(url=self.inter.author.display_avatar)
        await interaction.response.edit_message(embed=embed, view=None)

    @discord.ui.button(label="Отказать", style=discord.ButtonStyle.gray)
    async def no(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        embed = discord.Embed(title='Заключить брак', description=f'{self.inter.author.mention}, Вам отказали...',
                              color=0x2f3136)
        embed.set_thumbnail(url=self.inter.author.display_avatar)
        await interaction.response.edit_message(embed=embed, view=None)


class Back(discord.ui.View):

    def __init__(self, client, inter, first_member, second_member, member):
        super().__init__(timeout=None)

        self.client = client
        self.inter = inter
        self.first_member = first_member
        self.second_member = second_member
        self.member = member

    @discord.ui.button(label="Назад", style=discord.ButtonStyle.red)
    async def back(self, button: discord.ui.Button, interaction: discord.MessageInteraction):

        loveprofile_name = cursor.execute(
            "SELECT name FROM loveprofile WHERE first_member = {} OR second_member = {}".format(self.member.id,
                                                                                                self.member.id)).fetchone()[
            0]
        date = cursor.execute(
            "SELECT date FROM loveprofile WHERE first_member = {} OR second_member = {}".format(self.member.id,
                                                                                                self.member.id)).fetchone()[
            0]
        steamy_online = cursor.execute(
            "SELECT steamy_online FROM loveprofile WHERE  first_member = {} OR second_member = {}".format(
                self.member.id, self.member.id)).fetchone()[0]
        balance = cursor.execute(
            "SELECT balance FROM loveprofile WHERE first_member = {} OR second_member = {}".format(self.member.id,
                                                                                                   self.member.id)).fetchone()[
            0]

        if steamy_online == 0:
            online = "0 ч. 0 мин."
        else:
            online = f"{steamy_online // 3600} ч. {(steamy_online % 3600) // 60} мин."

        embed = discord.Embed(title=f"Любовный профиль —\n{loveprofile_name}", color=0x2f3136)
        embed.add_field(
            name="<:851538720519618590:991994861848899636> Пара",
            value=f"```{self.first_member} & {self.second_member}```",
            inline=False
        )
        embed.add_field(
            name="<:955671868080287824:991994860473163777> Дата",
            value=f"```{date}```",
            inline=True
        )
        embed.add_field(
            name="<:955671868189343814:991994859051290644>Парный онлайн",
            value=f"```{online}```",
            inline=True
        )
        embed.add_field(
            name="<:955671868063510548:991994857621049374> Баланс пары",
            value=f"```{balance}```",
            inline=True
        )
        embed.set_image(
            url="https://abrakadabra.fun/uploads/posts/2021-12/1640366192_11-abrakadabra-fun-p-parnie-oboi-na-planshet-13.png"
        )
        await interaction.response.edit_message(embed=embed,
                                                view=LoveButtons(self.client, self.inter, self.first_member,
                                                                 self.second_member, self.member))


class LoveButtons(discord.ui.View):
    def __init__(self, client, inter, first_member, second_member, member):
        super().__init__(timeout=None)

        self.client = client
        self.inter = inter
        self.first_member = first_member
        self.second_member = second_member
        self.member = member

    async def interaction_check(self, interaction):
        if interaction.user == self.first_member or interaction.user == self.second_member:
            return True
        else:
            return False

    @discord.ui.button(label="Развод", style=discord.ButtonStyle.red, emoji="<:851538720519618590:991994861848899636>")
    async def divorce(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        marryed = discord.utils.get(interaction.guild.roles, id=1003607227166376016)

        cursor.execute(
            "DELETE FROM loveprofile WHERE first_member = {} AND second_member = {}".format(self.first_member.id,
                                                                                            self.second_member.id))
        cursor.execute("UPDATE users SET spouse = NULL WHERE id = {}".format(self.first_member.id))
        cursor.execute("UPDATE users SET spouse = NULL WHERE id = {}".format(self.second_member.id))
        connection.commit()

        await self.first_member.remove_roles(marryed)
        await self.second_member.remove_roles(marryed)

        await interaction.response.edit_message(
            embed=discord.Embed(
                title="Развод",
                description=f"{self.first_member.mention} и {self.second_member.mention} развелись"
            ), view=None
        )

    @discord.ui.button(label="Поменять название", emoji="<:955671868189343814:991994859051290644>")
    async def rename(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        if cursor.execute("SELECT balance FROM loveprofile WHERE first_member = {} OR second_member = {}".format(
                interaction.user.id, interaction.user.id)).fetchone()[0] < 1500:
            embed = discord.Embed(
                title="Любовный канал",
                description="У вас недостаточно средств для изменения названия любовного канала <a:crystal:996045979084132382>",
            )
            embed.set_thumbnail(
                url=interaction.user.avatar
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                title="Любовный канал",
                description="Для того что бы сменить название любовного канала напишите название в чат",
            )
            embed.set_thumbnail(
                url=interaction.user.avatar
            )
            await interaction.response.edit_message(embed=embed, view=None)

            def check(m):
                return m.author == interaction.user and m.channel == interaction.channel

            msg = await self.client.wait_for('message', check=check)
            messg = '{.content}'.format(msg)
            await msg.delete()

            cursor.execute(
                "UPDATE loveprofile SET balance = balance - 1500 WHERE first_member = {} OR second_member = {}".format(
                    interaction.user.id, interaction.user.id))
            cursor.execute(
                "UPDATE loveprofile SET room = '{}' WHERE first_member = {} OR second_member = {}".format(messg,
                                                                                                          interaction.user.id,
                                                                                                          interaction.user.id))
            connection.commit()
            embed1 = discord.Embed(
                title="Любовный канал",
                description=f"Вы успешно сменили название любовного канала на `{messg}`"
            )
            await interaction.edit_original_message(embed=embed1, view=Back(self.client, self.inter, self.first_member,
                                                                            self.second_member, self.member))

    @discord.ui.button(label="Пополнить банк", style=discord.ButtonStyle.primary,
                       emoji="<:955671868063510548:991994857621049374>")
    async def addbalance(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        embed = discord.Embed(
            title="Пополнить банк",
            description="Для того что бы пополнить банк напишите сумму в чат <a:crystal:996045979084132382>",
        )
        embed.set_thumbnail(
            url=interaction.user.avatar
        )
        await interaction.response.edit_message(embed=embed, view=None)

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        msg = await self.client.wait_for('message', check=check)
        messg = '{.content}'.format(msg)
        await msg.delete()

        if int(messg) > cursor.execute("SELECT hands FROM users WHERE id = {}".format(interaction.user.id)).fetchone()[
            0]:
            embed = discord.Embed(
                title="Пополнить банк",
                description="У вас недостаточно средств для для пополнения банка на данную сумму",
            )
            embed.set_thumbnail(
                url=interaction.user.avatar
            )
            await interaction.edit_original_message(embed=embed, view=Back(self.client, self.inter, self.first_member,
                                                                           self.second_member, self.member))
        elif int(messg) < 0:
            embed = discord.Embed(
                title="Пополнить банк",
                description="Нельзя пополнить банк на сумму меньше нуля",
            )
            embed.set_thumbnail(
                url=interaction.user.avatar
            )
            await interaction.edit_original_message(embed=embed, view=Back(self.client, self.inter, self.first_member,
                                                                           self.second_member, self.member))
        else:
            cursor.execute(
                "UPDATE loveprofile SET balance = balance + {} WHERE first_member = {} OR second_member = {}".format(
                    messg, interaction.user.id, interaction.user.id))
            cursor.execute("UPDATE users SET hands = hands - {} WHERE id = {}".format(messg, interaction.user.id))
            connection.commit()

            embed1 = discord.Embed(
                title="Любовный канал",
                description=f"Вы успешно пополнили банк на `{messg}` <a:crystal:996045979084132382>"
            )
            await interaction.edit_original_message(embed=embed1, view=Back(self.client, self.inter, self.first_member,
                                                                            self.second_member, self.member))


class Family(commands.Cog, name="Family", description="Команды для отыгрывания небольшого РП с семьями"):

    def __init__(self, client):
        self.client = client
        print('Commands {} is loaded'.format(self.__class__.__name__))

    @commands.command(name='loveprofile', help="Вывести профиль пары (пара может взоимодействовать с кнопками)")
    async def loveprofile(self, inter, target: discord.Member = None):

        if target == None:
            member = inter.author
        else:
            member = target

        if cursor.execute("SELECT name FROM loveprofile WHERE first_member = {} OR second_member = {}".format(member.id,
                                                                                                              member.id)).fetchone() is None:
            embed = discord.Embed(
                title="Любовный профиль",
                description="Пользователь не состоит в браке",
                color=0x2f3136)
            await inter.send(embed=embed)
        else:
            loveprofile_name = cursor.execute(
                "SELECT name FROM loveprofile WHERE first_member = {} OR second_member = {}".format(member.id,
                                                                                                    member.id)).fetchone()[
                0]
            first = cursor.execute(
                "SELECT first_member FROM loveprofile WHERE first_member = {} OR second_member = {}".format(member.id,
                                                                                                            member.id)).fetchone()[
                0]
            second = cursor.execute(
                "SELECT second_member FROM loveprofile WHERE first_member = {} OR second_member = {}".format(member.id,
                                                                                                             member.id)).fetchone()[
                0]
            date = cursor.execute(
                "SELECT date FROM loveprofile WHERE first_member = {} OR second_member = {}".format(member.id,
                                                                                                    member.id)).fetchone()[
                0]
            steamy_online = cursor.execute(
                "SELECT steamy_online FROM loveprofile WHERE  first_member = {} OR second_member = {}".format(member.id,
                                                                                                              member.id)).fetchone()[
                0]
            balance = cursor.execute(
                "SELECT balance FROM loveprofile WHERE first_member = {} OR second_member = {}".format(member.id,
                                                                                                       member.id)).fetchone()[
                0]
            first_member = self.client.get_user(first)
            second_member = self.client.get_user(second)

            if steamy_online == 0:
                online = "В разработке"
            else:
                online = f"В разработке"

            embed = discord.Embed(title=f"Любовный профиль —\n{loveprofile_name}", color=0x2f3136)
            embed.add_field(
                name="<:851538720519618590:991994861848899636> Пара",
                value=f"```{first_member} & {second_member}```",
                inline=False
            )
            embed.add_field(
                name="<:955671868080287824:991994860473163777> Дата",
                value=f"```{date}```",
                inline=True
            )
            embed.add_field(
                name="<:955671868189343814:991994859051290644>Парный онлайн",
                value=f"```{online}```",
                inline=True
            )
            embed.add_field(
                name="<:955671868063510548:991994857621049374> Баланс пары",
                value=f"```{balance}```",
                inline=True
            )
            embed.set_image(
                url="https://abrakadabra.fun/uploads/posts/2021-12/1640366192_11-abrakadabra-fun-p-parnie-oboi-na-planshet-13.png"
            )
            if target is None:
                await inter.send(embed=embed, view=LoveButtons(self.client, inter, first_member, second_member, member))
            else:
                await inter.send(embed=embed)

    @commands.command(name='marry', help='Заключить брак с пользователем за 25000 <a:crystal:996045979084132382>')
    async def marry(self, inter, member: discord.Member):
        waifu_id = cursor.execute("SELECT spouse FROM users WHERE id = ?", [member.id]).fetchone()[0]

        if waifu_id is not None:
            embed = discord.Embed(title='Заключить брак',
                                  description=f'{inter.author.mention}, Вы уже состоите в браке',
                                  color=discord.Color.red())
            embed.set_thumbnail(url=inter.author.display_avatar)
            await inter.send(embed=embed)

        elif 25000 > cursor.execute("SELECT hands FROM users WHERE id = ?", [inter.author.id]).fetchone()[0]:
            embed = discord.Embed(title='Заключить брак',
                                  description=f'{inter.author.mention}, у Вас недостаточно <a:crystal:996045979084132382>\nНеобходимо 2500 <:money:961918415168217139>',
                                  color=discord.Color.red())
            embed.set_thumbnail(url=inter.author.display_avatar)
            await inter.send(embed=embed)

        elif member == inter.author:
            embed = discord.Embed(title='Заключить брак',
                                  description=f'{inter.author.mention}, Вы не можете заключить брак с самим собой',
                                  color=discord.Color.red())
            embed.set_thumbnail(url=inter.author.display_avatar)
            await inter.send(embed=embed)

        else:
            embed = discord.Embed(title='Заключить брак',
                                  description=f'{inter.author.mention}, хочет заключить брак с {member.mention}, согласны ли вы?',
                                  color=0x2f3136)
            embed.set_thumbnail(url=inter.author.display_avatar)
            await inter.send(f'{member.mention}', embed=embed, view=YesorNo(inter, inter.author, member))


def setup(client):
    client.add_cog(Family(client))
