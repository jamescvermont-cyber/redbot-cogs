from .gofast import GoFast


async def setup(bot):
    await bot.add_cog(GoFast(bot))
