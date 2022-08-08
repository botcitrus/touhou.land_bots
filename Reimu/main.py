import asyncio

from config.settings import settings
from config.tables import tablecreate
from commands.help.helpcommand import *

client = commands.Bot(command_prefix='+', intents=discord.Intents.all(), help_command=MyHelp(), case_insensitive=True)


@client.event
async def on_ready():
    print(f"{client.user} запущен(а)")
    while True:
        try:
            await client.change_presence(
                activity=discord.Streaming(name="+help", value="UwU", url="https://www.twitch.tv/astolfo_oxo"))
            await asyncio.sleep(60)
            await client.change_presence(
                activity=discord.Streaming(name=f"{len(client.commands)} команд(а)", value="UwU",
                                           url="https://www.twitch.tv/astolfo_oxo"))
            await asyncio.sleep(60)
            await client.change_presence(
                activity=discord.Streaming(name=f"{len(set(client.get_all_members()))} участников", value="UwU",
                                           url="https://www.twitch.tv/astolfo_oxo"))
            await asyncio.sleep(60)
        except:
            continue


async def load_extension():
    for commands in settings['commands']:
        try:
            client.load_extension(commands)
        except Exception as e:
            print(f"Ошибка загрузки команд: {e}")

    for errors in settings['errors']:
        try:
            client.load_extension(errors)
        except Exception as e:
            print(f"Ошибка загрузки команд: {e}")

    for events in settings['events']:
        try:
            client.load_extension(events)
        except Exception as e:
            print(f"Ошибка загрузки событий: {e}")


async def main():
    await tablecreate()
    await load_extension()
    await client.start(settings["TOKEN"])


if __name__ == '__main__':
    client.loop.run_until_complete(main())
