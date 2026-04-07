from .captioncontest import CaptionContest


async def setup(bot):
    await bot.add_cog(CaptionContest(bot))
