from discord.ext import commands
import openai, os, random
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

conversations = {}

NEKO_PROMPT = (
    "You are Neko, an AI based on Dheyn. "
    "Casual, witty, sometimes cursing (wtf, tf, omg, lmao). "
    "Chatty, encouraging, opinionated, Gen Z vibe. "
    "Academic/formal only when technical or philosophical. "
    "Keep responses concise and lively. "
    "Do not repeat personal bio unless necessary."
)

class Neko(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="neko", aliases=["Neko"])
    async def neko_command(self, ctx, *, message: str = None):
        if not message:
            await ctx.send("Yo, what do you want me to say? 😏")
            return
        try:
            guild_id = ctx.guild.id
            user_id = ctx.author.id

            if guild_id not in conversations:
                conversations[guild_id] = {}
            if user_id not in conversations[guild_id]:
                conversations[guild_id][user_id] = [{"role":"system","content":NEKO_PROMPT}]

            if random.random() < 0.25:
                message += " (btw, i use Arch)"

            conversations[guild_id][user_id].append({"role":"user","content":message})

            if len(conversations[guild_id][user_id]) > 15:
                conversations[guild_id][user_id] = [conversations[guild_id][user_id][0]] + conversations[guild_id][user_id][-14:]

            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=conversations[guild_id][user_id]
            )
            reply = response.choices[0].message.content

            conversations[guild_id][user_id].append({"role":"assistant","content":reply})

            await ctx.send(reply)

        except Exception as e:
            await ctx.send(f"Oops, something went wrong: {e}")

# --- async setup for discord.py 2.x+ ---
async def setup(bot):
    await bot.add_cog(Neko(bot))
