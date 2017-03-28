from discord.ext import commands
from kernel import enrich_user_id
import re


class Commands:
    """
    General Commands cog.

    This class contains the commands of the bot.
    """
    def __init__(self,
                 bot: commands.Bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def avatar(self, ctx: commands.Context, user_id):
        author = ctx.message.author
        server = ctx.message.server
        if user_id == "me":
            await self.bot.send_message(ctx.message.channel,
                                        'Avatar hash is {0.avatar} {0.avatar_url}'.format(author))
        else:
            member = enrich_user_id(
                server,
                re.sub('[<>@]', '', user_id))
            await self.bot.send_message(ctx.message.channel,
                                        'Avatar hash is {0.avatar} {0.avatar_url}'.format(member))

    @commands.command(pass_context=True)
    async def roles(self, ctx: commands.Context, user: str):
        author = ctx.message.author
        server = ctx.message.server
        member = enrich_user_id(
            server,
            re.sub('[<>@]', '', user))
        output = '{0.mention} a les rôles suivants:```\n'.format(member)
        for role in member.roles:
            if not role.name == '@everyone':
                output += '* {}\n'.format(
                    re.sub('@', '', role.name)
                )
        output += '```'
        await self.bot.send_message(ctx.message.channel, output)
