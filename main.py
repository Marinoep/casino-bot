import discord
from discord.ext import commands
import random
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

balances = {}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def balance(ctx):
    user = ctx.author
    bal = balances.get(user.id, 1000)
    await ctx.send(f"{user.mention}, your balance is 💰 ${bal}")

@bot.command()
async def bet(ctx, amount: int):
    user = ctx.author
    bal = balances.get(user.id, 1000)

    if amount <= 0:
        await ctx.send("Bet must be more than zero!")
        return
    if amount > bal:
        await ctx.send("You don't have enough money to bet that much!")
        return

    result = random.choice(["win", "lose"])
    if result == "win":
        bal += amount
        await ctx.send(f"You won! 🎉 Your new balance is ${bal}")
    else:
        bal -= amount
        await ctx.send(f"You lost! 💸 Your new balance is ${bal}")

    balances[user.id] = bal

@bot.command()
async def slots(ctx):
    user = ctx.author
    emojis = ["🍒", "🍋", "🍉", "🍇", "💎"]
    result = [random.choice(emojis) for _ in range(3)]
    await ctx.send(f"{' | '.join(result)}")

    if result[0] == result[1] == result[2]:
        bal = balances.get(user.id, 1000) + 500
        await ctx.send(f"JACKPOT! 🎰 You won $500!")
    else:
        bal = balances.get(user.id, 1000) - 50
        await ctx.send(f"You lost $50 😢")

    balances[user.id] = bal
    await ctx.send(f"{user.mention}, your balance is now ${bal}")

bot.run(os.environ["DISCORD_TOKEN"])
