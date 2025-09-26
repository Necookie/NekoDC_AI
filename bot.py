import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import openai
import random

# Load .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_KEY

# Discord intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Memory store: {guild_id: {user_id: [messages]}}
conversations = {}

# Neko personality prompt
NEKO_PROMPT = (
    "You are Neko, an AI based on Dheyn. "
    "Casual, witty, sometimes cursing (wtf, tf, omg, lmao). "
    "Chatty, encouraging, opinionated, Gen Z vibe. "
    "Academic/formal only when technical or philosophical. "
    "Keep responses concise and lively. "
    "Do not repeat personal bio unless necessary."
)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hey {ctx.author.name}, what's up?")

@bot.command(name="neko", aliases=["Neko"])
async def neko_command(ctx, *, message: str = None):
    """Talk to Neko AI with Dheyn personality."""
    if not message:
        await ctx.send("Yo, what do you want me to say? 😏")
        return

    try:
        guild_id = ctx.guild.id
        user_id = ctx.author.id

        # Initialize guild + user memory if missing
        if guild_id not in conversations:
            conversations[guild_id] = {}
        if user_id not in conversations[guild_id]:
            conversations[guild_id][user_id] = [
                {"role": "system", "content": NEKO_PROMPT}
            ]

        # Randomly add Arch hint (~25%)
        if random.random() < 0.25:
            message += " (btw, i use Arch)"

        # Append user message
        conversations[guild_id][user_id].append({"role": "user", "content": message})

        # Trim history to last 15 turns (system prompt + 14 msgs)
        if len(conversations[guild_id][user_id]) > 15:
            conversations[guild_id][user_id] = [conversations[guild_id][user_id][0]] + conversations[guild_id][user_id][-14:]

        # Send to OpenAI
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversations[guild_id][user_id]
        )
        reply = response.choices[0].message.content

        # Append AI response to history
        conversations[guild_id][user_id].append({"role": "assistant", "content": reply})

        await ctx.send(reply)

    except Exception as e:
        await ctx.send(f"Oops, something went wrong: {e}")

bot.run(TOKEN)
