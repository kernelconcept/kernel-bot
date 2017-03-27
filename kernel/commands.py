from discord.ext import commands


class Commands:
    """
    General Commands cog.

    This class contains the commands of the bot.
    """
    def __init__(self,
                 bot: commands.Bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def banana(self, ctx: commands.Context):
        author = ctx.message.author
        await self.bot.send_message(ctx.message.channel, '*Gives a banana to {0.mention}.*'.format(author))
