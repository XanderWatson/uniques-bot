from discord.ext import commands
import os
from dotenv import load_dotenv
import mongo_setup
from prefixes import Prefix

mongo_setup.global_init()

def get_prefix(client, message) -> Prefix:
    for pref in Prefix.objects:
        if pref._guild_id == str(message.guild.id):
            return pref._prefix

client = commands.Bot(command_prefix = get_prefix)

@client.event
async def on_ready():
    print("Uniques is ready for some development")
    client.load_extension('cogs.commands')
    client.load_extension('cogs.help')

@client.command()
async def load(ctx, extension):
    await client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    await client.unload_extension(f'cogs.{extension}')

@client.command()
async def reload(ctx, extension):
    await client.reload_extension(f'cogs.{extension}')

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
client.run(token)
