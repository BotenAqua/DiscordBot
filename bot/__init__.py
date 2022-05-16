import discord
import os
from dotenv import load_dotenv
import yaml

load_dotenv()

if os.getenv('ENV') == 'Prod':
	token = os.getenv('PROD_TOKEN')
	print('Prod')
else:
	token = os.getenv('TEST_TOKEN')
	print('Test')

intents = discord.Intents.default()
intents.members = True


client = discord.Client(intents=intents)

with open('roles.yaml') as roles:
	reaction_dict = yaml.safe_load(roles)

@client.event
async def on_ready():
	print(f'{client.user} polaczyl sie z:')
	for guild in client.guilds:
		print(guild.id)
	return

@client.event
async def on_raw_reaction_add(payload):
	if payload.message_id in reaction_dict:
		if payload.emoji.name in reaction_dict[payload.message_id]:
			member = payload.member
			await member.add_roles(discord.utils.get(member.guild.roles, name='Testowa'))
		else:
			channel = client.get_channel(payload.channel_id)
			message = await channel.fetch_message(payload.message_id)
			user = client.get_user(payload.user_id)
			if payload.emoji.id:
				emoji = client.get_emoji(payload.emoji.id)
			else:
				emoji = payload.emoji
			await message.remove_reaction(emoji, user)
	return

@client.event
async def on_raw_reaction_remove(payload):
	if payload.message_id in reaction_dict:
		if payload.emoji.name in reaction_dict[payload.message_id]:
			member = client.get_guild(payload.guild_id).get_member(payload.user_id)
			await member.remove_roles(discord.utils.get(member.guild.roles, name='Testowa'))


client.run(token)
