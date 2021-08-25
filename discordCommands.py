import aiohttp
import json
import random
import discord

from datetime import datetime
from discord.ext import commands

DISCORD_TOKEN = ''
collection_address = ''

client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
    print(f'[{datetime.now().strftime("%H:%M:%S")}] {client.user} -- has connected to Discord!')

@client.command()
async def floor(ctx):
    try:
        async with aiohttp.ClientSession() as session:
            query_url = f'https://api.opensea.io/api/v1/asset/{collection_address}/100'
            async with session.get(query_url) as resp:
                response = await resp.text()
        data = json.loads(response)

        floor_price = round(float(data['collection']['stats']['floor_price']), 3)
        await ctx.channel.send(f'Opeansea floor is {floor_price}Ξ')
    except:
        pass

@client.command()
async def stats(ctx):
    try:
        async with aiohttp.ClientSession() as session:
            query_url = f'https://api.opensea.io/api/v1/asset/{collection_address}/100'
            async with session.get(query_url) as resp:
                response = await resp.text()
        data = json.loads(response)
    
        num_owners = data['collection']['stats']['num_owners']
        average_price = round(float(data['collection']['stats']['average_price']), 3)
        
        total_sale = round(float(data['collection']['stats']['total_sales']), 3)
        total_volume = round(float(data['collection']['stats']['total_volume']), 3)
        total_supply = data['collection']['stats']['total_supply']

        embed = discord.Embed(title=f'**Statistics**')
        embed.add_field(name='Owners', value=f'{num_owners}', inline=False)
        embed.add_field(name='Average price', value=f'{average_price}Ξ', inline=False)
        embed.add_field(name='Total supply', value=f'{total_supply}', inline=False)
        embed.add_field(name='Total sales', value=f'{total_sale}', inline=False)
        embed.add_field(name='Total volume', value=f'{total_volume}Ξ', inline=False)
        embed.set_footer(text='Type !totalstats for all statistics_')

        await ctx.channel.send(embed=embed)

    except Exception as e:
        pass

@client.command()
async def totalstats(ctx):
    try:
        async with aiohttp.ClientSession() as session:
            query_url = f'https://api.opensea.io/api/v1/asset/{collection_address}/100'
            async with session.get(query_url) as resp:
                response = await resp.text()
        data = json.loads(response)
    
        num_owners = data['collection']['stats']['num_owners']
        average_price = round(float(data['collection']['stats']['average_price']), 3)

        one_day_volume = round(float(data['collection']['stats']['one_day_volume']), 3)
        one_day_sales = data['collection']['stats']['one_day_sales']
        one_day_average_price = round(float(data['collection']['stats']['one_day_average_price']), 3)

        seven_day_volume = round(float(data['collection']['stats']['seven_day_volume']), 3)
        seven_day_sales = data['collection']['stats']['seven_day_sales']
        seven_day_average_price = round(float(data['collection']['stats']['seven_day_average_price']), 3)

        thirty_day_volume = round(float(data['collection']['stats']['thirty_day_volume']), 3)
        thirty_day_sales = data['collection']['stats']['thirty_day_sales']
        thirty_day_average_price = round(float(data['collection']['stats']['thirty_day_average_price']), 3)

        total_sale = round(float(data['collection']['stats']['total_sales']), 3)
        total_volume = round(float(data['collection']['stats']['total_volume']), 3)
        total_supply = data['collection']['stats']['total_supply']

        embed = discord.Embed(title=f'**Total Statistics**')
        embed.add_field(name='Owners', value=f'{num_owners}', inline=False)
        embed.add_field(name='Average price', value=f'{average_price}Ξ', inline=False)
        embed.add_field(name='Total supply', value=total_supply, inline=False)

        embed.add_field(name='One day volume', value=f'{one_day_volume}Ξ', inline=False)
        embed.add_field(name='One day sales', value=one_day_sales, inline=False)
        embed.add_field(name='One day average price', value=f'{one_day_average_price}Ξ', inline=False)

        embed.add_field(name='Seven day volume', value=f'{thirty_day_volume}Ξ', inline=False)
        embed.add_field(name='Seven day sales', value=seven_day_sales, inline=False)
        embed.add_field(name='Seven day average price', value=f'{seven_day_average_price}Ξ', inline=False)

        embed.add_field(name='Thirty day volume', value=f'{seven_day_volume}Ξ', inline=False)
        embed.add_field(name='Thirty day sales', value=thirty_day_sales, inline=False)
        embed.add_field(name='Thirty day average price', value=f'{thirty_day_average_price}Ξ', inline=False)

        embed.add_field(name='Total sales', value=total_sale, inline=False)
        embed.add_field(name='Total volume', value=f'{total_volume}Ξ', inline=False)
        embed.set_footer(text='Type !stats for brief statistics')

        await ctx.channel.send(embed=embed)

    except Exception as e:
        pass

@client.command()
async def asset(ctx, token_id):

    message = await ctx.channel.send(f'Processing asset #{token_id}...')

    try:
        async with aiohttp.ClientSession() as session:
            query_url = f'https://api.opensea.io/api/v1/asset/{collection_address}/{token_id}/'
            async with session.get(query_url) as resp:
                response = await resp.text()
                asset_data = json.loads(response)     

        asset_name = asset_data['name']
        asset_url = asset_data['image_url']
        asset_link = asset_data['permalink']
        asset_owner = asset_data['owner']['user']
        
        if asset_owner != None:
            asset_owner = asset_owner['username']

        trait_list = asset_data['traits']

        last_sale = asset_data['last_sale']
        if last_sale != None:
            payment_token = last_sale['payment_token']['symbol']
            last_sale = str(int(last_sale['total_price'])/1000000000000000000) + f' {payment_token}'

        random_color = random.randint(0, 0xffffff)

        embed = discord.Embed(title=f'{asset_name}', url=asset_link, color=random_color)
        embed.add_field(name='Owner', value=asset_owner, inline=False)
        embed.add_field(name='Last sale', value=last_sale, inline=False)
        embed.set_image(url=asset_url)

        for trait in trait_list:
            embed.add_field(name=trait['trait_type'], value=trait['value'])

        await message.edit(embed=embed, content=None)

    except Exception as e:
        print(f'[{datetime.now().strftime("%H:%M:%S")}] Error - {e}')
        await message.edit(content=f'Failed to process asset #{token_id}')

@client.command()
async def owners(ctx):
    try:
        async with aiohttp.ClientSession() as session:
            query_url = f'https://api.opensea.io/api/v1/asset/{collection_address}/100'
            async with session.get(query_url) as resp:
                response = await resp.text()
        data = json.loads(response)

        num_owners = data['collection']['stats']['num_owners']
        await ctx.channel.send(f'Total owners: **{num_owners}**')

    except:
        pass

client.run(DISCORD_TOKEN)
