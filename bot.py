#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Main Lib 

import disnake as sweetness 
from disnake.ext import commands

# Standart Import

from client import config

# Other Libs 

from os import listdir 


# Client

client = commands.Bot(
    command_prefix = commands.when_mentioned,
    help_command = None, 
    sync_commands_debug = True, 
    intents = sweetness.Intents.all()
)

# Other

async def get_stats():
    return {
        "guilds": len(client.guilds), 
        "users": len(set(client.get_all_members()))
    }

# Events 

@client.event 
async def on_ready():
    print("Ready")
    await get_stats()

# Loading Moderation

for filename in listdir('./client/commands/moderation/'):
    if filename.endswith('.py'):
        client.load_extension(f'client.commands.moderation.{filename[:-3]}')
        print(f"\033SweetNess \033COGS: \033[38;5;105m{filename[:-3]}\033has been loaded")
    else:
        if (filename != '__pycache__'):
            for file in listdir(f'./client/commands/moderation/{filename}/'):
                if file.endswith('.py'):
                    client.load_extension(f'client.commands.moderation.{filename}.{file[:-3]}')
                    print(f"\033SweetNess \033 COGS: \033{filename}.{file[:-3]}\033 has been loaded")

# Client Loading 

client.run(config.SWEETNESS["TOKEN"])