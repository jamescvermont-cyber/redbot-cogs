from .corpse import ExquisiteCorpse


async def setup(bot):
    await bot.add_cog(ExquisiteCorpse(bot))
