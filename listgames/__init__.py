from .listgames import ListGames


async def setup(bot):
    await bot.add_cog(ListGames(bot))
