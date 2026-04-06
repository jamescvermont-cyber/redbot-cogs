from .wordguesser import WordGuesser


async def setup(bot):
    await bot.add_cog(WordGuesser(bot))
