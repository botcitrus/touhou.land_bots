import discord
from discord.ext import commands
import sqlite3
from datetime import datetime

connection = sqlite3.connect('databases/database.db')
cursor = connection.cursor()

class YesorNo(discord.ui.View):
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
        cursor.execute("UPDATE users SET hands = hands - 2500 WHERE id = ?", [self.inter.author.id])
        cursor.execute("UPDATE users SET spouse = ? WHERE id = ?", [self.member.id, self.inter.author.id])
        cursor.execute("UPDATE users SET spouse = ? WHERE id = ?", [self.inter.author.id, self.member.id])

        overwritesVoice = {
            self.inter.guild.default_role: discord.PermissionOverwrite(connect=False),
            self.inter.author: discord.PermissionOverwrite(connect=True),
            self.member: discord.PermissionOverwrite(connect=True)
        }

        category = discord.utils.get(self.inter.guild.categories, id=988848767518257182)
        love_room = await self.inter.guild.create_voice_channel(f'{self.member.name}💗{self.inter.author.name}', category=category, overwrites=overwritesVoice)

        cursor.execute("INSERT INTO loveprofile VALUES (?, ?, ?, ?, ?, ?)", [marry_name, self.author.id, self.member.id, date, 0, 0, love_room.id])
        connection.commit()

        embed = discord.Embed(title='Заключить брак', description=f'Поздравляем, {self.member.mention} и {self.inter.author.mention} с заключением брака!\nСо счета {self.inter.author.mention} было списано **2500** <:money:961918415168217139>' , color=0x2f3136)
        embed.set_thumbnail(url=self.inter.author.display_avatar)
        await interaction.response.edit_message(embed=embed, view=None)

    @discord.ui.button(label="Отказать", style=discord.ButtonStyle.gray)
    async def no(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        embed = discord.Embed(title='Заключить брак', description=f'{self.inter.author.mention}, Вам отказали...', color=0x2f3136)
        embed.set_thumbnail(url=self.inter.author.display_avatar)
        await interaction.response.edit_message(embed=embed, view=None)
        

class Marry(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        print('Commands {} is loaded'.format(self.__class__.__name__))

    @commands.command(name='marry', description='Заключить брак')
    async def marry(self, inter, member: discord.Member):
        waifu_id = cursor.execute("SELECT spouse FROM users WHERE id = ?", [member.id]).fetchone()[0]

        if waifu_id is not None:
            print("1")
            embed = discord.Embed(title='Заключить брак', description=f'{inter.author.mention}, Вы уже состоите в браке', color=discord.Color.red())
            embed.set_thumbnail(url=inter.author.display_avatar)
            await inter.send(embed=embed)
        
        elif 2500 > cursor.execute("SELECT hands FROM users WHERE id = ?", [inter.author.id]).fetchone()[0]:
            print("2")
            embed = discord.Embed(title='Заключить брак', description=f'{inter.author.mention}, у Вас недостаточно <:money:961918415168217139>\nНеобходимо 2500 <:money:961918415168217139>', color=discord.Color.red())
            embed.set_thumbnail(url=inter.author.display_avatar)
            await inter.send(embed=embed)

        elif member == inter.author:
            print("3")
            embed = discord.Embed(title='Заключить брак', description=f'{inter.author.mention}, Вы не можете заключить брак с самим собой', color=discord.Color.red())
            embed.set_thumbnail(url=inter.author.display_avatar)
            await inter.send(embed=embed)

        else:
            print("4")
            embed = discord.Embed(title='Заключить брак', description=f'{inter.author.mention}, хочет заключить брак с {member.mention}, согласны ли вы?', color=0x2f3136)
            embed.set_thumbnail(url=inter.author.display_avatar)
            await inter.send(f'{member.mention}', embed=embed, view=YesorNo(inter, inter.author, member, inter.guild))


    
def setup(client):
    client.add_cog(Marry(client))

