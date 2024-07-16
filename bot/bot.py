import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
from steamInfo import main
from chatgpt import aimodel

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

#All commands will start with the prefix '!'
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Simple in-memory storage for demonstration
stored_usernames = {}

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_guild_join(guild):
    """Sends a message to the server when the bot joins."""
    # Find the default channel and post the welcome message.
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send("Hello! I'm here to help you find game recommendations. Use `!commands` to see what commands you can use.")
            break

@bot.command()
async def help(ctx):
    """Displays a list of available commands."""
    embed = discord.Embed(title="About This Bot:", description="This bot is designed to help you find game recommendations based on your Steam data. It was created by Jared Immerman and Joshua Planovsky to enhance your gaming experience by suggesting games that you might enjoy.", color=discord.Color.blue())
    embed.add_field(name="Commands:", value="!reco: Asks for your Steam username and recommends games based on your data.\n\n!help: Displays this help message as well as a list of commands.")
    embed.add_field(name="How to Use:", value="To get started, simply type `!recommend` and follow the prompts. The bot will ask for your Steam username and then provide you with game recommendations. By using this bot, you agree to the terms of service.", inline=False)
    embed.add_field(name="Contact:", value="For any questions or feedback, feel free to contact Dominop or JimmJamm on Discord.", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def reco(ctx): 
    # Ask the user for a username
    await ctx.send("Please enter your Steam username:")

    # Wait for the user's response
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    #Handle time out error.     
    try:
        message = await bot.wait_for('message', check=check, timeout=30.0)
    except asyncio.TimeoutError:
        await ctx.send('Sorry, you took too long to respond.')
    #If user does not time out, store the username in temporary storage.
    else:
        steam_username = message.content

        # Store the received username in new Store_usernames dictionary
        stored_usernames[steam_username] = steam_username

        # Return the stored username to show we are storing it in the Store_usernames dictionary
        await ctx.send(f"Stored username: {steam_username}")

        # send username to steamInfo.py main()
        temp = main(steam_username)
    
        #formatting output to discord
        aioutput = aimodel(temp)
        embed = discord.Embed(title="Your game recommendation:", description=aioutput, color=discord.Color.blue())
        await ctx.send(embed=embed)
       
bot.run(TOKEN)