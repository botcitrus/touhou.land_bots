import discord
from discord.ext import commands

import asyncio

import sqlite3

db = sqlite3.connect('databases/database.db')
cur = db.cursor()


class private_voice_buttons(discord.ui.View):

    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(emoji="<:owner_room:1005544046065881118>", row=0, custom_id="a")
    async def creator(self, button, interaction):
        try:
            channel = interaction.user.voice.channel

            if cur.execute(
                    "SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone() is None:
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=":x:  Ошибка",
                        description="У вас нет приватного домика"
                    ), ephemeral=True, view=None
                )
            else:
                if channel.id != cur.execute(
                        "SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone()[0]:
                    await interaction.response.send_message(
                        embed=discord.Embed(
                            title=":x:  Ошибка",
                            description="Это не ваш приватный домик"
                        ), ephemeral=True, view=None
                    )
                elif \
                        cur.execute(
                            "SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone()[
                            0] == channel.id:
                    await interaction.response.send_message(
                        embed=discord.Embed(
                            title="<:owner_room:1005544046065881118>   Смена создателя",
                            description="Для смены овнера домика отправте его тег в чат"
                        ), ephemeral=True, view=None
                    )

                    def check(m):
                        return len(m.mentions) != 0 and m.author == interaction.user

                    try:
                        msg = await self.bot.wait_for('message', timeout=15, check=check)
                        new_owner_id = msg.mentions[0].id
                        cur.execute(
                            "UPDATE private_voice SET id = {} WHERE channel = {}".format(new_owner_id, channel.id))
                        db.commit()
                    except asyncio.TimeoutError:
                        pass
                        return

        except:
            embed = discord.Embed(
                title=":x:  Ошибка",
                description="Вы не находитесь в голосовом канале"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True, view=None)

    @discord.ui.button(emoji="<:ban_room:1005544037073289236>", row=0, custom_id="b")
    async def ban(self, button, interaction):
        try:
            channel = interaction.user.voice.channel

            if cur.execute(
                    "SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone() is None:
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=":x:  Ошибка",
                        description="У вас нет приватного домика"
                    ), ephemeral=True, view=None
                )
            else:
                if channel.id != cur.execute(
                        "SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone()[0]:
                    await interaction.response.send_message(
                        embed=discord.Embed(
                            title=":x:  Ошибка",
                            description="Это не ваш приватный домик"
                        ), ephemeral=True, view=None
                    )
                elif \
                        cur.execute(
                            "SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone()[
                            0] == channel.id:
                    await interaction.response.send_message(
                        embed=discord.Embed(
                            title="<:ban_room:1005544037073289236> ограничить доступ к комнате",
                            description="Для ограничения доступа к домику отправте тег пользователя в чат"
                        ), ephemeral=True, view=None
                    )

                    def check(m):
                        return len(m.mentions) != 0 and m.author == interaction.user

                    try:

                        msg = await self.bot.wait_for('message', timeout=15, check=check)
                        ban_member = msg.mentions[0]
                        if channel.permissions_for(ban_member).connect != False:
                            await channel.set_permissions(ban_member, connect=False)
                            await ban_member.move_to(channel=None)
                        else:
                            await channel.set_permissions(ban_member, connect=True)
                    except asyncio.TimeoutError:
                        pass
                        return
                    except:
                        pass

        except TypeError:
            embed = discord.Embed(
                title=":x:  Ошибка",
                description="Вы не находитесь в голосовом канале"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True, view=None)

    @discord.ui.button(emoji="<:len_users:1005544043243114526>", row=0, custom_id="c")
    async def len(self, button, interaction):
        try:
            channel = interaction.user.voice.channel

            if cur.execute(
                    "SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone() is None:
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=":x:  Ошибка",
                        description="У вас нет приватного домика"
                    ), ephemeral=True, view=None
                )
            else:
                if channel.id != cur.execute(
                        "SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone()[0]:
                    await interaction.response.send_message(
                        embed=discord.Embed(
                            title=":x:  Ошибка",
                            description="Это не ваш приватный домик"
                        ), ephemeral=True, view=None
                    )
                elif \
                        cur.execute(
                            "SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone()[
                            0] == channel.id:
                    await interaction.response.send_message(
                        embed=discord.Embed(
                            title="<:len_users:1005544043243114526> назначить лимит комнаты",
                            description="Для назначения лимита участников отправьте число от 0 до 99"
                        ), ephemeral=True, view=None
                    )

                    def check(m):
                        return m.author == interaction.user and m.channel == interaction.channel

                    try:
                        msg = await self.bot.wait_for('message', timeout=15, check=check)
                        limit = int(msg.content)
                        await channel.edit(user_limit=limit)
                    except asyncio.TimeoutError:
                        pass
                        return
                    except:
                        pass

        except:
            embed = discord.Embed(
                title=":x:  Ошибка",
                description="Вы не находитесь в голосовом канале"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True, view=None)

    @discord.ui.button(emoji="<:close_room:1005544038209966122>", row=0, custom_id="d")
    async def close(self, button, interaction):
        try:
            channel = interaction.user.voice.channel

            if cur.execute(
                    "SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone() is None:
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=":x:  Ошибка",
                        description="У вас нет приватного домика"
                    ), ephemeral=True, view=None
                )
            else:
                if channel.id != cur.execute(
                        "SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone()[0]:
                    await interaction.response.send_message(
                        embed=discord.Embed(
                            title=":x:  Ошибка",
                            description="Это не ваш приватный домик"
                        ), ephemeral=True, view=None
                    )
                elif \
                        cur.execute(
                            "SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone()[
                            0] == channel.id:

                    role = discord.utils.get(interaction.guild.roles, id=795671578829652000)

                    if channel.permissions_for(role).connect != False:
                        await channel.set_permissions(role, connect=False)
                        await interaction.response.send_message(
                            embed=discord.Embed(
                                title="<:close_room:1005544038209966122> открыть/закрыть доступ к комнате",
                                description="Вы закрыли доступ к комнате"
                            ), ephemeral=True, view=None
                        )
                    else:
                        await channel.set_permissions(role, connect=True)
                        await interaction.response.send_message(
                            embed=discord.Embed(
                                title="<:blurplelock:1003612077908308092> открыть/закрыть доступ к комнате",
                                description="Вы открыли доступ к комнате"
                            ), ephemeral=True, view=None
                        )

        except:
            embed = discord.Embed(
                title=":x:  Ошибка",
                description="Вы не находитесь в голосовом канале"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True, view=None)

    @discord.ui.button(emoji="<:rename_room:1005544047424843806>", row=1, custom_id="e")
    async def rename(self, button, interaction):
        try:
            channel = interaction.user.voice.channel

            if cur.execute(
                    "SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone() is None:
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=":x:  Ошибка",
                        description="У вас нет приватного домика"
                    ), ephemeral=True, view=None
                )
            else:
                if channel.id != cur.execute(
                        "SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone()[0]:
                    await interaction.response.send_message(
                        embed=discord.Embed(
                            title=":x:  Ошибка",
                            description="Это не ваш приватный домик"
                        ), ephemeral=True, view=None
                    )
                elif \
                        cur.execute(
                            "SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone()[
                            0] == channel.id:
                    await interaction.response.send_message(
                        embed=discord.Embed(
                            title="<:rename_room:1005544047424843806> сменить название комнаты",
                            description="Введить новое название комнаты"
                        ), ephemeral=True, view=None
                    )

                    def check(m):
                        return m.author == interaction.user and m.channel == interaction.channel

                    try:
                        msg = await self.bot.wait_for('message', timeout=15, check=check)
                        name = msg.content
                        await channel.edit(name=name)
                    except asyncio.TimeoutError:
                        pass
                        return
                    except:
                        pass

        except:
            embed = discord.Embed(
                title=":x:  Ошибка",
                description="Вы не находитесь в голосовом канале"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True, view=None)

    @discord.ui.button(emoji="<:hide_room:1005544039883489301>", row=1, custom_id="f")
    async def view_room(self, button, interaction):
        try:
            channel = interaction.user.voice.channel

            if cur.execute(
                    "SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone() is None:
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=":x:  Ошибка",
                        description="У вас нет приватного домика"
                    ), ephemeral=True, view=None
                )
            else:
                if channel.id != cur.execute(
                        "SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone()[0]:
                    await interaction.response.send_message(
                        embed=discord.Embed(
                            title=":x:  Ошибка",
                            description="Это не ваш приватный домик"
                        ), ephemeral=True, view=None
                    )
                elif \
                        cur.execute(
                            "SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone()[
                            0] == channel.id:

                    role = discord.utils.get(interaction.guild.roles, id=795671578829652000)

                    if channel.permissions_for(role).view_channel != False:
                        await channel.set_permissions(role, view_channel=False)
                        await interaction.response.send_message(
                            embed=discord.Embed(
                                title="<:hide_room:1005544039883489301> скрыть/показать комнату",
                                description="Вы скрыли комнату"
                            ), ephemeral=True, view=None
                        )
                    else:
                        await channel.set_permissions(role, view_channel=True)
                        await interaction.response.send_message(
                            embed=discord.Embed(
                                title="<a:z_gawrgurashy:1003206331106340954>  скрыть/показать комнату",
                                description="Вашу комнату снова видно"
                            ), ephemeral=True, view=None
                        )

        except:
            embed = discord.Embed(
                title=":x:  Ошибка",
                description="Вы не находитесь в голосовом канале"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True, view=None)

    @discord.ui.button(emoji="<:kick_room:1005544041703809054>", row=1, custom_id="g")
    async def kick(self, button, interaction):
        try:
            channel = interaction.user.voice.channel

            if cur.execute(
                    "SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone() is None:
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=":x:  Ошибка",
                        description="У вас нет приватного домика"
                    ), ephemeral=True, view=None
                )
            else:
                if channel.id != cur.execute(
                        "SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone()[0]:
                    await interaction.response.send_message(
                        embed=discord.Embed(
                            title=":x:  Ошибка",
                            description="Это не ваш приватный домик"
                        ), ephemeral=True, view=None
                    )
                elif \
                        cur.execute(
                            "SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone()[
                            0] == channel.id:
                    await interaction.response.send_message(
                        embed=discord.Embed(
                            title="<:kick_room:1005544041703809054> выгнать участника из комнаты",
                            description="Для того что бы выгнать пользователя из домика отправте тег пользователя в чат"
                        ), ephemeral=True, view=None
                    )

                    def check(m):
                        return len(m.mentions) != 0 and m.author == interaction.user

                    try:

                        msg = await self.bot.wait_for('message', timeout=15, check=check)
                        kick_member = msg.mentions[0]
                        await kick_member.move_to(channel=None)
                    except asyncio.TimeoutError:
                        pass
                        return
                    except:
                        pass

        except:
            embed = discord.Embed(
                title=":x:  Ошибка",
                description="Вы не находитесь в голосовом канале"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True, view=None)

    @discord.ui.button(emoji="<:mute_room:1005544044606263346>", row=1, custom_id="h")
    async def mute(self, button, interaction):
        try:
            channel = interaction.user.voice.channel

            if cur.execute(
                    "SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone() is None:
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=":x:  Ошибка",
                        description="У вас нет приватного домика"
                    ), ephemeral=True, view=None
                )
            else:
                if channel.id != cur.execute(
                        "SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone()[0]:
                    await interaction.response.send_message(
                        embed=discord.Embed(
                            title=":x:  Ошибка",
                            description="Это не ваш приватный домик"
                        ), ephemeral=True, view=None
                    )
                elif \
                        cur.execute(
                            "SELECT channel FROM private_voice WHERE id = {}".format(interaction.user.id)).fetchone()[
                            0] == channel.id:
                    await interaction.response.send_message(
                        embed=discord.Embed(
                            title="<:mute_room:1005544044606263346> ограничить/выдать право говорить",
                            description="Для того что бы замутить/размутить пользователя в домикe отправте тег пользователя в чат"
                        ), ephemeral=True, view=None
                    )

                    def check(m):
                        return len(m.mentions) != 0 and m.author == interaction.user

                    try:

                        msg = await self.bot.wait_for('message', timeout=15, check=check)
                        mute_member = msg.mentions[0]
                        if channel.permissions_for(mute_member).speak != False:
                            await channel.set_permissions(mute_member, speak=False)
                        else:
                            await channel.set_permissions(mute_member, speak=True)
                    except asyncio.TimeoutError:
                        pass
                        return
                    except:
                        pass

        except:
            embed = discord.Embed(
                title=":x:  Ошибка",
                description="Вы не находитесь в голосовом канале"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True, view=None)


class Setting_private(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Commands {} is loaded'.format(self.__class__.__name__))

    @commands.command()
    @commands.has_any_role(977141423931523092)
    async def setting_voice(self, ctx):
        await ctx.message.delete()
        await ctx.send(embed=discord.Embed(
            title="Управление приватными комнатами",
            description='''Вы можете изменить конфигурацию своей комнаты с помощью взаимодействий.\n\n<:owner_room:1005544046065881118> — назначить нового создателя комнаты\n<:ban_room:1005544037073289236> — ограничить/выдать доступ к комнате\n<:len_users:1005544043243114526> — задать новый лимит участников\n<:close_room:1005544038209966122> — закрыть/открыть комнату\n<:rename_room:1005544047424843806> — изменить название комнаты\n<:hide_room:1005544039883489301> — скрыть/показать комнату\n<:kick_room:1005544041703809054> — выгнать участника из комнаты\n<:mute_room:1005544044606263346> — ограничить/выдать право говорить'''
        ).set_image(
            url="https://img3.akspic.ru/crops/2/3/6/9/4/149632/149632-noch-anime-atmosfera-vselennaya-kosmos-3840x2160.jpg"
        ), view=private_voice_buttons(self.bot)
        )

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(private_voice_buttons(self.bot))


def setup(client):
    client.add_cog(Setting_private(client))
