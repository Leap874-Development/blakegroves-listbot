import discord
import json

with open('config.json', 'r') as f:
	config = json.load(f)

class ErrorEmbed(discord.Embed):
	def __init__(self, message):
		self.color = discord.Color.from_rgb(*config['embed_colors']['error'])
		self.message = message

		discord.Embed.__init__(self,
			color=self.color, title="An error occured",
			description=self.message )

class CommandErrorEmbed(discord.Embed):
	def __init__(self, err, ctx):
		self.color = discord.Color.from_rgb(*config['embed_colors']['error'])
		self.message = str(err)
		self.help = 'See %shelp %s' % (config['prefix'], ctx.command) 

		discord.Embed.__init__(self,
			color=self.color, title="Invalid command usage",
			description=self.message)
		self.set_footer(text=self.help)

class ListEmbed(discord.Embed):
	def __init__(self, list, bot):
		self.color = discord.Color.from_rgb(*config['embed_colors']['info'])
		self.list = list
		discord.Embed.__init__(self, color=self.color)

		content = ''
		for i,u in enumerate(self.list['data']):
			if u: user = bot.get_user(u).mention
			else: user = 'Empty'
			content += '%s) %s\n' % ((i+1), user)

			if (i + 1) % config['wrap_length'] == 0:
				if i <= config['wrap_length']: name = '**%s**' % self.list['name']
				else: name = '\u200b'
				self.add_field(name=name, value=content, inline=True)
				content = ''
		
		if len(self.list['data']) < config['wrap_length']:
			self.add_field(name='**%s**' % self.list['name'], value=content, inline=True)
		else:
			self.add_field(name='\u200b', value=content, inline=True)

class AllEmbed(discord.Embed):
	def __init__(self, all):
		self.color = discord.Color.from_rgb(*config['embed_colors']['info'])
		self.all = all
		self.content = ''
		self.help = 'See %shelp to get started' % config['prefix'] 

		for l in self.all:
			self.content += '`%s` (%s)\n' % (l['name'], len(l['data']))

		if len(self.all):
			discord.Embed.__init__(self, color=self.color)
			self.add_field(name='**All lists**', value=self.content)
		else:
			discord.Embed.__init__(self,
				color=self.color, title='No lists created')
			self.set_footer(text=self.help)

class SuccessEmbed(discord.Embed):
	def __init__(self, message):
		self.color = discord.Color.from_rgb(*config['embed_colors']['success'])
		self.message = message

		discord.Embed.__init__(self,
			color=self.color, title="Success",
			description=self.message)
