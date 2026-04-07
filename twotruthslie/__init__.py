from .twotruthslie import TwoTruthsLie


async def setup(bot):
    await bot.add_cog(TwoTruthsLie(bot))
