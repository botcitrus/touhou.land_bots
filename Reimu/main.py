import discord
from discord.ext import commands

from config.settings import settings

from config.tables import tablecreate

client = commands.Bot(command_prefix = 'reimu.', intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f"{client.user} запущен(а)")

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
    tablecreate()
    await load_extension()
    await client.start(settings["TOKEN"])

if __name__ == '__main__':
    client.loop.run_until_complete(main())
