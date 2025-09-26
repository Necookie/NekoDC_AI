from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="neko_ping")
    async def ping(self, ctx):
        """Check bot latency."""
        await ctx.send(f"Pong! Latency: {round(self.bot.latency*1000)}ms 😎")

    @commands.command(name="neko_help")
    async def help(self, ctx):
        """Show list of commands."""
        help_text = """
**NekoDC_AI Commands**
!neko [message] - Chat with Dheyn's personality
!neko_ping - Check bot latency
!neko_help - Show this message
"""
        await ctx.send(help_text)

# --- async setup for discord.py 2.3+ ---
async def setup(bot):
    await bot.add_cog(General(bot))
