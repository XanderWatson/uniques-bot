import discord
from discord.ext import commands
from discord.errors import Forbidden
import mongo_setup
from prefixes import Prefix

mongo_setup.global_init()

async def send_embed(ctx, embed):
    try:
        await ctx.send(embed=embed)
    except Forbidden:
        try:
            await ctx.send("Hey, seems like I can't send embeds. Please check my permissions :)")
        except Forbidden:
            await ctx.author.send(
                f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                f"Please inform the server team about this issue :slight_smile: ",
                embed=embed
            )

# Getting the bot's prefix
def get_prefix(ctx) -> Prefix:
    for pref in Prefix.objects:
        if pref._guild_id == str(ctx.guild.id):
            return pref._prefix

class Help(commands.Cog):
    '''
        Contains the help command
    '''

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def help(self, ctx, *, query=""):
        '''
            Displays the help page

            Optional parameters: <module_name>
        '''
        prefix = get_prefix(ctx)

        query = query.split()

        if not query:
            emb = discord.Embed(
                title='Commands - Help\n',
                color=discord.Color.blue(),
                description=f'Use `{prefix}help <module>` to gain more information about that module\n'
            )

            cogs_desc = ""
            for cog in self.bot.cogs:
                cogs_desc += f'`{cog}` {self.bot.cogs[cog].__doc__}\n'

            emb.add_field(
                name='Modules\n',
                value=cogs_desc,
                inline=False
            )

            commands_desc = ''
            for command in self.bot.walk_commands():
                if not command.cog_name and not command.hidden:
                    commands_desc += f'\n`{command.name}`\n{command.help}\n'

            if commands_desc:
                emb.add_field(
                    name='General\n',
                    value=f'\n{commands_desc}\n',
                    inline=False
                )

            mention = "<@!824358672506814535>"
            emb.add_field(
                name="About",
                value=f"{mention} was created by {'<@!760781002833395732>'}\n"
            )

            emb.set_footer(
                text="This bot is licensed under the MIT License for Open-Source Software.")

        elif len(query) == 1:
            for cog in self.bot.cogs:
                if cog.lower() == query[0].lower():
                    emb = discord.Embed(
                        title=f'{cog} - Commands\n',
                        description=f'{self.bot.cogs[cog].__doc__}\n\n',
                        color=discord.Color.green()
                    )

                    for command in self.bot.get_cog(cog).get_commands():
                        if not command.hidden:
                            emb.add_field(
                                name=f"\n`{prefix}{command.name}`\n", value=f"{command.help}\n\n", inline=False)
                    break
            else:
                emb = discord.Embed(
                    title="What's that?!",
                    description=f"I've never heard from a module called `{query[0]}` before :scream:",
                    color=discord.Color.orange()
                )

        elif len(query) > 1:
            emb = discord.Embed(
                title="That's too much.",
                description="Please request only one module at once :sweat_smile:",
                color=discord.Color.orange()
            )

        else:
            emb = discord.Embed(
                title="It's a magical place.",
                description="I don't know how you got here. But I didn't see this coming at all.\n"
                "Would you please be so kind to report that issue to me on github?\n"
                "https://github.com/XanderWatson/uniques-bot/issues\n"
                "Thank you!",
                color=discord.Color.red()
            )

        await send_embed(ctx, emb)


def setup(bot):
    bot.add_cog(Help(bot))
