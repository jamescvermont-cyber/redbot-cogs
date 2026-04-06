from .wordrush import WordRush


async def setup(bot):
    await bot.add_cog(WordRush(bot))
