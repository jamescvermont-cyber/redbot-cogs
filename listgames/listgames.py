import discord
from redbot.core import commands
from pathlib import Path


class ListGames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def listgames(self, ctx):
        """List all games available on this server."""
        games_file = Path(__file__).parent / "games.md"
        content = games_file.read_text(encoding="utf-8")
        embed = discord.Embed(
            title="Games You Can Play Here",
            description=content,
            color=discord.Color.blurple(),
        )
        await ctx.send(embed=embed)
