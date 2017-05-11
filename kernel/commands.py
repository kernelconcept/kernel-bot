from discord.ext import commands
from kernel import enrich_user_id
from kernel.text import COMMAND_ROLE_NO_ARGS_GIVEN
import re

CREATOR_ID = '132253217529659393'


class Commands:
    """
    General Commands cog.

    This class contains the commands of the bot.
    """
    def __init__(self,
                 bot: commands.Bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def avatar(self, ctx: commands.Context, user_id: str = None):
        author = ctx.message.author
        server = ctx.message.server
        if not user_id:
            await self.bot.send_message(ctx.message.channel,
                                        'Ton avatar: {0.avatar_url}'.format(author))
        else:
            member = enrich_user_id(server, user_id)
            await self.bot.send_message(ctx.message.channel,
                                        'L\'avatar de {0.mention}: {0.avatar_url}'.format(member))

    @commands.command(pass_context=True, aliases=['headshot', 'close', 'expel'])
    async def kill(self, ctx: commands.Context):
        if ctx.message.author.id == CREATOR_ID:
            await self.bot.send_message(ctx.message.channel,
                                        '[test] Reçu. Extinction en cours.')
            await self.bot.close()
        else:
            await self.bot.send_message(ctx.message.channel, 'Tu n\'es pas autorisé à ordonner mon extinction.')

    @commands.command(pass_context=True, aliases=['who', 'quiestu', 'kernelbot'])
    async def whoareyou(self, ctx: commands.Context):
        await self.bot.send_message(ctx.message.channel,
                                    'Je suis le très rare Kernel Bot aux quatres yeux. Je réponds à tout le monde. Je vois tout ceux qui sont ici. Je sais ce que vous faites.')

    @commands.command(pass_context=True)
    async def role(self, ctx: commands.Context, user: str = None):
        author = ctx.message.author
        server = ctx.message.server
        if not user:
            await self.bot.delete_message(ctx.message)
            await self.bot.send_message(author, COMMAND_ROLE_NO_ARGS_GIVEN.format(author))
        else:
            member = enrich_user_id(server, user)
            output = '{0.mention} a les rôles suivants:```\n'.format(member)
            for role in member.roles:
                if not role.name == '@everyone':
                    output += '* {}\n'.format(
                        re.sub('@', '', role.name)
                    )
            output += '```'
            await self.bot.send_message(ctx.message.channel, output)
