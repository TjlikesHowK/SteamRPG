import math
import asyncio
import discord
import requests

from bs4 import BeautifulSoup
from discord.ext import commands

token = 'ODQwMTk1NzQ5MzA3MjE5OTk5.YJUrRA.mwIF6pZ8jSVKNe8dIG9rXMpY1JE'
prefix = '!'

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.198 (Edition Yx)'
}

descs = {
	'profile awards': 'Profile Awards',
	'badges': 'Badges',
	'games': 'Games',
	'reviews': 'Reviews'
}

bot = commands.Bot(command_prefix = prefix)

bot.remove_command('help')

async def get_html(url, params=''):
    html = requests.get(url, headers=headers, params=params)
    soup = BeautifulSoup(html.text, 'lxml')
    return soup

async def hiden(url):
	soup = await get_html(url)

	try:
		profile_hide = soup.find('div', class_='profile_private_info').get_text()

		return True
	except:
		return False

async def SI_act(url):
	soup = await get_html(url)

	bool_shit = [True, True, True, True]

	nick = soup.find('span', class_='actual_persona_name').get_text()
	lvl = soup.find('span', class_='friendPlayerLevelNum').get_text()
	adds_desc = soup.find_all('span', class_='count_link_label')
	adds = soup.find_all('span', class_='profile_count_link_total')
	img_url = soup.find('div', class_='playerAvatarAutoSizeInner').find_all('img')

	for i in range(len(adds)):
		if(adds_desc[i].get_text() == descs['profile awards'] and bool_shit[0]):
			pa = adds[i].get_text()
			bool_shit[0] = False
		elif(adds_desc[i] != descs['profile awards'] and bool_shit[0]):
			pa = '0'

		if(adds_desc[i].get_text() == descs['badges'] and bool_shit[1]):
			badges = adds[i].get_text()
			bool_shit[1] = False
		elif(adds_desc[i] != descs['badges'] and bool_shit[1]):
			badges = '0'

		if(adds_desc[i].get_text() == descs['games'] and bool_shit[2]):
			games = adds[i].get_text()
			bool_shit[2] = False
		elif(adds_desc[i] != descs['games'] and bool_shit[2]):
			games = '0'

		if(adds_desc[i].get_text() == descs['reviews'] and bool_shit[3]):
			reviews = adds[i].get_text()
			bool_shit[3] = False
		elif(adds_desc[i] != descs['reviews'] and bool_shit[3]):
			reviews = '0'

	if(len(img_url) == 2):
		img_url = img_url[1]['src']
	elif(len(img_url) == 1):
		img_url = img_url[0]['src']

	return nick, lvl, pa, badges, games, reviews, img_url

async def aid(perf):
	ids = []
	args = []

	with open('prof.txt', 'r') as f:
		lines = f.readlines()
		for line in lines:
			ids.append(line.strip().split()[0])
			args.append(line.strip().split()[1])

	if perf:
		return ids
	else:
		return ids, args

async def sort_uns(s, nn):
	a = s[1][nn]
	b = s[0][nn]

	for i in range(len(s[1])-1):
		for k in range(len(s[1]) - i):
			j = k + i

			if s[1][j] > s[1][i]:
				num_sort = s[1][i]
				str_sort = s[0][i]
				s[1][i] = s[1][j]
				s[0][i] = s[0][j]
				s[1][j] = num_sort
				s[0][j] = str_sort
	return s

async def rate():
	rpgs = [[],[]]

	ids, args = await aid(False)

	for i in range(len(ids)):
		if not await hiden(args[i]):
			nick, lvl, pa, badges, games, reviews, img_url = await SI_act(args[i])

			rpg_s = int(lvl) + int(pa.strip().replace(",", ""))*3 + int(badges.strip().replace(",", ""))*1.5 + int(games.strip().replace(",", ""))*0.5 + int(reviews.strip().replace(",", ""))*0.5
			rpg_l = math.floor(math.sqrt(rpg_s))

			rpgs[0].append(int(ids[i]))
			rpgs[1].append(rpg_l)

	res = await sort_uns(rpgs, 0)

	return res

async def lb_updating():
	while True:
		await asyncio.sleep(28800)
		res = await rate()
		text = ''
		for i in range(len(res[0])):
			if i < 10:
				text = text + f'{i+1}: ' + str(await bot.fetch_user(res[0][i])) + '-' + str(res[1][i]) + ' ур.\n'
			else:
				break
		with open('lb.txt', 'w', encoding='utf-8') as f:
			f.write(text)
		print('lb was updated!')

@bot.event
async def on_ready():
	print('We have logged in as {0.user}'.format(bot))
	print("I'm in " + str(len(bot.guilds)) + " servers")

	await bot.change_presence(status=discord.Status.online, activity=discord.Game("!Shelp - info about commands"))
	await lb_updating()

@bot.command(pass_context=True)
async def ASTC(ctx):
    await ctx.send("I'm in " + str(len(bot.guilds)) + " servers")

@bot.command()
async def Shelp(ctx):
	await ctx.send(
		'For the bot to work, you need to make your steam profile open to everyone. In the worst case, the bot will not be able to give you the level, at the best, it will give you the old one.\n\n'
		'***Attention!** When you start using SteamRPG-bot, you consent to the processing of your steam profile data open to all. The bot does not ask for or store your personal data, logins, passwords, etc.*\n\n'
	)

	description_text = (
		"For more information\n"
		"To register\n"
		"For re-registration\n"
		"To view your SteamRPG level\n\n"
		"To view some steam account information\n"
		"To view the top 10 registered users"
	)

	command_text = (
		"**!Shelp**\n"
		"**!SREG** *<link to steam-profile>*\n"
		"**!SREREG** *<link to steam-profile>*\n"
		"**!SRPG** *<link to steam-profile>* or nothing if you registered\n"
		"**!SINFO** *<link to steam-profile>* or nothing if you registered\n"
		"**!SRANK**"
	)

	embed = discord.Embed(
		title = 'Available commands',
		colour = discord.Colour.from_rgb(75, 0, 130)
	)
	embed.set_footer(text = f'Caused by: {ctx.author}', icon_url = ctx.author.avatar_url)
	embed.add_field(name = 'Commands', value = command_text, inline = True)
	embed.add_field(name = 'Description', value = description_text, inline = True)

	await ctx.send(embed = embed)

@bot.command()
async def SRPG(ctx, arg = None):
	if arg == None:
		ids, args = await aid(False)

		if str(ctx.author.id) in ids:
			index = ids.index(str(ctx.author.id))
			arg = args[index]
		else:
			await ctx.send('You must be registered to not enter the link')

	if not await hiden(arg):
		nick, lvl, pa, badges, games, reviews, img_url = await SI_act(arg)

		rpg_s = int(lvl) + int(pa.strip().replace(",", ""))*3 + int(badges.strip().replace(",", ""))*1.5 + int(games.strip().replace(",", ""))*0.5 + int(reviews.strip().replace(",", ""))*0.5
		rpg_l = math.floor(math.sqrt(rpg_s))

		embed = discord.Embed(
			title = nick,
			description = 
				'SteamRPG score: ' + str(rpg_s) + ' / ' + str((rpg_l+1)**2) + '\n'
				'SteamRPG level: ' + str(rpg_l) + '\n',
			colour = discord.Colour.from_rgb(75, 0, 130)
		)
		embed.set_thumbnail(url = img_url)
		embed.set_footer(text = f'Caused by: {ctx.author}', icon_url = ctx.author.avatar_url)

		await ctx.send(embed = embed)
	else:
		await ctx.send(await SI_act(arg))

@bot.command()
async def SINFO(ctx, arg = None):
	if arg == None:
		ids, args = await aid(False)
		if str(ctx.author.id) in ids:
			index = ids.index(str(ctx.author.id))
			arg = args[index]
		else:
			await ctx.send('You must be registered to not enter the link')

	if not await hiden(arg):
		nick, lvl, pa, badges, games, reviews, img_url = await SI_act(arg)

		embed = discord.Embed(
			title = nick,
			description = 
				'level: ' + lvl + '\n'
				'profile awards: ' + pa.strip() + '\n'
				'badges: ' + badges.strip() + '\n'
				'games: ' + games.strip() + '\n'
				'reviews: ' + reviews.strip() + '\n',
			colour = discord.Colour.from_rgb(75, 0, 130)
		)
		embed.set_thumbnail(url = img_url)
		embed.set_footer(text = f'Caused by: {ctx.author}', icon_url = ctx.author.avatar_url)

		await ctx.send(embed = embed)
	else:
		await ctx.send(await SI_act(arg))

@bot.command()
async def SREG(ctx, arg):
	ids = await aid(True)

	with open('prof.txt', 'a+') as f:
		if str(ctx.author.id) in ids:
			await ctx.send(str(ctx.author) + ' already registered!')
		else:
			f.writelines(str(ctx.author.id) + ' ' + arg + '\n')
			await ctx.send(str(ctx.author) + ' was registered!')

@bot.command()
async def SREREG(ctx, arg):
	ids, args = await aid(False)

	with open('prof.txt', 'a+') as f:
		with open('prof.txt', 'w') as f_m:
			f_m.write('')
		if str(ctx.author.id) in ids:
			index = ids.index(str(ctx.author.id))
			args[index] = arg
			for i in range(len(ids)):
				f.writelines(ids[i] + ' ' + args[i] + '\n')
			await ctx.send(str(ctx.author) + ' was re-registered')
		else:
			await ctx.send(str(ctx.author) + ' was never registered')

@bot.command()
async def SRANK(ctx):
	await ctx.send('Leaderboard updating every 8 hours!')

	nicks = ''
	levels = ''

	with open('lb.txt', 'r', encoding='utf-8') as f:
		text = f.readlines()

		for i in range(len(text)):
			colon = text[i].find(":")
			dash = text[i].find("-")
			point = text[i].find(".")

			nicks = nicks + text[i][:dash] + '\n'
			levels = levels + text[i][dash+1:point+1] + '\n'

	embed = discord.Embed(
		title = 'TOP 10 SteamRPG PLAYERS',
		colour = discord.Colour.from_rgb(75, 0, 130)
	)
	embed.add_field(name = 'player discord', value = nicks, inline = True)
	embed.add_field(name = 'level', value = levels, inline = True)
	embed.set_footer(text = f'Caused by: {ctx.author}', icon_url = ctx.author.avatar_url)

	await ctx.send(embed = embed)

bot.run(token)
