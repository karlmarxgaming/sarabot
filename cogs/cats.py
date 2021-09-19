from os import name, waitpid
import sqlite3
import discord
from discord.ext import commands
from managment.database_manager_thing import database

class cats_db(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(
        name="cats",
		description=(
			"cats database thing that MANIPULATES and databases\n"
		)
    )
    async def cats(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(self.cats)
    
    @cats.command(
        name="create",
		usage="<name>",
        description="cats"
    )
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def create(self, ctx, name: str):
        try:
            with database:
                database.execute(
                    "INSERT INTO cats (user, cat_name) VALUES (?, ?)", 
                    (ctx.author.id, name))

            print(f"{ctx.author.id}, be embraced, you {name}!")
            await ctx.send(f"{name} has been added into the database")

        except sqlite3.Error as e:
            print(e)
            await ctx.send(f"epic sqlfail: {e}")
        
    @cats.command(
        name="info"
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def info(self, ctx):
        print(f"{ctx.author.id} wants to know how many cats they have")
        try:
            with database:
                dbcats = database.execute(
                    "SELECT cat_name, sadness FROM cats WHERE user=:userid",
                    {"userid": ctx.author.id}).fetchmany(1024)
                cats = ", ".join([col['cat_name'] + " sadness: " + str(col['sadness']) for idx, col in enumerate(dbcats)])
                print(cats)

            if cats is None:
                await ctx.reply("you have no cats")
            else:
                await ctx.send(f"cats info {cats}")

        except sqlite3.Error as e:
            print(e)
            await ctx.send(f"epic sqlfail: {e}")
    
    @create.error
    async def create_OnError(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send_help(self.create)
            return
                
def setup(bot):
    bot.add_cog(cats_db(bot))
