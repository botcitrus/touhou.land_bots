import discord
from discord.ext import commands


import sqlite3

import asyncio

db = sqlite3.connect("databases/database.db") 
cur = db.cursor()

class BuyButtons(discord.ui.Button):
    def __init__(self, label, inter, limit):
        super().__init__(label = label, style = discord.ButtonStyle.primary, emoji = "🛒",row = 0)
        self.inter = inter
        self.limit = limit
        self.label = label

    async def callback(self, interaction):
        if interaction.user == self.inter.author:
            const = cur.execute("SELECT const FROM shop WHERE _rowid_ = {}".format(self.label)).fetchone()[0]
            if const > cur.execute("SELECT hands FROM users WHERE id = {}".format(self.inter.author.id)).fetchone()[0]:
                await interaction.response.send_message(content = f"{self.inter.author.mention}", embed = discord.Embed(
                    title = "Покупка не совершилась",
                    description = "у вас не достаточно средств"
                ), ephemeral = True)
            else:
                role_id = cur.execute("SELECT role_id FROM shop WHERE _rowid_ = {}".format(self.label)).fetchone()[0]
                role = self.inter.guild.get_role(role_id)
                if role in self.inter.author.roles:
                    await interaction.response.send_message(content = f"{self.inter.author.mention}", embed = discord.Embed(
                        title = "Покупка не совершилась",
                        description = "у вас уже имеется данный лот"
                    ), ephemeral = True)
                else:
                    cur.execute("UPDATE users SET hands = hands - {} WHERE id = {}".format(const, self.inter.author.id))
                    cur.execute("UPDATE shop SET quantity = quantity + 1 WHERE _rowid_ = {}".format(self.label))
                    db.commit()
                    await self.inter.author.add_roles(role)
                    await interaction.response.edit_message(content = f"{self.inter.author.mention}",  embed = discord.Embed(
                        title = "Сделка совершена",
                        description = f"{self.inter.author.mention} купил слот под №{self.label} - {role.mention}"
                    ), view = None)
        
class Button_back(discord.ui.Button):
    def __init__(self, pages, inter, limit, current_page, sorting, sort, con_one):
        super().__init__(emoji="◀️", row = 2)
        self.pages = pages
        self.inter = inter
        self.limit = limit
        self.current_page = current_page
        self.sorting = sorting
        self.sort = sort
        self.con_one = con_one

    async def callback(self, interaction):
        if interaction.user == self.inter.author:
            self.current_page -= 1
            self.limit -= 5
            self.con_one = 0
            if self.current_page < 1:
                self.con_one = len(self.pages)*5-5
                self.current_page = len(self.pages)
                self.limit = len(self.pages)*5-5
            view = discord.ui.View()
            for x in cur.execute("SELECT id, role_id, const, quantity, _rowid_ FROM shop ORDER BY {} {} LIMIT {},5".format(self.sorting, self.sort, self.limit)):
                self.con_one += 1
                view.add_item(BuyButtons(str(self.con_one), self.inter, self.limit))

            view.add_item(Shop_select(self.inter))
            view.add_item(Button_back(self.pages, self.inter, self.limit, self.current_page, self.sorting, self.sort, self.con_one))
            view.add_item(Button_close(self.inter))
            view.add_item(Button_forward(self.pages, self.inter, self.limit, self.current_page, self.sorting, self.sort, self.con_one))

            await interaction.response.edit_message(content = f"{self.inter.author.mention}", embed = self.pages[self.current_page-1], view = view)

class Button_close(discord.ui.Button):
    def __init__(self, inter):
        super().__init__(emoji="🗑", row = 2)
        self.inter = inter

    async def callback(self, interaction):
        if interaction.user == self.inter.author:
            await interaction.response.defer()
            await interaction.edit_original_message(embed = discord.Embed(
                title = "Удаление сообщение..."
            ), view = None)
            await interaction.delete_original_message()

class Button_forward(discord.ui.Button):
    def __init__(self, pages, inter, limit, current_page, sorting, sort, con_one):
        super().__init__(emoji="▶️", row = 2)
        self.pages = pages
        self.inter = inter
        self.limit = limit
        self.current_page = current_page
        self.sorting = sorting
        self.sort = sort
        self.con_one = con_one

    async def callback(self, interaction):
        if interaction.user == self.inter.author:
            self.current_page += 1
            self.limit += 5
            if self.current_page > len(self.pages):
                self.current_page = 1
                self.con_one = 0
                self.limit = 0
                
            view = discord.ui.View()
            for x in cur.execute("SELECT id, role_id, const, quantity, _rowid_ FROM shop ORDER BY {} {} LIMIT {},5".format(self.sorting, self.sort, self.limit)):
                self.con_one += 1
                view.add_item(BuyButtons(label = str(self.con_one), inter = self.inter, limit = self.limit))
            
            view.add_item(Shop_select(self.inter))
            view.add_item(Button_back(self.pages, self.inter, self.limit, self.current_page, self.sorting, self.sort, self.con_one))
            view.add_item(Button_close(self.inter))
            view.add_item(Button_forward(self.pages, self.inter, self.limit, self.current_page, self.sorting, self.sort, self.con_one))
            
            await interaction.response.edit_message(content = f"{self.inter.author.mention}", embed = self.pages[self.current_page-1], view = view)

class Shop_select(discord.ui.Select):
    def __init__(self, inter):
        options = [
            discord.SelectOption(label='Сначала новые'),
            discord.SelectOption(label='Сначала старые'),
            discord.SelectOption(label='Сначала дорогие'),
            discord.SelectOption(label='Сначала дешевые'),
            discord.SelectOption(label='Сначала популярные')
        ]
        super().__init__(placeholder='Фильтр', min_values=1, max_values=1, options=options, row = 1)
        self.inter = inter


    async def callback(self, interaction):
        if interaction.user == self.inter.author:
            view = discord.ui.View()
            emb = discord.Embed(
                title = "Магазин ролей"
            )
            if self.values[0] == 'Сначала старые':
                sorting = '_rowid_'
                sort = 'DESC'
            elif self.values[0] == 'Сначала новые':
                sorting = '_rowid_'
                sort = 'ASC'
            elif self.values[0] == 'Сначала дорогие':
                sorting = 'const'
                sort = 'DESC'
            elif self.values[0] == 'Сначала дешевые':
                sorting = 'const'
                sort = 'ASC'
            else:
                sorting = 'quantity'
                sort = 'DESC'

            con_one = 0
            n = 0
            pages = []
            limit = 0
            for x in cur.execute("SELECT id, role_id, const, quantity, _rowid_ FROM shop ORDER BY {} {} LIMIT 5".format(sorting, sort)):
                con_one += 1
                view.add_item(BuyButtons(label = str(con_one), inter = self.inter, limit = limit))
                
            s = 0
            for x in cur.execute("SELECT id, role_id, const, quantity, _rowid_ FROM shop"):
                s += 1
            
            a = s//5
            if s%5 != 0:
                a += 1
            
            b = 0
            con_two = 0
            for x in cur.execute("SELECT id, role_id, const, quantity, _rowid_ FROM shop ORDER BY {} {}".format(sorting, sort)):
                con_two += 1
                n += 1 
                emb.add_field(
                    name = f" ⁣ ",
                    value = f"**{con_two}) {self.inter.guild.get_role(x[1]).mention} \nВладелец: <@{x[0]}> \nЦена: {x[2]} \nКуплена {x[3]} раз **",
                    inline = False
                )
                if n == 5:
                    b += 1
                    emb.set_thumbnail(url=self.inter.author.display_avatar)
                    emb.set_footer(text = f"Страница {b}/{a}")
                    pages.append(emb)
                    emb = discord.Embed(
                        title = "Магазин ролей"
                    )
                    n = 0
            
            if n < 5 and n != 0:
                emb.set_thumbnail(url=self.inter.author.display_avatar)
                emb.set_footer(text = f"Страница {b+1}/{a}")
                pages.append(emb)

            current_page = 1
            view.add_item(Shop_select(self.inter))
            view.add_item(Button_back(pages, self.inter, limit, current_page, sorting, sort, con_one))
            view.add_item(Button_close(self.inter))
            view.add_item(Button_forward(pages, self.inter, limit, current_page, sorting, sort, con_one))

            await interaction.response.edit_message(embed = pages[0], view = view)

class Shop(commands.Cog):
    
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        print('Commands {} is loaded'.format(self.__class__.__name__))
    
    @commands.command(aliases = ["магазин"])
    async def shop(self, inter):
        emb = discord.Embed(
            title = "Магазин ролей"
        )
        if cur.execute("SELECT * FROM shop").fetchone() == None:
            return await inter.send(
                embed = discord.Embed(
                    title = "На сервере отсутствуют роли",
                    color = 0x2f3136
                )
            )

        view = discord.ui.View()
        n = 0
        pages = []
        limit = 0
        sorting = '_rowid_'
        sort = 'ASC'
        con_one = 0
        for x in cur.execute("SELECT id, role_id, const, quantity, _rowid_ FROM shop ORDER BY {} {} LIMIT 5".format(sorting, sort)):
            con_one += 1
            view.add_item(BuyButtons(label = str(con_one), inter = inter, limit = limit))
        
        s = 0
        for x in cur.execute("SELECT id, role_id, const, quantity, _rowid_ FROM shop"):
            s += 1
        
        a = s//5
        if s%5 != 0:
            a += 1
        
        b = 0
        con_two = 0
        for x in cur.execute("SELECT id, role_id, const, quantity, _rowid_ FROM shop ORDER BY {} {}".format(sorting, sort)):
            n += 1 
            con_two += 1
            emb.add_field(
                name = f" ⁣ ",
                value = f"**{con_two}) {inter.guild.get_role(x[1]).mention} \nВладелец: <@{x[0]}> \nЦена: {x[2]} \nКуплена {x[3]} раз **",
                inline = False
            )
            if n == 5:
                b += 1
                emb.set_thumbnail(url=inter.author.display_avatar)
                emb.set_footer(text = f"Страница {b}/{a}")
                pages.append(emb)
                emb = discord.Embed(
                    title = "Магазин ролей"
                )
                n = 0
        
        if n < 5 and n != 0:
            emb.set_thumbnail(url=inter.author.display_avatar)
            emb.set_footer(text = f"Страница {b+1}/{a}")
            pages.append(emb)

        current_page = 1
        view.add_item(Shop_select(inter))
        view.add_item(Button_back(pages, inter, limit, current_page, sorting, sort, con_one))
        view.add_item(Button_close(inter))
        view.add_item(Button_forward(pages, inter, limit, current_page, sorting, sort, con_one ))
        await inter.send(content = f"{inter.author.mention}", embed = pages[0], view = view)

def setup(client):
    client.add_cog(Shop(client))







            

