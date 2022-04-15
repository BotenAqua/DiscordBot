import discord
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.members = True


client = discord.Client(intents=intents)

reaction_dict = {963461119681388624:{}}

@client.event
async def on_ready():
	print(f'{client.user} polaczyl sie z:')
	for guild in client.guilds:
		print(guild.id)
	return

@client.event
async def on_raw_reaction_add(payload):
	if payload.message_id in reaction_dict:
		member = payload.member
		await member.add_roles(discord.utils.get(member.guild.roles, name='Testowa'))
	return

@client.event
async def on_raw_reaction_remove(payload):
	if payload.message_id in reaction_dict:
		member = client.get_guild(payload.guild_id).get_member(payload.user_id)
		await member.remove_roles(discord.utils.get(member.guild.roles, name='Testowa'))
	return

client.run(token)
