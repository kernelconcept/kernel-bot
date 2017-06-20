from discord.ext import commands


class Cog:
    def __init__(self, bot: commands.Bot):
        self.bot = bot