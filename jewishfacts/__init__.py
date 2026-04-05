from .jewishfacts import JewishFacts


async def setup(bot):
    await bot.add_cog(JewishFacts(bot))
