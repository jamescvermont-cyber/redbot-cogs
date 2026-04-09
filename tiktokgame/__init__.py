from .tiktokgame import TikTokGameCog


async def setup(bot):
    await bot.add_cog(TikTokGameCog(bot))
