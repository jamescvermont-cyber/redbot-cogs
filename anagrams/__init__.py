from .anagrams import Anagrams


async def setup(bot):
    await bot.add_cog(Anagrams(bot))
