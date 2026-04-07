from .rhymeduel import RhymeDuel


async def setup(bot):
    await bot.add_cog(RhymeDuel(bot))
