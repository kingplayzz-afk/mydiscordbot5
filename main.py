import discord
from discord.ext import commands
import random
import os
from datetime import datetime
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

@bot.command()
async def allcmd(ctx, action=None, amount: int = 0, member: discord.Member = None, *, message=None):
    user_id = str(ctx.author.id)
    if user_id not in user_data:
        user_data[user_id] = {'balance': 0, 'animals': [], 'last_daily': None}

    if action == 'bal':
        await ctx.send(f'{ctx.author.mention} you have {user_data[user_id]["balance"]} coins!')

    elif action == 'cf':
        if user_data[user_id]['balance'] < amount:
            await ctx.send(f'{ctx.author.mention} you don\'t have enough coins!')
            return
        result = random.choice(['heads', 'tails'])
        if random.choice(['heads', 'tails']) == result:
            user_data[user_id]['balance'] += amount
            await ctx.send(f'{ctx.author.mention} won {amount} coins! Total: {user_data[user_id]["balance"]} coins')
        else:
            user_data[user_id]['balance'] -= amount
            await ctx.send(f'{ctx.author.mention} lost {amount} coins! Total: {user_data[user_id]["balance"]} coins')

    elif action == 'slot':
        if user_data[user_id]['balance'] < amount:
            await ctx.send(f'{ctx.author.mention} you don\'t have enough coins!')
            return
        symbols = ["🍒", "🍋", "🔔", "⭐", "7️⃣"]
        result = [random.choice(symbols) for _ in range(3)]
        if len(set(result)) == 1:
            user_data[user_id]['balance'] += amount * 5
            await ctx.send(f'{ctx.author.mention} {" ".join(result)} You won {amount * 5} coins! Total: {user_data[user_id]["balance"]} coins')
        else:
            user_data[user_id]['balance'] -= amount
            await ctx.send(f'{ctx.author.mention} {" ".join(result)} You lost {amount} coins! Total: {user_data[user_id]["balance"]} coins')

    elif action == 'kiss' and member:
        await ctx.send(f'{ctx.author.mention} kissed {member.mention}! 💋')

    elif action == 'kill' and member:
        await ctx.send(f'{ctx.author.mention} killed {member.mention}! 💀 (Just a joke!)')

    elif action == 'hunt':
        animals = ['🦁 Lion', '🐶 Dog', '🐱 Cat', '🐍 Snake', '🐯 Tiger']
        animal = random.choice(animals)
        coins = random.randint(5, 15)
        user_data[user_id]['balance'] += coins
        user_data[user_id]['animals'].append(animal)
        await ctx.send(f'{ctx.author.mention} hunted a {animal} and earned {coins} coins! Total: {user_data[user_id]["balance"]} coins')

    elif action == 'sellall':
        sold_animals = len(user_data[user_id]['animals'])
        coins_earned = sold_animals * 10
        user_data[user_id]['balance'] += coins_earned
        user_data[user_id]['animals'] = []
        await ctx.send(f'{ctx.author.mention} sold all animals and earned {coins_earned} coins!')

    elif action == 'broadcast' and message:
        for guild in bot.guilds:
            for channel in guild.text_channels:
                try:
                    await channel.send(message)
                    break
                except:
                    continue

    elif action == 'pay' and member and amount > 0:
        receiver_id = str(member.id)
        if user_data[user_id]['balance'] < amount:
            await ctx.send(f'{ctx.author.mention} you don\'t have enough coins!')
            return
        if receiver_id not in user_data:
            user_data[receiver_id] = {'balance': 0, 'animals': [], 'last_daily': None}
        user_data[user_id]['balance'] -= amount
        user_data[receiver_id]['balance'] += amount
        await ctx.send(f'{ctx.author.mention} paid {amount} coins to {member.mention}!')

    elif action == 'kingpay':
        receiver_id = str(member.id)
        if receiver_id not in user_data:
            user_data[receiver_id] = {'balance': 0, 'animals': [], 'last_daily': None}
        user_data[receiver_id]['balance'] += 10000000
        await ctx.send(f'{ctx.author.mention} has gifted 1 Crore coins to {member.mention}! 💸👑')

    else:
        await ctx.send(f'{ctx.author.mention} Invalid command or missing arguments!')

bot.run(os.getenv('DISCORD_TOKEN'))
                  
