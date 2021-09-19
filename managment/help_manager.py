from typing import MutableMapping
from unicodedata import name
import discord
from discord.ext import commands
from discord.ext.commands.converter import clean_content

class CustomHelpCommand(commands.HelpCommand):
	"""i will murder you if you dont define the following on every command:

	name, usage*, description

	*:  you can skip this one
	"""
	async def send_bot_help(self, mapping): 
		ctx = self.context
		bot = ctx.bot
		prefix = self.clean_prefix

		command_list = []
		for cog in mapping:
			for command in mapping[cog]:
				command_list.append(f"`{prefix}{command.name}`")

		commands_avlbl = "\n".format(prefix).join(command_list)
		nl = "\n".format(prefix) #fuck you f-strings

		help_embd = discord.Embed(
		title=f"sara's bot", 
		description=f"{str(bot.description)}", 
		color=0xe3aec2
		)
		help_embd.set_thumbnail(url=bot.user.avatar_url)
		help_embd.add_field(name="commands available:", value=f"{nl}{str(commands_avlbl)}")
		help_embd.add_field(name="for more info type:", value=f"`{prefix}help <command>`", inline=False)
		help_embd.set_footer(text=f"ping: {round(bot.latency * 1000)}ms")
		
		await self.get_destination().send(embed=help_embd)

		
	async def send_cog_help(self, cog):
		await self.get_destination().send()

	async def send_group_help(self, group):
		prefix = self.clean_prefix
		group_cmds = "\n`{0}{1} ".format(prefix, group.name).join([command.name + "`" for idx, command in enumerate(group.commands)]) #please pay attention to the ` in "\n`{0}"
		nl = "\n`{0}{1} ".format(prefix, group.name) 
		grp_help_embd = discord.Embed(
			title=f"{group.name} help", 
			description=f"sub-commands available:{nl}{group_cmds}", 
			color=0xe3aec2
			)
		grp_help_embd.add_field(name="for help on subcommands type:", value=f"`{prefix}help {group.name} <sub-command>`")
		await self.get_destination().send(embed=grp_help_embd)

	async def send_command_help(self, command):
		prefix = self.clean_prefix
		cmd_help_embd = discord.Embed(
			title=f"{command} help", 
			description=f"{command.description}", 
			color=0xe3aec2
			)
		cmd_help_embd.add_field(name="usage:", value=f"`{prefix}{command.name}{'' if command.usage is None else ' ' + command.usage}`") #:feels:
		await self.get_destination().send(embed=cmd_help_embd)
