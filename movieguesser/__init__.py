from .movieguesser import MovieGuesser


async def setup(bot):
    await bot.add_cog(MovieGuesser(bot))
