from pydoc import cli
import discord
from discord.ext import commands

from discord.ui import Button, View, Select

import asyncio

import sqlite3

db = sqlite3.connect('databases/database.db')
cur = db.cursor()

class private_voice_buttons(discord.ui.View):

    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout = None)

    @discord.ui.button(emoji = "<:funny_shiro:796803485701767209>", row = 0, custom_id="a")
    async def creator(self, button, interaction):
        try:
            channel = interaction.user.voice.channel

            if cur.execute("SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone() is None: 
                        await interaction.response.send_message(
                            embed = discord.Embed(
                                    title = ":x:  Ошибка",
                                    description = "У вас нет приватного домика"
                                ),ephemeral = True, view = None
                            )
            else:
                if channel.id != cur.execute("SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone()[0]:
                    await interaction.response.send_message(
                        embed = discord.Embed(
                                title = ":x:  Ошибка",
                                description = "Это не ваш приватный домик"
                            ),ephemeral = True, view = None
                        )
                elif cur.execute("SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone()[0] == channel.id:
                    await interaction.response.send_message(
                        embed = discord.Embed(
                            title = "<:0o0_senko:801313651192496158>  Смена создателя",
                            description = "Для смены овнера домика отправте его тег в чат"
                        ),ephemeral = True, view = None
                    )

                    def check(m):
                        return len(m.mentions) != 0 and m.author == interaction.user
                    
                    try:
                        msg = await self.bot.wait_for('message', timeout=15, check=check)
                        new_owner_id = msg.mentions[0].id
                        await msg.delete()
                        cur.execute("UPDATE private_voice SET id = {} WHERE channel = {}".format(new_owner_id, channel.id))
                        db.commit()
                    except asyncio.TimeoutError:
                        pass
                        return

        except:
            embed = discord.Embed(
                title  =":x:  Ошибка",
                description = "Вы не находитесь в голосовом канале"
            )
            await interaction.response.send_message(embed = embed, ephemeral = True, view = None)


    @discord.ui.button(emoji = "<:OoO_senko:801312054668820480>", row = 0, custom_id="b")
    async def ban(self, button, interaction):
        try:
            channel = interaction.user.voice.channel

            if cur.execute("SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone() is None: 
                        await interaction.response.send_message(
                            embed = discord.Embed(
                                    title = ":x:  Ошибка",
                                    description = "У вас нет приватного домика"
                                ),ephemeral = True, view = None
                            )
            else:
                if channel.id != cur.execute("SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone()[0]:
                    await interaction.response.send_message(
                        embed = discord.Embed(
                                title = ":x:  Ошибка",
                                description = "Это не ваш приватный домик"
                            ),ephemeral = True, view = None
                        )
                elif cur.execute("SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone()[0] == channel.id:
                    await interaction.response.send_message(
                        embed = discord.Embed(
                            title = "<:OoO_senko:801312054668820480> ограничить доступ к комнате",
                            description = "Для ограничения доступа к домику отправте тег пользователя в чат"
                        ),ephemeral = True, view = None
                    )

                    def check(m):
                        return len(m.mentions) != 0 and m.author == interaction.user
                    
                    try:

                        msg = await self.bot.wait_for('message', timeout=15, check=check)
                        ban_member = msg.mentions[0]
                        await msg.delete()
                        if channel.permissions_for(ban_member).connect != False:
                            await channel.set_permissions(ban_member, connect = False)
                            await ban_member.move_to(channel = None)
                        else:
                            await channel.set_permissions(ban_member, connect = True)
                    except asyncio.TimeoutError:
                        pass
                        return
                    except:
                        pass

        except:
            embed = discord.Embed(
                title  =":x:  Ошибка",
                description = "Вы не находитесь в голосовом канале"
            )
            await interaction.response.send_message(embed = embed, ephemeral = True, view = None)

    @discord.ui.button(emoji = "<:0o0_senko:801313651192496158>", row = 0, custom_id="c")
    async def len(self, button, interaction):
        try:
            channel = interaction.user.voice.channel

            if cur.execute("SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone() is None: 
                        await interaction.response.send_message(
                            embed = discord.Embed(
                                    title = ":x:  Ошибка",
                                    description = "У вас нет приватного домика"
                                ),ephemeral = True, view = None
                            )
            else:
                if channel.id != cur.execute("SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone()[0]:
                    await interaction.response.send_message(
                        embed = discord.Embed(
                                title = ":x:  Ошибка",
                                description = "Это не ваш приватный домик"
                            ),ephemeral = True, view = None
                        )
                elif cur.execute("SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone()[0] == channel.id:
                    await interaction.response.send_message(
                        embed = discord.Embed(
                            title = "<:0o0_senko:801313651192496158> назначить лимит комнаты",
                            description = "Для назначения лимита участников отправьте число от 0 до 99"
                        ),ephemeral = True, view = None
                    )

                    def check(m):
                        return m.author == interaction.user and m.channel == interaction.channel

                    try:
                        msg = await self.bot.wait_for('message', timeout=15, check=check)
                        await msg.delete()  
                        limit = int(msg.content)
                        await channel.edit(user_limit=limit)
                    except asyncio.TimeoutError:
                        pass
                        return
                    except:
                        pass

        except:
            embed = discord.Embed(
                title  =":x:  Ошибка",
                description = "Вы не находитесь в голосовом канале"
            )
            await interaction.response.send_message(embed = embed, ephemeral = True, view = None)

    @discord.ui.button(emoji = "<:stop:803261151060164639>", row = 0, custom_id="d")
    async def close(self, button, interaction):
        try:
            channel = interaction.user.voice.channel

            if cur.execute("SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone() is None: 
                        await interaction.response.send_message(
                            embed = discord.Embed(
                                    title = ":x:  Ошибка",
                                    description = "У вас нет приватного домика"
                                ),ephemeral = True, view = None
                            )
            else:
                if channel.id != cur.execute("SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone()[0]:
                    await interaction.response.send_message(
                        embed = discord.Embed(
                                title = ":x:  Ошибка",
                                description = "Это не ваш приватный домик"
                            ),ephemeral = True, view = None
                        )
                elif cur.execute("SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone()[0] == channel.id:

                    role = discord.utils.get(interaction.guild.roles, id = 795671578829652000)

                    if channel.permissions_for(role).connect != False:
                        await channel.set_permissions(role, connect = False)
                        await interaction.response.send_message(
                            embed = discord.Embed(
                                title = "<:stop:803261151060164639> открыть/закрыть доступ к комнате",
                                description = "Вы закрыли доступ к комнате"
                            ),ephemeral = True, view = None
                        )
                    else:
                        await channel.set_permissions(role, connect = True)
                        await interaction.response.send_message(
                            embed = discord.Embed(
                                title = "<:stop:803261151060164639> открыть/закрыть доступ к комнате",
                                description = "Вы открыли доступ к комнате"
                            ),ephemeral = True, view = None
                        )
                   
        except:
            embed = discord.Embed(
                title  =":x:  Ошибка",
                description = "Вы не находитесь в голосовом канале"
            )
            await interaction.response.send_message(embed = embed, ephemeral = True, view = None)

    @discord.ui.button(emoji = "<:UvU_senko:801316981516009482>", row = 1, custom_id="e")
    async def rename(self, button, interaction):
        try:
            channel = interaction.user.voice.channel

            if cur.execute("SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone() is None: 
                        await interaction.response.send_message(
                            embed = discord.Embed(
                                    title = ":x:  Ошибка",
                                    description = "У вас нет приватного домика"
                                ),ephemeral = True, view = None
                            )
            else:
                if channel.id != cur.execute("SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone()[0]:
                    await interaction.response.send_message(
                        embed = discord.Embed(
                                title = ":x:  Ошибка",
                                description = "Это не ваш приватный домик"
                            ),ephemeral = True, view = None
                        )
                elif cur.execute("SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone()[0] == channel.id:
                    await interaction.response.send_message(
                        embed = discord.Embed(
                            title = "<:UvU_senko:801316981516009482> сменить название комнаты",
                            description = "Введить новое название комнаты"
                        ),ephemeral = True, view = None
                    )

                    def check(m):
                        return m.author == interaction.user and m.channel == interaction.channel

                    try:
                        msg = await self.bot.wait_for('message', timeout=15, check=check)
                        await msg.delete()  
                        name = msg.content
                        await channel.edit(name = name)
                    except asyncio.TimeoutError:
                        pass
                        return
                    except:
                        pass

        except:
            embed = discord.Embed(
                title  =":x:  Ошибка",
                description = "Вы не находитесь в голосовом канале"
            )
            await interaction.response.send_message(embed = embed, ephemeral = True, view = None)

    @discord.ui.button(emoji = "<:no_2:803246050101035049>", row = 1, custom_id="f")
    async def view_room(self, button, interaction):
        try:
            channel = interaction.user.voice.channel

            if cur.execute("SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone() is None: 
                        await interaction.response.send_message(
                            embed = discord.Embed(
                                    title = ":x:  Ошибка",
                                    description = "У вас нет приватного домика"
                                ),ephemeral = True, view = None
                            )
            else:
                if channel.id != cur.execute("SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone()[0]:
                    await interaction.response.send_message(
                        embed = discord.Embed(
                                title = ":x:  Ошибка",
                                description = "Это не ваш приватный домик"
                            ),ephemeral = True, view = None
                        )
                elif cur.execute("SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone()[0] == channel.id:

                    role = discord.utils.get(interaction.guild.roles, id = 795671578829652000)

                    if channel.permissions_for(role).view_channel != False:
                        await channel.set_permissions(role, view_channel = False)
                        await interaction.response.send_message(
                            embed = discord.Embed(
                                title = "<:no_2:803246050101035049>  скрыть/показать комнату",
                                description = "Вы скрыли комнату"
                            ),ephemeral = True, view = None
                        )
                    else:
                        await channel.set_permissions(role, view_channel = True)
                        await interaction.response.send_message(
                            embed = discord.Embed(
                                title = "<:no_2:803246050101035049>  скрыть/показать комнату",
                                description = "Вашу комнату снова видно"
                            ),ephemeral = True, view = None
                        )

        except:
            embed = discord.Embed(
                title  =":x:  Ошибка",
                description = "Вы не находитесь в голосовом канале"
            )
            await interaction.response.send_message(embed = embed, ephemeral = True, view = None)

    @discord.ui.button(emoji = "<:pam:803261384715534396>", row = 1, custom_id="g")
    async def kick(self, button, interaction):
        try:
            channel = interaction.user.voice.channel

            if cur.execute("SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone() is None: 
                        await interaction.response.send_message(
                            embed = discord.Embed(
                                    title = ":x:  Ошибка",
                                    description = "У вас нет приватного домика"
                                ),ephemeral = True, view = None
                            )
            else:
                if channel.id != cur.execute("SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone()[0]:
                    await interaction.response.send_message(
                        embed = discord.Embed(
                                title = ":x:  Ошибка",
                                description = "Это не ваш приватный домик"
                            ),ephemeral = True, view = None
                        )
                elif cur.execute("SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone()[0] == channel.id:
                    await interaction.response.send_message(
                        embed = discord.Embed(
                            title = "<:pam:803261384715534396> выгнать участника из комнаты",
                            description = "Для того что бы выгнать пользователя из домика отправте тег пользователя в чат"
                        ),ephemeral = True, view = None
                    )

                    def check(m):
                        return len(m.mentions) != 0 and m.author == interaction.user
                    
                    try:

                        msg = await self.bot.wait_for('message', timeout=15, check=check)
                        kick_member = msg.mentions[0]
                        await msg.delete()                        
                        await kick_member.move_to(channel = None)
                    except asyncio.TimeoutError:
                        pass
                        return
                    except:
                        pass

        except:
            embed = discord.Embed(
                title  =":x:  Ошибка",
                description = "Вы не находитесь в голосовом канале"
            )
            await interaction.response.send_message(embed = embed, ephemeral = True, view = None)

    @discord.ui.button(emoji = "<:sad_senko:796803744406306826>", row = 1, custom_id="h")
    async def mute(self, button, interaction):
        try:
            channel = interaction.user.voice.channel

            if cur.execute("SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone() is None: 
                        await interaction.response.send_message(
                            embed = discord.Embed(
                                    title = ":x:  Ошибка",
                                    description = "У вас нет приватного домика"
                                ),ephemeral = True, view = None
                            )
            else:
                if channel.id != cur.execute("SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone()[0]:
                    await interaction.response.send_message(
                        embed = discord.Embed(
                                title = ":x:  Ошибка",
                                description = "Это не ваш приватный домик"
                            ),ephemeral = True, view = None
                        )
                elif cur.execute("SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone()[0] == channel.id:
                    await interaction.response.send_message(
                        embed = discord.Embed(
                            title = "<:sad_senko:796803744406306826> ограничить/выдать право говорить",
                            description = "Для того что бы замутить/размутить пользователя в домикe отправте тег пользователя в чат"
                        ),ephemeral = True, view = None
                    )

                    def check(m):
                        return len(m.mentions) != 0 and m.author == interaction.user
                    
                    try:

                        msg = await self.bot.wait_for('message', timeout=15, check=check)
                        mute_member = msg.mentions[0]
                        await msg.delete()
                        if channel.permissions_for(mute_member).speak != False:
                            await channel.set_permissions(mute_member, speak = False)
                        else:
                            await channel.set_permissions(mute_member, speak = True)
                    except asyncio.TimeoutError:
                        pass
                        return
                    except:
                        pass

        except:
            embed = discord.Embed(
                title  =":x:  Ошибка",
                description = "Вы не находитесь в голосовом канале"
            )
            await interaction.response.send_message(embed = embed, ephemeral = True, view = None)

class Setting_private(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Commands {} is loaded'.format(self.__class__.__name__))

    @commands.command()
    @commands.has_any_role(977141423931523092)
    async def setting_voice(self, ctx):
        await ctx.message.delete()
        await ctx.send(embed = discord.Embed(
            title = "Управление приватными комнатами",
            description = '''Вы можете изменить конфигурацию своей комнаты с помощью взаимодействий.
                                
                                <:funny_shiro:796803485701767209> — назначить нового создателя комнаты
                                <:OoO_senko:801312054668820480> — ограничить/выдать доступ к комнате
                                <:0o0_senko:801313651192496158> — задать новый лимит участников
                                <:stop:803261151060164639> — закрыть/открыть комнату
                                <:UvU_senko:801316981516009482> — изменить название комнаты
                                <:no_2:803246050101035049> — скрыть/показать комнату
                                <:pam:803261384715534396> — выгнать участника из комнаты
                                <:sad_senko:796803744406306826> — ограничить/выдать право говорить'''
            ).set_image(
                url = "https://img3.akspic.ru/crops/2/3/6/9/4/149632/149632-noch-anime-atmosfera-vselennaya-kosmos-3840x2160.jpg"
            ), view = private_voice_buttons(self.bot)
        )

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(private_voice_buttons(self.bot))

def setup(client):
    client.add_cog(Setting_private(client))