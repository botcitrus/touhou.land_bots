import discord
from discord.ext import commands
from discord.ext.pages import PaginatorButton, Paginator, Page

import datetime


class HelpEmbed(discord.Embed):  # Our embed with some preset attributes to avoid setting it multiple times
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timestamp = datetime.datetime.now()
        self.set_thumbnail(url="https://i.pinimg.com/564x/3c/ee/31/3cee31f0feaa18705e4163d7d042c886.jpg")
        text = "Используйте `help [command]` или `help [category]` для большей информации \n| <> обязательный аргумент | [] опциональный"
        self.set_footer(text=text)
        self.color = 0xFFC0AF


class MyHelp(commands.MinimalHelpCommand):

    async def send_bot_help(self, commands):
        pages = [
            Page(
                embeds=[
                    discord.Embed(
                        title="Привет! Это мой хелп, здесь ты можешь посмотреть все мои команды",
                        description="Нажимай на кнопки ниже для перемещения по страницам",
                    ).add_field(
                        name="Небольшая справка",
                        value="Вы можете получить детальную справку по каждой группе или команде.\n**Используйте:**\nДля групп `+help <category>`\nДля команд `+help <command>`\n\n**Префикс бота на сервере:** `+`\n\n**Справка по аргументам:**\n\nОбязательный аргумент: `<>`\nНеобязательный аргумент`[]`\n\n**Здесь описаны только основные функции, вы можете так же узнать о функциях групп:**\n\n`Emoties`\n\n**Используйте:**\+help `<category>`"
                    ).set_image(
                        url="https://i.pinimg.com/originals/6f/83/5b/6f835b9ab80fffa78ce7db715f0b9f88.gif"
                    ).set_thumbnail(
                        url="https://i.pinimg.com/564x/3c/ee/31/3cee31f0feaa18705e4163d7d042c886.jpg"
                    )
                ],
            ),
            Page(
                embeds=[
                    discord.Embed(
                        title="Раздел комманд группы __**User's information**__",
                        description="На этой странице вы можете увидить команды группы __**User's information**__",
                    ).add_field(
                        name="+user",
                        value="Показывает детальную информацию о пользователе на платформе дискорд",
                        inline=False
                    ).add_field(
                        name="+profile",
                        value="Показывает серверную информацию об участнике",
                        inline=False
                    ).add_field(
                        name="+biography",
                        value="Устанавливает ваше описание в профиле",
                        inline=False
                    ).add_field(
                        name="+level",
                        value="Выдать пользователю определённый уровень",
                        inline=False
                    ).add_field(
                        name="+leaderboard",
                        value="Выводит таблицу лидеров по разделам",
                        inline=False
                    ).set_footer(
                        text="Используйте `help [command]` или `help [category]` для большей информации \n| <> обязательный аргумент | [] опциональный"
                    ).set_thumbnail(
                        url="https://i.pinimg.com/564x/3c/ee/31/3cee31f0feaa18705e4163d7d042c886.jpg"
                    )
                ],
            ),
            Page(
                embeds=[
                    discord.Embed(
                        title="Раздел комманд группы __**Moderation**__",
                        description="На этой странице вы можете увидеть все команды группы __**Moderation**__",
                    ).add_field(
                        name="+kick",
                        value="Выгнать пользователя с сервера",
                        inline=False
                    ).add_field(
                        name="+ban",
                        value="Забанить пользователя на сервере",
                        inline=False
                    ).add_field(
                        name="+unban",
                        value="Разбанить пользователя на сервере",
                        inline=False
                    ).add_field(
                        name="+mute",
                        value="Забрать право писать и говорить на n-ое количество времени",
                        inline=False
                    ).add_field(
                        name="+unmute",
                        value="Вернуть право писать и говорить пользователю",
                        inline=False
                    ).add_field(
                        name="+warn",
                        value="Выдать пользователю предупреждение на сервере",
                        inline=False
                    ).add_field(
                        name="+unwarn",
                        value="Снять предупреждение по номеру случая",
                        inline=False
                    ).add_field(
                        name="+warns",
                        value="Посмотреть варны пользователя",
                        inline=False
                    ).add_field(
                        name="+my_warns",
                        value="Посмотреть свои варны",
                        inline=False
                    ).add_field(
                        name="+clear",
                        value="Очитьстить n-ое количество сообщений",
                        inline=False
                    ).set_footer(
                        text="Используйте `help [command]` или `help [category]` для большей информации \n| <> обязательный аргумент | [] опциональный"
                    ).set_thumbnail(
                        url="https://i.pinimg.com/564x/3c/ee/31/3cee31f0feaa18705e4163d7d042c886.jpg"
                    )
                ],
            ),
            Page(
                embeds=[
                    discord.Embed(
                        title="Раздел комманд группы __**Economic**__",
                        description="На этой странице вы можете увидеть все команды группы __**Economic**__",
                    ).add_field(
                        name="+pay",
                        value="Перевести деньги участнику",
                        inline=False
                    ).add_field(
                        name="+withdout",
                        value="Вывести определённую сумму с банка",
                        inline=False
                    ).add_field(
                        name="+deposit",
                        value="Положить определённую сумму в банк",
                        inline=False
                    ).add_field(
                        name="+addmoney",
                        value="Выдать определённому пользователю n-ое колличество валюты (Право администратора)",
                        inline=False
                    ).add_field(
                        name="+shop",
                        value="Купить роль в магазине за определённую сумму",
                        inline=False
                    )
                    # .add_field(
                    #     name="+addlot",
                    #     value="Добавляет новый лот в магазин за определённую плату",
                    #     inline=False
                    # )
                    .add_field(
                        name="+work",
                        value="Заработать денег на работе",
                        inline=False
                    ).set_footer(
                        text="Используйте `help [command]` или `help [category]` для большей информации \n| <> обязательный аргумент | [] опциональный"
                    ).set_thumbnail(
                        url="https://i.pinimg.com/564x/3c/ee/31/3cee31f0feaa18705e4163d7d042c886.jpg"
                    )
                ],
            ),
            Page(
                embeds=[
                    discord.Embed(
                        title="Раздел комманд группы __**Games**__",
                        description="На этой странице вы можете увидеть все команды группы __**Games**__",
                    ).add_field(
                        name="+slots",
                        value="Испытай удачу в слотах, уйди со всем или проиграй всё",
                        inline=False
                    ).add_field(
                        name="+rulet",
                        value="Русская рулетка",
                        inline=False
                    ).add_field(
                        name="+bf",
                        value="Подкинь монеточку и, возможно выйграй приз",
                        inline=False
                    ).set_footer(
                        text="Используйте `help [command]` или `help [category]` для большей информации \n| <> обязательный аргумент | [] опциональный"
                    ).set_thumbnail(
                        url="https://i.pinimg.com/564x/3c/ee/31/3cee31f0feaa18705e4163d7d042c886.jpg"
                    )
                ],
            ),
            Page(
                embeds=[
                    discord.Embed(
                        title="Раздел комманд группы __**Family**__",
                        description="На этой странице вы можете увидеть все команды группы __**family**__",
                    ).add_field(
                        name="+marry",
                        value="Заключить брак с пользователем за 25000 <a:crystal:996045979084132382>",
                        inline=False
                    ).add_field(
                        name="+loveprofile",
                        value="Вывести профиль пары (пара может взоимодействовать с кнопками)",
                        inline=False
                    ).set_footer(
                        text="Используйте `help [command]` или `help [category]` для большей информации \n| <> обязательный аргумент | [] опциональный"
                    ).set_thumbnail(
                        url="https://i.pinimg.com/564x/3c/ee/31/3cee31f0feaa18705e4163d7d042c886.jpg"
                    )
                ],
            ),
        ]
        ctx = self.context
        buttons = [
            PaginatorButton("first", emoji="<:firstPage:1002272225023512736> ", style=discord.ButtonStyle.green),
            PaginatorButton("prev", emoji="<:previousPage:1002272197412405359> ", style=discord.ButtonStyle.green),
            PaginatorButton("page_indicator", style=discord.ButtonStyle.gray, disabled=True),
            PaginatorButton("next", emoji="<:nextPage:1002272325464494150> ", style=discord.ButtonStyle.green),
            PaginatorButton("last", emoji="<:lastPage:1002271989366538302>", style=discord.ButtonStyle.green),
        ]
        paginator = Paginator(
            pages=pages,
            show_disabled=True,
            show_indicator=True,
            use_default_buttons=False,
            custom_buttons=buttons,
            loop_pages=True
        )
        channel = self.get_destination()
        await paginator.send(ctx)

    async def send(self, **kwargs):
        await self.get_destination().send(**kwargs)

    async def send_help_embed(self, title, description, commands):
        embed = HelpEmbed(title=title, description=description or "Не найдено описание...")

        if filtered_commands := await self.filter_commands(commands):
            for command in filtered_commands:
                embed.add_field(name=self.get_command_signature(command),
                                value=f"{command.help}" or "Не найдено описание...", inline=False)

        await self.send(embed=embed)

    async def send_group_help(self, group):
        title = self.get_command_signature(group)
        await self.send_help_embed(title, group.help, group.commands)

    async def send_cog_help(self, cog):
        title = cog.qualified_name or "No"
        await self.send_help_embed(f'{title} Category', cog.description, cog.get_commands())

    async def send_command_help(self, command):
        embed = discord.Embed(title=f"Подробнее о команде: {command.name}")
        alias = command.aliases
        desc = command.description
        hel = command.help
        if hel:
            embed.add_field(name=command.name, value=command.help)
        else:
            embed.add_field(name=command.name, value="Мне ничего не известно об этой команде")
        if alias:
            embed.add_field(name="Псевдонимы", value=f'`{"`, `".join(alias)}`', inline=False)
        else:
            embed.add_field(name="Псевдонимы", value=f'Не могу найти больше псевдонимов этой команды', inline=False)
        if desc == "None":
            embed.add_field(name="Использование", value=f"+{command.name}")
        else:
            embed.add_field(name="Использование", value=f"{self.get_command_signature(command)}")

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_error_message(self, error):
        embed = discord.Embed(title="Ошибка", description=error)
        channel = self.get_destination()
        await channel.send(embed=embed)
