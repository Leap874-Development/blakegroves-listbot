from discord.ext import commands
import json
import discord
import lists
import embeds

with open('config.json', 'r') as f:
	config = json.load(f)

with open('secrets.json', 'r') as f:
	secrets = json.load(f)

bot = commands.Bot(command_prefix=config['prefix'])

async def on_ready():
	guild_names = ', '.join([ a.name for a in bot.guilds ])
	print('ListBot online and logged in as %s' % bot.user)
	print('Connected to %s guild(s): %s' % (len(bot.guilds), guild_names))
	print('Now awaiting commands...')

async def on_command_error(ctx, err):
	await ctx.send(embed=embeds.CommandErrorEmbed(err, ctx))

@bot.command(name=config['commands']['new_list'], help='Creates new list')
@commands.has_permissions(administrator=True)
async def new_list(ctx, name : str, length : int):
	try:
		lists.new_list(name, length)
		await ctx.send(embed=embeds.SuccessEmbed('New list created'))
	except lists.ListExists:
		await ctx.send(embed=embeds.ErrorEmbed('List already exists'))
	except Exception as e:
		await ctx.send(embed=embeds.ErrorEmbed(e))

@bot.command(name=config['commands']['delete_list'], help='Deletes list')
@commands.has_permissions(administrator=True)
async def delete_list(ctx, name : str):
	try:
		lists.delete_list(name)
		await ctx.send(embed=embeds.SuccessEmbed('List deleted'))
	except lists.ListNotFound:
		await ctx.send(embed=embeds.ErrorEmbed('List does not exist'))
	except Exception as e:
		await ctx.send(embed=embeds.ErrorEmbed(e))

@bot.command(name=config['commands']['add_member'], help='Adds member to list')
@commands.has_permissions(administrator=True)
async def add_member(ctx, user : discord.Member, name : str, *posn : int):
	try:
		for p in posn:
			lists.add_member(name, user.id, p - 1)
		await ctx.send(embed=embeds.SuccessEmbed('Member added to list'))
	except lists.ListNotFound:
		await ctx.send(embed=embeds.ErrorEmbed('List does not exist'))
	except IndexError:
		await ctx.send(embed=embeds.ErrorEmbed('Position out of range'))
	except Exception as e:
		await ctx.send(embed=embeds.ErrorEmbed(e))

@bot.command(name=config['commands']['remove_member'], help='Removed member from list')
@commands.has_permissions(administrator=True)
async def remove_member(ctx, user : discord.Member, name : str):
	try:
		lists.remove_member(name, user.id)
		await ctx.send(embed=embeds.SuccessEmbed('Member removed from list'))
	except lists.ListNotFound:
		await ctx.send(embed=embeds.ErrorEmbed('List does not exist'))
	except Exception as e:
		await ctx.send(embed=embeds.ErrorEmbed(e))

@bot.command(name=config['commands']['clear_position'], help='Clears position in list')
@commands.has_permissions(administrator=True)
async def clear_position(ctx, name : str, posn : int):
	try:
		lists.clear_position(name, posn - 1)
		await ctx.send(embed=embeds.SuccessEmbed('Position cleared'))
	except lists.ListNotFound:
		await ctx.send(embed=embeds.ErrorEmbed('List does not exist'))
	except IndexError:
		await ctx.send(embed=embeds.ErrorEmbed('Position out of range'))
	except Exception as e:
		await ctx.send(embed=embeds.ErrorEmbed(e))

@bot.command(name=config['commands']['view_list'], help='Shows members in a list')
@commands.has_permissions(administrator=True)
async def view_list(ctx, name : str):
	try:
		lst = lists.get_list(name)
		await ctx.send(embed=embeds.ListEmbed(lst, bot))
	except lists.ListNotFound:
		await ctx.send(embed=embeds.ErrorEmbed('List does not exist'))
	except Exception as e:
		await ctx.send(embed=embeds.ErrorEmbed(e))

@bot.command(name=config['commands']['see_all'], help='Shows all lists')
@commands.has_permissions(administrator=True)
async def see_all(ctx):
	try:
		lsts = lists.see_all()
		await ctx.send(embed=embeds.AllEmbed(lsts))
	except Exception as e:
		await ctx.send(embed=embeds.ErrorEmbed(e))

bot.add_listener(on_ready)
bot.add_listener(on_command_error)
bot.run(secrets['token'])
