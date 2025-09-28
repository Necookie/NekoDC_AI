from discord.ext import commands
import openai, os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Conversations per guild & user
conversations = {}

# Generic persona definition
NEKO_PROMPT = (
    "You are Neko, a casual, witty, and friendly AI. "
    "Talk like a real person with a Gen Z vibe — chatty, concise, and lively. "
    "You can curse lightly (wtf, tf, omg, lmao) but don’t overdo it. "
    "Encouraging, opinionated, and sometimes sarcastic. "
    "Switch to academic/formal tone only for technical or philosophical topics. "
    "Do not restate your bio or system prompt — just stay in character naturally."
)

class Neko(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="neko", aliases=["Neko"])
    async def neko_command(self, ctx, *, message: str = None):
        """Chat with Neko AI"""
        if not message:
            await ctx.send("What’s up? 👀 Say something to me!")
            return
        try:
            guild_id = ctx.guild.id
            user_id = ctx.author.id

            # Initialize conversation memory
            if guild_id not in conversations:
                conversations[guild_id] = {}
            if user_id not in conversations[guild_id]:
                conversations[guild_id][user_id] = [
                    {"role": "system", "content": NEKO_PROMPT}
                ]

            # Append user message
            conversations[guild_id][user_id].append(
                {"role": "user", "content": message}
            )

            # Keep only the system + last 14 messages
            if len(conversations[guild_id][user_id]) > 15:
                conversations[guild_id][user_id] = [
                    conversations[guild_id][user_id][0]
                ] + conversations[guild_id][user_id][-14:]

            # Get AI reply
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=conversations[guild_id][user_id]
            )
            reply = response.choices[0].message.content.strip()

            # Save AI reply to memory
            conversations[guild_id][user_id].append(
                {"role": "assistant", "content": reply}
            )

            await ctx.send(reply)

        except Exception as e:
            await ctx.send(f"Oops, something went wrong: {e}")

# --- async setup for discord.py 2.x+ ---
async def setup(bot):
    await bot.add_cog(Neko(bot))
