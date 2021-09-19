import os
import sqlite3
import json
import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument
from managment.help_manager import CustomHelpCommand

if not os.path.exists("real_database.db3"):
    print("creating database")
    db = sqlite3.connect("real_database.db3")
    db.executescript(open("real_db_setup.sql", "r").read())

if os.path.exists("config.json"):
    with open("config.json", "r") as configfile:
        config = json.load(configfile)
        try:
            if config['token'] == "your token here":
                print("please enter your fucking token on the config file")
                quit()
            else:
                print("config loaded")
        except KeyError as error:
            print("hello where is {0} ????".format(error))
            quit()
else:
    with open("config.json", "w") as file_obj:
        data = {"token": "your token here"}
        json.dump(data, file_obj)
        print("generated config file bcs this is either the first time you run this or youre completely clueless and youre deleting random files which i think is not ok at all")
        quit()
    
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
    command_prefix='!',
    help_command=CustomHelpCommand(),
    intents=intents,
    description=("testing bot")
    )

@bot.event
async def on_ready():
    print(bot.user)

@bot.event
async def on_command_error(ctx, error):
    print(error)

for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension('cogs.' + file[:-3])

bot.run(config['token'], bot=True)