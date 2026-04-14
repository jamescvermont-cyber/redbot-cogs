from .trackpoints import TrackPoints


async def setup(bot):
    await bot.add_cog(TrackPoints(bot))
