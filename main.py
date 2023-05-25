import os
import discord
import requests
import json
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$cheese'):
        await CheeseCommand().execute(message)

class CheeseCommand:
    def __init__(self):
        self.url = 'https://cheese-api.onrender.com/random'

    async def execute(self, message):
        cheese_data = self.get_cheese_data()
        if cheese_data is not None:
            formatted_data = self.format_cheese_data(cheese_data)
            embed = discord.Embed(title='Cheese Information', description=formatted_data, color=0xFF5733)
            embed.set_thumbnail(url=cheese_data['image'])
            await message.channel.send(embed=embed)
        else:
            await message.channel.send('Error: Could not retrieve cheese data')

    def get_cheese_data(self):
        cheese_data = get_json_response(self.url)
        return cheese_data

    def format_cheese_data(self, cheese_data):
        name = cheese_data['name']
        description = cheese_data['description']
        milk = cheese_data['milk']

        formatted_data = f'**Name:** {name}\n\n**Description:** {description}\n\n**Milk:** {milk}'
        return formatted_data

def get_json_response(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

bot_token = os.getenv('DISCORD_BOT_TOKEN')
if bot_token is not None:
    client.run(bot_token)
