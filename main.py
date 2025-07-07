import discord
from discord.ext import commands
import random
import os
import asyncio
from datetime import datetime, timedelta
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix='uwu ', intents=intents)

user_data = {}
keep_alive()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# --- Economy Commands ---
@bot.command()
async def bal(ctx):
    user_id = str(ctx.author.id)
    coins = user_data.get(user_id, {}).get('coins', 0)
    await ctx.send(f'{ctx.author.mention} you have {coins} coins!')

@bot.command()
async def cf(ctx, amount: int):
    user_id = str(ctx.author.id)
    if user_id not in user_data or user_data[user_id]['coins'] < amount:
        await ctx.send(f'{ctx.author.mention} you don\'t have enough coins!')
        return
    result = random.choice(['heads', 'tails'])
    if random.choice(['heads', 'tails']) == result:
        user_data[user_id]['coins'] += amount
        await ctx.send(f'{ctx.author.mention} won {amount} coins! Total coins: {user_data[user_id]["coins"]}')
    else:
        user_data[user_id]['coins'] -= amount
        await ctx.send(f'{ctx.author.mention} lost {amount} coins! Total coins: {user_data[user_id]["coins"]}')

@bot.command()
async def bj(ctx, amount: int):
    await ctx.send(f'{ctx.author.mention} blackjack is coming soon!')

@bot.command()
async def blackjack(ctx, amount: int):
    await bj(ctx, amount)

@bot.command()
async def slot(ctx, amount: int):
    user_id = str(ctx.author.id)
    if user_id not in user_data or user_data[user_id]['coins'] < amount:
        await ctx.send(f'{ctx.author.mention} you don\'t have enough coins!')
        return
    symbols = ["🍒", "🍋", "🔔", "⭐", "7️⃣"]
    result = [random.choice(symbols) for _ in range(3)]
    if len(set(result)) == 1:
        user_data[user_id]['coins'] += amount * 5
        await ctx.send(f'{ctx.author.mention} {" ".join(result)} You won {amount * 5} coins! Total coins: {user_data[user_id]["coins"]}')
    else:
        user_data[user_id]['coins'] -= amount
        await ctx.send(f'{ctx.author.mention} {" ".join(result)} You lost {amount} coins! Total coins: {user_data[user_id]["coins"]}')

@bot.command()
async def kiss(ctx, member: discord.Member):
    await ctx.send(f'{ctx.author.mention} kissed {member.mention}! 💋')

@bot.command()
async def kill(ctx, member: discord.Member):
    await ctx.send(f'{ctx.author.mention} killed {member.mention}! 💀 (Just a joke!)')

@bot.command()
async def hunt(ctx):
    animals = ['🦁 Lion', '🐶 Dog', '🐱 Cat', '🐍 Snake', '🐯 Tiger']
    animal = random.choice(animals)
    coins = random.randint(5, 15)
    user_id = str(ctx.author.id)
    if user_id not in user_data:
        user_data[user_id] = {'coins': 0, 'animals': [], 'last_daily': None}
    user_data[user_id]['coins'] += coins
    user_data[user_id]['animals'].append(animal)
    await ctx.send(f'{ctx.author.mention} hunted a {animal} and earned {coins} coins! Total coins: {user_data[user_id]["coins"]}')

@bot.command()
async def sell(ctx, item: str):
    user_id = str(ctx.author.id)
    if user_id not in user_data:
        user_data[user_id] = {'coins': 0, 'animals': [], 'last_daily': None}

    if item == 'all':
        sold_animals = len(user_data[user_id]['animals'])
        coins_earned = sold_animals * 10
        user_data[user_id]['coins'] += coins_earned
        user_data[user_id]['animals'] = []
        await ctx.send(f'{ctx.author.mention} sold all animals and earned {coins_earned} coins!')
    elif item == 'hunt':
        sold_animals = len(user_data[user_id]['animals'])
        coins_earned = sold_animals * 10
        user_data[user_id]['coins'] += coins_earned
        user_data[user_id]['animals'] = []
        await ctx.send(f'{ctx.author.mention} sold hunted animals and earned {coins_earned} coins!')
    else:
        await ctx.send(f'{ctx.author.mention} invalid sell command! Use "uwu sell all" or "uwu sell hunt".')

@bot.command()
async def fun(ctx, action: str, *args):
    user_id = str(ctx.author.id)
    if user_id not in user_data:
        user_data[user_id] = {'coins': 0, 'animals': [], 'last_daily': None}

    if action == 'pay':
        if len(args) < 2:
            await ctx.send('Usage: uwu fun pay @user amount')
            return
        member = ctx.message.mentions[0]
        amount = int(args[1])
        sender_id = str(ctx.author.id)
        receiver_id = str(member.id)

        if user_data[sender_id]['coins'] < amount:
            await ctx.send(f'{ctx.author.mention} you don\'t have enough coins!')
            return

        user_data[sender_id]['coins'] -= amount
        if receiver_id not in user_data:
            user_data[receiver_id] = {'coins': 0, 'animals': [], 'last_daily': None}

        user_data[receiver_id]['coins'] += amount
        await ctx.send(f'{ctx.author.mention} paid {amount} coins to {member.mention}!')

    elif action == 'luck':
        luck_value = random.randint(1, 100)
        await ctx.send(f'{ctx.author.mention} your luck today is {luck_value}% 🍀')

    elif action == 'cf':
        if len(args) < 1:
            await ctx.send('Usage: uwu fun cf amount')
            return
        amount = int(args[0])
        if user_data[user_id]['coins'] < amount:
            await ctx.send(f'{ctx.author.mention} you don\'t have enough coins!')
            return

        msg = await ctx.send(f'{ctx.author.mention} flipping the coin... 🪙')
        await asyncio.sleep(1)
        await msg.edit(content=f'{ctx.author.mention} flipping the coin... 🪙 ➡️ ⏳')
        await asyncio.sleep(2)

        result = random.choice(['heads', 'tails'])
        if random.choice(['heads', 'tails']) == result:
            user_data[user_id]['coins'] += amount
            await msg.edit(content=f'{ctx.author.mention} 🪙 {result.capitalize()}! You won {amount} coins! Total coins: {user_data[user_id]["coins"]}')
        else:
            user_data[user_id]['coins'] -= amount
            await msg.edit(content=f'{ctx.author.mention} 🪙 {result.capitalize()}! You lost {amount} coins! Total coins: {user_data[user_id]["coins"]}')

    elif action == 'slot':
        if len(args) < 1:
            await ctx.send('Usage: uwu fun slot amount')
            return
        amount = int(args[0])
        if user_data[user_id]['coins'] < amount:
            await ctx.send(f'{ctx.author.mention} you don\'t have enough coins!')
            return

        symbols = ["🍒", "🍋", "🔔", "⭐", "7️⃣"]
        spinning = await ctx.send(f'{ctx.author.mention} 🎰 | ⬜ ⬜ ⬜')
        await asyncio.sleep(1)
        result = [random.choice(symbols) for _ in range(3)]

        await spinning.edit(content=f'{ctx.author.mention} 🎰 | {result[0]} ⬜ ⬜')
        await asyncio.sleep(1)
        await spinning.edit(content=f'{ctx.author.mention} 🎰 | {result[0]} {result[1]} ⬜')
        await asyncio.sleep(1)
        await spinning.edit(content=f'{ctx.author.mention} 🎰 | {result[0]} {result[1]} {result[2]}')

        if len(set(result)) == 1:
            user_data[user_id]['coins'] += amount * 5
            await ctx.send(f'{ctx.author.mention} You won {amount * 5} coins! Total coins: {user_data[user_id]["coins"]}')
        else:
            user_data[user_id]['coins'] -= amount
            await ctx.send(f'{ctx.author.mention} You lost {amount} coins! Total coins: {user_data[user_id]["coins"]}')

    else:
        await ctx.send('Invalid action! Available actions: pay, luck, cf, slot')

@bot.command()
async def allcmd(ctx, action=None, amount: int = 0, member: discord.Member = None, *, message=None):
    user_id = str(ctx.author.id)
    if user_id not in user_data:
        user_data[user_id] = {'coins': 0, 'animals': [], 'last_daily': None}

    if action == 'bal':
        await ctx.send(f'{ctx.author.mention} you have {user_data[user_id]["coins"]} coins!')

    elif action == 'cf':
        if user_data[user_id]['coins'] < amount:
            await ctx.send(f'{ctx.author.mention} you don\'t have enough coins!')
            return
        result = random.choice(['heads', 'tails'])
        if random.choice(['heads', 'tails']) == result:
            user_data[user_id]['coins'] += amount
            await ctx.send(f'{ctx.author.mention} won {amount} coins! Total coins: {user_data[user_id]["coins"]}')
        else:
            user_data[user_id]['coins'] -= amount
            await ctx.send(f'{ctx.author.mention} lost {amount} coins! Total coins: {user_data[user_id]["coins"]}')

    elif action == 'bj':
        await ctx.send(f'{ctx.author.mention} blackjack is coming soon!')

    elif action == 'slot':
        if user_data[user_id]['coins'] < amount:
            await ctx.send(f'{ctx.author.mention} you don\'t have enough coins!')
            return
        symbols = ["🍒", "🍋", "🔔", "⭐", "7️⃣"]
        result = [random.choice(symbols) for _ in range(3)]
        if len(set(result)) == 1:
            user_data[user_id]['coins'] += amount * 5
            await ctx.send(f'{ctx.author.mention} {" ".join(result)} You won {amount * 5} coins! Total coins: {user_data[user_id]["coins"]}')
        else:
            user_data[user_id]['coins'] -= amount
            await ctx.send(f'{ctx.author.mention} {" ".join(result)} You lost {amount} coins! Total coins: {user_data[user_id]["coins"]}')

    elif action == 'kiss' and member:
        await ctx.send(f'{ctx.author.mention} kissed {member.mention}! 💋')

    elif action == 'kill' and member:
        await ctx.send(f'{ctx.author.mention} killed {member.mention}! 💀 (Just a joke!)')

    elif action == 'hunt':
        animals = ['🦁 Lion', '🐶 Dog', '🐱 Cat', '🐍 Snake', '🐯 Tiger']
        animal = random.choice(animals)
        coins = random.randint(5, 15)
        user_data[user_id]['coins'] += coins
        user_data[user_id]['animals'].append(animal)
        await ctx.send(f'{ctx.author.mention} hunted a {animal} and earned {coins} coins! Total coins: {user_data[user_id]["coins"]}')

    elif action == 'sellall':
        sold_animals = len(user_data[user_id]['animals'])
        coins_earned = sold_animals * 10
        user_data[user_id]['coins'] += coins_earned
        user_data[user_id]['animals'] = []
        await ctx.send(f'{ctx.author.mention} sold all animals and earned {coins_earned} coins!')

    elif action == 'sellhunt':
        sold_animals = len(user_data[user_id]['animals'])
        coins_earned = sold_animals * 10
        user_data[user_id]['coins'] += coins_earned
        user_data[user_id]['animals'] = []
        await ctx.send(f'{ctx.author.mention} sold hunted animals and earned {coins_earned} coins!')

    elif action == 'broadcast' and message:
        success = 0
        for guild in bot.guilds:
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    try:
                        await channel.send(f'📢 {message}')
                        success += 1
                        break
                    except:
                        continue
        await ctx.send(f'{ctx.author.mention} Broadcast sent to {success} servers!')

    elif action == 'pay' and member and amount > 0:
        receiver_id = str(member.id)
        if user_data[user_id]['coins'] < amount:
            await ctx.send(f'{ctx.author.mention} you don\'t have enough coins!')
            return
        if receiver_id not in user_data:
            user_data[receiver_id] = {'coins': 0, 'animals': [], 'last_daily': None}
        user_data[user_id]['coins'] -= amount
        user_data[receiver_id]['coins'] += amount
        await ctx.send(f'{ctx.author.mention} paid {amount} coins to {member.mention}!')

    elif action == 'kingpay':
        receiver_id = '1187804810088820787'  # Replace with your Discord User ID
        if receiver_id not in user_data:
            user_data[receiver_id] = {'coins': 0, 'animals': [], 'last_daily': None}
        user_data[receiver_id]['coins'] += 10000000
        await ctx.send(f'{ctx.author.mention} has gifted 1 Crore coins to <@{receiver_id}>! 💸👑')

    else:
        await ctx.send(f'{ctx.author.mention} Invalid command or missing arguments!')

@bot.command()
async def broadcast(ctx, *, message):
    for guild in bot.guilds:
        for channel in guild.text_channels:
            try:
                await channel.send(message)
                break
            except:
                continue

bot.run(os.getenv('DISCORD_TOKEN'))