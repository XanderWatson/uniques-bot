import discord
from discord.ext import commands
import aiohttp
import random
from modules import ide
import mongo_setup
from prefixes import Prefix

mongo_setup.global_init()

def getprefix(msg) -> Prefix:
    for pref in Prefix.objects:
        if pref._guild_id == str(msg.guild.id):
            return pref._prefix

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild) -> Prefix:
        pref = Prefix()
        pref._guild_name = guild.name
        pref._guild_id = str(guild.id)
        pref._prefix = "unix "
        pref.save()
        
        channel = guild.system_channel
        if channel is not None:
            await channel.send(f"Hello! I'm Uniques! Thanks for inviting me to {guild.name}.")
            await channel.send("My default prefix is 'unix '.\nUse ```unix setprefix <prefix>``` to change the prefix.")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild) -> Prefix:
        Prefix.objects(_guild_id = str(guild.id)).delete()

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f"Hello {ctx.author.mention}! I'm Uniques, a bot to help you with all your programming needs!")

class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.content.split()[0] == "prefix":
            if msg.mentions[0] == self.bot.user:
                await msg.channel.send(f"My prefix is {getprefix(msg)}")

    @commands.command()
    async def setprefix(self, ctx, *, prefix) -> Prefix:
        for pref in Prefix.objects:
            if pref._guild_id == str(ctx.guild.id):
                pref._prefix = prefix
                pref.save()
        
        name = ctx.message.guild.get_member(self.bot.user.id).display_name
        p = name.split()[-1]

        if p[0] == '(' and p[-1] == ')':
            await ctx.message.guild.get_member(self.bot.user.id).edit(nick=f"{' '.join(name.split()[:-1])} ({prefix})")
        else:
            await ctx.message.guild.get_member(self.bot.user.id).edit(nick=f"{name} ({prefix})")

        await ctx.send("Prefix set to {}".format(prefix))

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"My ping time is: {round(self.bot.latency * 1000)} ms")
    
    @commands.command(aliases = ['c'])
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amount = 2):
        if amount == 0:
            await ctx.channel.purge()
        else:
            await ctx.channel.purge(limit = amount)

class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['git'])
    async def github(self, ctx):
        await ctx.send("https://github.com/XanderWatson/uniques-bot")

    @commands.command()
    async def ide(self, ctx):
        await ctx.send("Select ide mode (channel/dm):")
        ideMode = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
        ideMode = ideMode.content

        if ideMode == "channel":
            await ctx.send("Your ide mode is now set to channel.")
            await ctx.send("What should be the name of your code file (without extension)?")
            filename = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
            filename = filename.content

            while True:
                langlist = ["c", "c++", "cpp", "py", "python"]
                await ctx.send("Select a programming language: c, cpp/c++, python/py")
                language = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
                lang = language.content

                if lang in langlist:
                    break
                else:
                    await ctx.send("This programming language is either not recognized or not supported. Please try again.")

            ext = ""
            if lang == "python" or lang == "py":
                ext = "py"
            elif lang == "c":
                ext = "c"
            elif lang == "c++" or lang == "cpp":
                ext = "cpp"

            await ctx.send("Enter your code here (enclosed within three times '`'): ")
            msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
            if msg.content[0:3] == '```' and msg.content[len(msg.content) - 3:] == '```':
                code = msg.content[3:len(msg.content) - 3]
            
            await ctx.send("Type 'run' to run this code.")
            toRun = await self.bot.wait_for('message', check = lambda message: message.author == ctx.author)

            outputs = []
            if toRun.content == "run":
                outputs = ide.run(filename, ext, lang, code)
                await ctx.send(f"CompileError:\n{outputs[0]}")
                await ctx.send(f"Output:\n{outputs[1]}")
                await ctx.send(f"RuntimeError:\n{outputs[2]}")

        if ideMode == "dm":
            await ctx.send("Your ide mode is now set to dm.")
            await ctx.author.send("What should be the name of your code file (without extension)?")
            filename = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
            filename = filename.content

            while True:
                langlist = ["c", "c++", "cpp", "py", "python"]
                await ctx.author.send("Select a programming language: c, cpp/c++, python/py")
                language = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
                lang = language.content

                if lang in langlist:
                    break
                else:
                    await ctx.author.send("This programming language is either not recognized or not supported. Please try again.")

            ext = ""
            if lang == "python" or lang == "py":
                ext = "py"
            elif lang == "c":
                ext = "c"
            elif lang == "c++" or lang == "cpp":
                ext = "cpp"

            await ctx.author.send("Enter your code here (enclosed within three times '`'): ")
            msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
            if msg.content[0:3] == '```' and msg.content[len(msg.content) - 3:] == '```':
                code = msg.content[3:len(msg.content) - 3]
            
            await ctx.author.send("Type 'run' to run this code.")
            toRun = await self.bot.wait_for('message', check = lambda message: message.author == ctx.author)

            outputs = []
            if toRun.content == "run":
                outputs = ide.run(filename, ext, lang, code)
                await ctx.author.send(f"CompileError:\n`{outputs[0]}`")
                await ctx.author.send(f"Output:\n`{outputs[1]}`")
                await ctx.author.send(f"RuntimeError:\n`{outputs[2]}`")

    @commands.command(aliases = ['term'])
    async def terminal(self, ctx):
        await ctx.send("Welcome to Uniques Terminal!")

        while True:
            await ctx.send(f"{str(ctx.author).split('#')[0]}@Uniques:~$")
            comm = await self.bot.wait_for('message', check = lambda message: message.author == ctx.author)
            comm = comm.content

            if comm == "exit":
                await ctx.send("Exiting Uniques Terminal.")
                break
            else:
                from modules import terminal

                outputs = terminal.runCommand(comm.split())

                if outputs[0] != '':
                    if len(outputs[0]) > 2000:
                        j = 0
                        for i in range(len(outputs[0]) // 2000 + 1):
                            await ctx.send(f"Output:\n`{outputs[0][j:j + 1990]}`")
                            j += 1990
                    else:
                        await ctx.send(f"Output:\n`{outputs[0]}`")

                if outputs[1] != '':
                    await ctx.send(f"Error:\n`{outputs[1]}`")

    @commands.command(aliases = ['progmeme', 'pm'])
    async def meme(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://www.reddit.com/r/programmerhumour.json") as r:
                memes = await r.json()
                embed = discord.Embed(
                    color = discord.Color.blue(),
                )
                embed.set_image(url=memes["data"]["children"][random.randint(1, 25)]["data"]["url"])
                embed.set_footer(text=f"Meme requested by {ctx.author}")
                await ctx.send(embed=embed)
                
def setup(bot):
    bot.add_cog(Greetings(bot))
    bot.add_cog(Settings(bot))
    bot.add_cog(Developer(bot))
