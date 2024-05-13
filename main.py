import os
import discord
from discord.ext import commands
import json
import re
import logging
import aiofiles
from flask import Flask
from home import home_blueprint  # Import the blueprint
# from threading import Thread
from multiprocessing import Process




# Configure logging
logging.basicConfig(level=logging.INFO)

# Load configuration from config.json asynchronously
async def load_config():
    async with aiofiles.open('config.json', 'r') as config_file:
        return json.loads(await config_file.read())

# Save configuration to config.json asynchronously
async def save_config(config):
    async with aiofiles.open('config.json', 'w') as config_file:
        await config_file.write(json.dumps(config, indent=4))

# Check if the message, user, or channel is exempt from link checks
async def is_exempt(message, config):
    return (
        str(message.channel.id) in config['exempt_channels'] or
        message.author.id == message.guild.owner_id or
        str(message.author.id) in config['exempt_users'] or
        any(role.id in config['exempt_roles'] for role in getattr(message.author, 'roles', []))
    )

# Regex pattern to detect Discord invite links
discord_invite_pattern = re.compile(
    r'(https?://|www\.|[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'  # Match the start of the URL
    r'[\w$-_@.&+!*\\(\\),%]*'  # Match the domain/path using \w for word characters
    r'(?:\.[a-zA-Z]{2,}|'  # Match the TLD
    r'(?:/[\w$-_@.&+!*\\(\\),%]{1,8})?|'  # Match the short path of a shortened URL
    r'(?:25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.'  # Start IP address
    r'(?:25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.'  # Middle IP address
    r'(?:25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.'  # Middle IP address
    r'(?:25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?))'  # End IP address
    r'(?:/[\w$-_@.&+!*\\(\\),%]*)?',  # Match the path with \w
    re.IGNORECASE
)


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!!", intents=intents)

class LinkCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='set')
    async def set_link(self, ctx, server_name, value):
        config = await load_config()
        config['servers'][server_name] = value
        await save_config(config)
        await ctx.send(f'Successfully set `{server_name}` link to: `{value}`')

    @commands.command(name='servers')
    async def list_servers(self, ctx):
        config = await load_config()
        server_names = list(config['servers'].keys())
        if server_names:
            server_names_str = '\n'.join(f'{index + 1}. `{name}`' for index, name in enumerate(server_names))
            await ctx.send(f"Servers names:\n{server_names_str}")
        else:
            await ctx.send("No servers names found.")

    @commands.command(name='server_L')
    async def show_all_server_links(self, ctx):
        config = await load_config()
        if config['servers']:
            for server_name, link in config['servers'].items():
                await ctx.send(f'`{server_name}` link: `{link}`')
        else:
            await ctx.send("No servers found.")

@bot.event
async def on_ready():
    logging.info(f'{bot.user} has connected')
    await bot.add_cog(LinkCommands(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    config = await load_config()

    if message.guild is not None and not await is_exempt(message, config):
        if discord_invite_pattern.search(message.content):
            await message.delete()
            await message.channel.send(f"{message.author.mention}, posting other Discord server links is not allowed!")
            return

    await bot.process_commands(message)

bot.remove_command('help')

@bot.command(name='help')
async def custom_help(ctx, *args):
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
#bot.run(os.environ["DISCORD_TOKEN"])

#TOKEN = os.environ["DISCORD_TOKEN"]

# def run_bot():
#     bot.run(os.environ["DISCORD_TOKEN"])
    
# # run web page
# # Create a function to run the Flask app
# # def run_app():
# #     app = Flask(__name__)
# #     app.register_blueprint(home_blueprint)  # Register the blueprint
# #     port = int(os.environ.get('PORT', 5000))
# #     app.run(host='0.0.0.0', port=port)


# # Run the Discord bot and Flask app in separate threads
# bot_thread = Thread(target=run_bot)
# # app_thread = Thread(target=run_app)
# bot_thread.start()
# # app_thread.start()

# Load token from environment variable
TOKEN = os.environ["DISCORD_TOKEN"]

# Create a function to run the Discord bot
def run_bot():
    bot.run(TOKEN)

# Create a function to run the Flask app
def run_app():
    app = Flask(__name__)
    app.register_blueprint(home_blueprint)  # Register the blueprint
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)

# Run the Discord bot and Flask app in separate processes
bot_process = Process(target=run_bot)
app_process = Process(target=run_app)
bot_process.start()
app_process.start()



