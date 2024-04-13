import os
import discord
from discord.ext import commands
import json
import re  # Import the regular expressions module

# Load configuration from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Ensure 'servers' key is present in config
if 'servers' not in config:
    config['servers'] = {}

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!!", intents=intents)

# Regex pattern to detect Discord invite links
discord_invite_pattern = re.compile(
    r'(discord\.(gg|io|me|li)|discord(app)?\.com/invite)/.+', re.IGNORECASE)

class LinkCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='set')
    async def set_link(self, ctx, server_name, value):
        """Set a custom link for a custom server name."""
        config['servers'][server_name] = value
        with open('config.json', 'w') as config_file:
            json.dump(config, config_file)
        await ctx.send(f'Successfully set `{server_name}` link to: `{value}`')

    @commands.command(name='servers')
    async def list_servers(self, ctx):
        """List all servers names."""
        server_names = list(config['servers'].keys())
        if server_names:
            server_names_str = '\n'.join(
                f'{index + 1}. `{name}`'
                for index, name in enumerate(server_names))
            await ctx.send(f"Servers names:\n{server_names_str}")
        else:
            await ctx.send("No servers names found.")

    @commands.command(name='server_L')
    async def show_all_server_links(self, ctx):
        """Show links for all servers."""
        if config['servers']:
            for server_name, link in config['servers'].items():
                await ctx.send(f'`{server_name}` link: `{link}`')
        else:
            await ctx.send("No servers found.")

@bot.event
async def on_ready():
    print(f'{bot.user} has connected')
    await bot.add_cog(LinkCommands(bot))  # Ensure the cog is awaited

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if discord_invite_pattern.search(message.content):
        await message.delete()
        await message.channel.send(
            f"{message.author.mention}, posting other Discord server links is not allowed!"
        )
    else:
        await bot.process_commands(message)

bot.remove_command('help')  # Remove the default help command

@bot.command(name='help')
async def custom_help(ctx, *args):
    """Custom help command."""
    if not args:
        help_message = (
            "Type `!!help command` for more info on a command.\n"
            "You can also type `!!set Name Link` to set server link.\n"
            "You can also type `!!servers` to list all server names.\n"
            "You can also type `!!server_L` to show links for all servers.\n"
            "You can also type `!!help category` for more info on a category.")
        await ctx.send(help_message)
    else:
        command = bot.get_command(args[0])
        if command:
            command_help = f"**{command.name}:** {command.help}"
            await ctx.send(command_help)
        else:
            await ctx.send("Command not found.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound) and ctx.message.content.startswith('!!'):
        return  # Ignore the error for custom servers names
    await ctx.send("Command not found.")

# Load token from environment variable
discord_token = "ODM2MjE5Njg4MTY0OTE3MzM4.GdkI8N.JDK3oX3rGvoDRGbLRU7mW4wdCioiN_oGqjPu00"

bot.run(discord_token)
