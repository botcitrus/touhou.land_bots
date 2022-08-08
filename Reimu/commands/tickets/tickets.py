from unicodedata import category
import discord
from discord.ext import commands
import sqlite3
from discord.ui import InputText, Modal
import asyncio

db = sqlite3.connect("databases/database.db")
cur = db.cursor()


class TicketAccepted(discord.ui.View):

    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label="Принято", custom_id="accepted", disabled=True)
    async def q_callback(self, button, interaction):
        pass


class QuestionAccepted(discord.ui.View):

    def __init__(self, bot, channel, question, memb):
        self.bot = bot
        self.channel = channel
        self.question = question
        self.memb = memb
        super().__init__(timeout=None)

    @discord.ui.button(label="Принять", style=discord.ButtonStyle.green, custom_id="acceptq")
    async def q_callback(self, button, interaction):
        embed = discord.Embed(
            title="Новый вопрос",
            description=f"Поступил вопрос от `{self.memb}`"
        ).add_field(
            name="Вопрос:",
            value=f"{self.question}"
        ).add_field(
            name="Принял:",
            value=f"{interaction.user.mention}"
        )
        ower = {interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True),
                self.memb: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True),
                self.memb.guild.default_role: discord.PermissionOverwrite(view_channel=False)}
        await self.channel.edit(overwrites=ower)
        await self.channel.send(f"> Вжуууух... Дикий {interaction.user.mention} приземлился!")
        await interaction.response.edit_message(embed=embed, view=TicketAccepted(self.bot))


class TicketAccept(discord.ui.View):

    def __init__(self, bot, category, channel, reason, object, memb):
        self.bot = bot
        self.category = category
        self.channel = channel
        self.reason = reason
        self.object = object
        self.memb = memb
        super().__init__(timeout=None)

    @discord.ui.button(label="Принять", style=discord.ButtonStyle.green, custom_id="accept")
    async def q_callback(self, button, interaction):
        embed = discord.Embed(
            title="Новая жалоба",
            description=f"Поступила жалоба на `{self.object}`"
        ).add_field(
            name=f"Жалобу отправил:",
            value=f"{interaction.user.mention}"
        ).add_field(
            name="Проблема (причина):",
            value=f"{self.reason}"
        ).add_field(
            name="Принял:",
            value=f"{interaction.user.mention}"
        )
        ower = {interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True),
                self.memb: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True),
                self.memb.guild.default_role: discord.PermissionOverwrite(view_channel=False)}
        await self.channel.edit(overwrites=ower)
        await self.channel.send(f"> Вжуууух... Дикий {interaction.user.mention} приземлился!")
        await interaction.response.edit_message(embed=embed, view=TicketAccepted(self.bot))


class DeleteTicket(discord.ui.View):

    def __init__(self, bot, category, channel):
        self.bot = bot
        self.category = category
        self.channel = channel
        super().__init__(timeout=None)

    @discord.ui.button(label="Закрыть", custom_id="close")
    async def m_callback(self, button, interaction):
        await interaction.response.send_message(
            embed=discord.Embed(
                description="обращение закроется через 5 сек..."
            )
        )
        await asyncio.sleep(5)
        await self.channel.delete()
        cur.execute("DELETE FROM createdtickets WHERE channel = {}".format(self.channel.id))
        db.commit()


class UserModal(Modal):

    def __init__(self, bot, category, channel_tickets):
        self.bot = bot
        self.category = category
        self.channel_tickets = channel_tickets
        super().__init__(title="Жалоба на пользователя")

        self.add_item(
            InputText(
                label="Пользователь",
                placeholder="parmesan#2017 | 666631626293510164",
                min_length=1,
                max_length=20,
                style=discord.InputTextStyle.singleline
            )
        )

        self.add_item(
            InputText(
                label="Жалоба",
                placeholder="Опишите проблему как можно подробнее...",
                min_length=1,
                max_length=300,
                style=discord.InputTextStyle.singleline
            )
        )

        self.add_item(
            InputText(
                label="Доказательства",
                placeholder="Ссылка... (не обязательно)",
                min_length=1,
                max_length=50,
                required=False,
                style=discord.InputTextStyle.singleline
            )
        )

    async def callback(self, interaction: discord.Interaction):
        ower = {interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True)}
        channel = await interaction.guild.create_text_channel(name=f"Жалоба от {interaction.user.name}",
                                                              category=self.bot.get_channel(self.category),
                                                              overwrites=ower)
        cur.execute("INSERT INTO createdtickets VALUES (?, ?)", [channel.id, interaction.user.id])
        db.commit()

        embed_accept = discord.Embed(
            title="Новая жалоба",
            description=f"Поступила жалоба на пользователя `{self.children[0].value}`"
        ).add_field(
            name=f"Жалобу отправил:",
            value=f"{interaction.user.mention}"
        ).add_field(
            name="Проблема (причина):",
            value=f"{self.children[1].value}"
        ).add_field(
            name="Принял:",
            value="Никто пока что не принял этот тикет"
        )

        if "http" in self.children[1].value:
            embed_accept.add_field(
                name="Доказалельства",
                value=f"[Нажмите для того что бы открыть изображение в браузере...]({self.children[1].value})",
                inline=False
            )
        else:
            embed_accept.add_field(
                name="Доказательства",
                value=f"Отсутствует"
            )

        embed_ticket = discord.Embed(
            title="Жалоба на ведущего",
            description=f"Была отправлена жалоба на пользователя `{self.children[0].value}`"
        ).add_field(
            name=f"Жалобу отправил:",
            value=f"{interaction.user.mention}"
        ).add_field(
            name="Проблема (причина):",
            value=f"{self.children[1].value}"
        )
        if "http" in self.children[1].value:
            embed_ticket.add_field(
                name="Доказалельства",
                value=f"[Нажмите для того что бы открыть изображение в браузере...]({self.children[1].value})",
                inline=False
            )
        else:
            embed_ticket.add_field(
                name="Доказательства",
                value=f"Отсутствует"
            )
        await interaction.response.send_message(
            embed=discord.Embed(
                description="Ваша жалоба отправлена, подождите пока я подберу администратора для её решения..."
            ), ephemeral=True
        )
        await self.channel_tickets.send(embed=embed_accept,
                                        view=TicketAccept(self.bot, category, channel, self.children[1].value,
                                                          self.children[0].value, interaction.user))
        await channel.send(f"{interaction.user.mention}", embed=embed_ticket,
                           view=DeleteTicket(self.bot, category, channel))


class ModeratorModal(Modal):

    def __init__(self, bot, category, channel_tickets):
        self.bot = bot
        self.category = category
        self.channel_tickets = channel_tickets
        super().__init__(title="Жалоба на модератора")

        self.add_item(
            InputText(
                label="Модератор",
                placeholder="parmesan#2017 | 666631626293510164",
                min_length=1,
                max_length=20,
                style=discord.InputTextStyle.singleline
            )
        )

        self.add_item(
            InputText(
                label="Жалоба",
                placeholder="Опишите проблему как можно подробнее...",
                min_length=1,
                max_length=300,
                style=discord.InputTextStyle.singleline
            )
        )

        self.add_item(
            InputText(
                label="Доказательства",
                placeholder="Ссылка... (не обязательно)",
                min_length=1,
                max_length=50,
                required=False,
                style=discord.InputTextStyle.singleline
            )
        )

    async def callback(self, interaction: discord.Interaction):
        ower = {interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True)}
        channel = await interaction.guild.create_text_channel(name=f"Жалоба от {interaction.user.name}",
                                                              category=self.bot.get_channel(self.category),
                                                              overwrites=ower)
        cur.execute("INSERT INTO createdtickets VALUES (?, ?)", [channel.id, interaction.user.id])
        db.commit()

        embed_accept = discord.Embed(
            title="Новая жалоба",
            description=f"Поступила жалоба на модератора `{self.children[0].value}`"
        ).add_field(
            name=f"Жалобу отправил:",
            value=f"{interaction.user.mention}"
        ).add_field(
            name="Проблема (причина):",
            value=f"{self.children[1].value}"
        ).add_field(
            name="Принял:",
            value="Никто пока что не принял этот тикет"
        )

        if "http" in self.children[1].value:
            embed_accept.add_field(
                name="Доказалельства",
                value=f"[Нажмите для того что бы открыть изображение в браузере...]({self.children[1].value})",
                inline=False
            )
        else:
            embed_accept.add_field(
                name="Доказательства",
                value=f"Отсутствует"
            )

        embed_ticket = discord.Embed(
            title="Жалоба на ведущего",
            description=f"Была отправлена жалоба на модератора `{self.children[0].value}`"
        ).add_field(
            name=f"Жалобу отправил:",
            value=f"{interaction.user.mention}"
        ).add_field(
            name="Проблема (причина):",
            value=f"{self.children[1].value}"
        )
        if "http" in self.children[1].value:
            embed_ticket.add_field(
                name="Доказалельства",
                value=f"[Нажмите для того что бы открыть изображение в браузере...]({self.children[1].value})",
                inline=False
            )
        else:
            embed_ticket.add_field(
                name="Доказательства",
                value=f"Отсутствует"
            )
        await interaction.response.send_message(
            embed=discord.Embed(
                description="Ваша жалоба отправлена, подождите пока я подберу администратора для её решения..."
            ), ephemeral=True
        )
        await self.channel_tickets.send(embed=embed_accept,
                                        view=TicketAccept(self.bot, category, channel, self.children[1].value,
                                                          self.children[0].value, interaction.user))
        await channel.send(f"{interaction.user.mention}", embed=embed_ticket,
                           view=DeleteTicket(self.bot, category, channel))


class EventerModal(Modal):

    def __init__(self, bot, category, channel_tickets):
        self.bot = bot
        self.category = category
        self.channel_tickets = channel_tickets
        super().__init__(title="Жалоба на ведущего")

        self.add_item(
            InputText(
                label="Ведущий",
                placeholder="parmesan#2017 | 666631626293510164",
                min_length=1,
                max_length=20,
                style=discord.InputTextStyle.singleline
            )
        )

        self.add_item(
            InputText(
                label="Жалоба",
                placeholder="Опишите проблему как можно подробнее...",
                min_length=1,
                max_length=300,
                style=discord.InputTextStyle.singleline
            )
        )

        self.add_item(
            InputText(
                label="Доказательства",
                placeholder="Ссылка... (не обязательно)",
                min_length=1,
                max_length=50,
                required=False,
                style=discord.InputTextStyle.singleline
            )
        )

    async def callback(self, interaction: discord.Interaction):
        ower = {interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True)}
        channel = await interaction.guild.create_text_channel(name=f"Жалоба от {interaction.user.name}",
                                                              category=self.bot.get_channel(self.category),
                                                              overwrites=ower)
        cur.execute("INSERT INTO createdtickets VALUES (?, ?)", [channel.id, interaction.user.id])
        db.commit()

        embed_accept = discord.Embed(
            title="Новая жалоба",
            description=f"Поступила жалоба на ведущего `{self.children[0].value}`"
        ).add_field(
            name=f"Жалобу отправил:",
            value=f"{interaction.user.mention}"
        ).add_field(
            name="Проблема (причина):",
            value=f"{self.children[1].value}"
        ).add_field(
            name="Принял:",
            value="Никто пока что не принял этот тикет"
        )

        if "http" in self.children[1].value:
            embed_accept.add_field(
                name="Доказалельства",
                value=f"[Нажмите для того что бы открыть изображение в браузере...]({self.children[1].value})",
                inline=False
            )
        else:
            embed_accept.add_field(
                name="Доказательства",
                value=f"Отсутствует"
            )

        embed_ticket = discord.Embed(
            title="Жалоба на ведущего",
            description=f"Была отправлена жалоба на ведущего `{self.children[0].value}`"
        ).add_field(
            name=f"Жалобу отправил:",
            value=f"{interaction.user.mention}"
        ).add_field(
            name="Проблема (причина):",
            value=f"{self.children[1].value}"
        )
        if "http" in self.children[1].value:
            embed_ticket.add_field(
                name="Доказалельства",
                value=f"[Нажмите для того что бы открыть изображение в браузере...]({self.children[1].value})",
                inline=False
            )
        else:
            embed_ticket.add_field(
                name="Доказательства",
                value=f"Отсутствует"
            )
        await interaction.response.send_message(
            embed=discord.Embed(
                description="Ваша жалоба отправлена, подождите пока я подберу администратора для её решения..."
            ), ephemeral=True
        )
        await self.channel_tickets.send(embed=embed_accept,
                                        view=TicketAccept(self.bot, category, channel, self.children[1].value,
                                                          self.children[0].value, interaction.user))
        await channel.send(f"{interaction.user.mention}", embed=embed_ticket,
                           view=DeleteTicket(self.bot, category, channel))


class QuestionModal(Modal):

    def __init__(self, bot, category, channel_tickets):
        self.bot = bot
        self.category = category
        self.channel_tickets = channel_tickets
        super().__init__(title="Задать вопрос")

        self.add_item(
            InputText(
                label="Ваш вопрос",
                placeholder="Я бы хотел поинтересоватся по поводу...",
                min_length=1,
                max_length=300,
                style=discord.InputTextStyle.long
            )
        )

    async def callback(self, interaction: discord.Interaction):
        ower = {interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True)}
        channel = await interaction.guild.create_text_channel(name=f"Вопрос от {interaction.user.name}",
                                                              category=self.bot.get_channel(self.category),
                                                              overwrites=ower)
        cur.execute("INSERT INTO createdtickets VALUES (?, ?)", [channel.id, interaction.user.id])
        db.commit()

        embed_accept = discord.Embed(
            title="Новый вопрос",
            description=f"Поступил вопрос от {interaction.user.mention}"
        ).add_field(
            name="Вопрос:",
            value=f"{self.children[0].value}"
        ).add_field(
            name="Принял:",
            value="Пока что никто не принял этот тикет"
        )

        embed_ticket = discord.Embed(
            title="Вопрос",
            description=f"Был задан новый вопрос"
        ).add_field(
            name="Вопрос от:",
            value=f"{interaction.user.mention}"
        ).add_field(
            name="Вопрос:",
            value=f"{self.children[0].value}"
        )
        await interaction.response.send_message(
            embed=discord.Embed(
                description="Ваша жалоба отправлена, подождите пока я подберу администратора для её решения..."
            ), ephemeral=True
        )
        await self.channel_tickets.send(embed=embed_accept,
                                        view=QuestionAccepted(self.bot, channel, self.children[0].value,
                                                              interaction.user))
        await channel.send(f"{interaction.user.mention}", embed=embed_ticket,
                           view=DeleteTicket(self.bot, category, channel))


class TicketButtons(discord.ui.View):

    def __init__(self, bot, category, channel_tickets):
        self.bot = bot
        self.category = category
        self.channel_tickets = channel_tickets
        super().__init__(timeout=None)

    @discord.ui.button(label="Пользователь", custom_id="user")
    async def a_callback(self, button, interaction):
        if cur.execute("SELECT id FROM createdtickets WHERE id = {}".format(interaction.user.id)).fetchone() is None:
            modal = UserModal(self.bot, self.category, self.channel_tickets)
            await interaction.response.send_modal(modal)
        else:
            await interaction.response.send_message(
                embed=discord.Embed(
                    description="У вас уже есть активный тикет"
                ), ephemeral=True
            )

    @discord.ui.button(label="Модератор", custom_id="moderator")
    async def b_callback(self, button, interaction):
        if cur.execute("SELECT id FROM createdtickets WHERE id = {}".format(interaction.user.id)).fetchone() is None:
            modal = ModeratorModal(self.bot, self.category, self.channel_tickets)
            await interaction.response.send_modal(modal)
        else:
            await interaction.response.send_message(
                embed=discord.Embed(
                    description="У вас уже есть активный тикет"
                ), ephemeral=True
            )

    @discord.ui.button(label="Ведущий", custom_id="eventer")
    async def c_callback(self, button, interaction):
        if cur.execute("SELECT id FROM createdtickets WHERE id = {}".format(interaction.user.id)).fetchone() is None:
            modal = EventerModal(self.bot, self.category, self.channel_tickets)
            await interaction.response.send_modal(modal)
        else:
            await interaction.response.send_message(
                embed=discord.Embed(
                    description="У вас уже есть активный тикет"
                ), ephemeral=True
            )

    @discord.ui.button(label="Вопрос", custom_id="question")
    async def d_callback(self, button, interaction):
        if cur.execute("SELECT id FROM createdtickets WHERE id = {}".format(interaction.user.id)).fetchone() is None:
            modal = QuestionModal(self.bot, self.category, self.channel_tickets)
            await interaction.response.send_modal(modal)
        else:
            await interaction.response.send_message(
                embed=discord.Embed(
                    description="У вас уже есть активный тикет"
                ), ephemeral=True
            )


class Tickets(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Commands {} is loaded'.format(self.__class__.__name__))

    @commands.command()
    async def ticket(self, ctx):
        channel_tickets = self.bot.get_channel(1002857811966951536)
        category = cur.execute("SELECT category FROM ticket").fetchone()[0]
        embed = discord.Embed(
            title="Выберите на кого вы хотите подать жалобу",
            description="В всплывающем окне опишите вашу ситуацию как можно точнее.\nВы можете прикрепить фото/видео доказательства после создания обращения.",
            color=0x00FF0F
        )
        await ctx.send(embed=embed, view=TicketButtons(self.bot, category, channel_tickets))

    @commands.Cog.listener()
    async def on_ready(self):
        category = cur.execute("SELECT category FROM ticket").fetchone()[0]
        channel_tickets = self.bot.get_channel(1002857811966951536)
        self.bot.add_view(TicketButtons(self.bot, category, channel_tickets))


def setup(client):
    client.add_cog(Tickets(client))
