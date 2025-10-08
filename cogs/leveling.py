import discord
from discord.ext import commands

class LevelSys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @commands.Cog.listener()
        async def on_ready():
            print("Leveling cog is now ready")

async def setup(bot):
    await bot.add_cog(LevelSys(bot))