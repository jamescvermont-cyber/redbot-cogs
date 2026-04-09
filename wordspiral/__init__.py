from .wordspiral import WordSpiral


async def setup(bot):
    await bot.add_cog(WordSpiral(bot))
