from .gamestop import GameStop


async def setup(bot):
    await bot.add_cog(GameStop(bot))
