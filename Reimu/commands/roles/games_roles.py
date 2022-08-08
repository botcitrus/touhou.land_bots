import discord
from discord.ext import commands
import sqlite3

connection = sqlite3.connect("databases/database.db")
cursor = connection.cursor()


class RoleSelect(discord.ui.View):

    def __init__(self, guild, bs, csgo, d2, lol, gen, valor):
        self.bs = bs
        self.csgo = csgo
        self.d2 = d2
        self.lol = lol
        self.gen = gen
        self.valor = valor
        self.guild = guild
        super().__init__(timeout=None)

    @discord.ui.select(placeholder='Выберите от 1 до 6 ролей', min_values=1, max_values=6, custom_id="a", options=[
        discord.SelectOption(label='Brawl Stars', emoji='<:987632362928107521:994495827777159168>'),
        discord.SelectOption(label='CS:GO', emoji='<:987632271479681025:994495826304970843>'),
        discord.SelectOption(label='Dota 2', emoji='<:987632164537532547:994495824685965332>'),
        discord.SelectOption(label='League Of Legends', emoji='<:987632393605234750:994495861704900608>'),
        discord.SelectOption(label='Genshin Impact', emoji='<:987632146283921408:994495860320772199>'),
        discord.SelectOption(label='Valorant', emoji='<:987632188973535302:994495858722746468>')
    ])
    async def select_callback(self, select, interaction):
        added_roles = []
        if 'Brawl Stars' in select.values:
            if self.bs in interaction.user.roles:
                await interaction.user.remove_roles(self.bs)
                added_roles.append(self.bs.name)
            else:
                await interaction.user.add_roles(self.bs)
                added_roles.append(self.bs.name)
        if 'CS:GO' in select.values:
            if self.csgo in interaction.user.roles:
                await interaction.user.remove_roles(self.csgo)
                added_roles.append(self.csgo.name)
            else:
                await interaction.user.add_roles(self.csgo)
                added_roles.append(self.csgo.name)
        if 'Dota 2' in select.values:
            if self.d2 in interaction.user.roles:
                await interaction.user.remove_roles(self.d2)
                added_roles.append(self.d2.name)
            else:
                await interaction.user.add_roles(self.d2)
                added_roles.append(self.d2.name)
        if 'League Of Legends' in select.values:
            if self.lol in interaction.user.roles:
                await interaction.user.remove_roles(self.lol)
                added_roles.append(self.lol.name)
            else:
                await interaction.user.add_roles(self.lol)
                added_roles.append(self.lol.name)
        if 'Genshin Impact' in select.values:
            if self.gen in interaction.user.roles:
                await interaction.user.remove_roles(self.gen)
                added_roles.append(self.gen.name)
            else:
                await interaction.user.add_roles(self.gen)
                added_roles.append(self.gen.name)
        if 'Valorant' in select.values:
            if self.valor in interaction.user.roles:
                await interaction.user.remove_roles(self.valor)
                added_roles.append(self.valor.name)
            else:
                await interaction.user.add_roles(self.valor)
                added_roles.append(self.valor.name)
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Игровые роли",
                description=f"Вам были добавлены/удалены роли:\n>>> " + '\n'.join(added_roles)
            ), ephemeral=True
        )
        added_roles.clear()


class Games_roles(commands.Cog):

    def __init__(self, client):
        self.client = client
        print('Commands {} is loaded'.format(self.__class__.__name__))

    @commands.command()
    async def games_roles(self, ctx):
        brawl_stars = discord.utils.get(ctx.guild.roles, id=1002618885108924486)
        csgo = discord.utils.get(ctx.guild.roles, id=866590159003582504)
        dota_2 = discord.utils.get(ctx.guild.roles, id=866589892582440980)
        lol = discord.utils.get(ctx.guild.roles, id=866600674946842625)
        genshin = discord.utils.get(ctx.guild.roles, id=866590322833621012)
        valorant = discord.utils.get(ctx.guild.roles, id=866590167073947659)

        await ctx.message.delete()

        await ctx.send(
            embed=discord.Embed(
                title="Под этим постом вы можете выбрать себе роль нажав на соответствующую кнопку в меню выбора ниже"
            ).add_field(
                name=" ⁣ ",
                value="**<:987632362928107521:994495827777159168> — Brawl Stars\n<:987632271479681025:994495826304970843> — CS:GO\n<:987632164537532547:994495824685965332> —Dota 2**"
            ).add_field(
                name=" ⁣ ",
                value="**<:987632393605234750:994495861704900608> — League Of Legends\n<:987632146283921408:994495860320772199> — Genshin Impact\n<:987632188973535302:994495858722746468> — Valorant**"
            ).set_image(
                url="https://cdn.discordapp.com/attachments/978647814483611668/994491329964933130/222.png"
            ).set_footer(
                text="Выбором в меню вы можете взять соответствующую смайлику роль.\nТак же повторным нажатием роль можно снять"
            ), view=RoleSelect(ctx.guild, brawl_stars, csgo, dota_2, lol, genshin, valorant)
        )

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.client.get_guild(795606016728760320)
        brawl_stars = discord.utils.get(guild.roles, id=1002618885108924486)
        csgo = discord.utils.get(guild.roles, id=866590159003582504)
        dota_2 = discord.utils.get(guild.roles, id=866589892582440980)
        lol = discord.utils.get(guild.roles, id=866600674946842625)
        genshin = discord.utils.get(guild.roles, id=866590322833621012)
        valorant = discord.utils.get(guild.roles, id=866590167073947659)
        self.client.add_view(RoleSelect(guild, brawl_stars, csgo, dota_2, lol, genshin, valorant))


def setup(client):
    client.add_cog(Games_roles(client))
