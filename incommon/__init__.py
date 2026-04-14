from .incommon import InCommon


async def setup(bot):
    await bot.add_cog(InCommon(bot))
