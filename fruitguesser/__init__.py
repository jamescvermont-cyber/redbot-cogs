from .fruitguesser import FruitGuesser


async def setup(bot):
    await bot.add_cog(FruitGuesser(bot))
