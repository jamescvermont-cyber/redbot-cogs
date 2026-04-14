from .brandguesser import BrandGuesser


async def setup(bot):
    await bot.add_cog(BrandGuesser(bot))
