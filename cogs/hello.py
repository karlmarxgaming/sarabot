import discord
from discord.ext import commands

class hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="hello"
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hello(self, ctx):
        await ctx.reply("hi")

def setup(bot):
    bot.add_cog(hello(bot))