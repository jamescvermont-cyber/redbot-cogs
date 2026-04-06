import discord
from redbot.core import commands


class GameStop(commands.Cog):
    """Universal command to stop any active game in the current channel."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="end")
    @commands.guild_only()
    async def end(self, ctx: commands.Context):
        """Stop any active game running in this channel."""
        stopped = []
        for cog in self.bot.cogs.values():
            if hasattr(cog, "force_stop_game"):
                name = await cog.force_stop_game(ctx.channel.id)
                if name:
                    stopped.append(name)

        if not stopped:
            await ctx.send("No games are running in this channel.")
        else:
            games_str = ", ".join(stopped)
            await ctx.send(embed=discord.Embed(
                description=f"🛑 Stopped: {games_str}",
                color=discord.Color.red(),
            ))
