from discord.ext import commands
from kernel import enrich_user_id, enrich_emoji, text
from kernel.bot import MESSAGE_DELETE_AFTER
import random
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
            await self.bot.reply(text.SELF_AVATAR.format(author), delete_after=MESSAGE_DELETE_AFTER)
        else:
            member = enrich_user_id(server, user_id)
            await self.bot.reply(text.USER_AVATAR.format(member), delete_after=MESSAGE_DELETE_AFTER)

    @commands.command(pass_context=True, aliases=['headshot', 'close', 'expel'])
    async def kill(self, ctx: commands.Context):
        if ctx.message.author.id == CREATOR_ID:
            await self.bot.reply(text.KILL)
            await self.bot.close()
        else:
            await self.bot.reply(text.NO_RIGHTS, delete_after=MESSAGE_DELETE_AFTER)

    @commands.command(aliases=['who', 'quiestu', 'kernelbot'])
    async def whoareyou(self):
        await self.bot.reply(text.WHOAREYOU, delete_after=MESSAGE_DELETE_AFTER)

    @commands.command()
    async def role(self, user: str = None):
        if not user:
            await self.bot.reply(text.COMMAND_NO_ARGS_GIVEN.format('role'), delete_after=MESSAGE_DELETE_AFTER)
        else:
            member = enrich_user_id(self.bot.server, user)
            output = text.ROLE.format(member)
            for role in member.roles:
                if not role.name == '@everyone':
                    output += '* {}\n'.format(
                        re.sub('@', '', role.name)
                    )
            output += '```'
            await self.bot.reply(output, delete_after=MESSAGE_DELETE_AFTER)

    @commands.command(pass_context=True)
    async def hug(self, ctx: commands.Context, user: str):
        to_hug = enrich_user_id(self.bot.server, user)
        print(ctx.message.content)
        if to_hug.id == ctx.message.author.id:
            await self.bot.reply('J\'ai sincèrement pitié de toi.')
        elif 'Kernel Bot' in to_hug.name:
            await self.bot.send_message(ctx.message.channel, '{} s\'exhibe contre du métal froid (j\'suis un bot, tu t\'attendais à quoi eh ?).'.format(ctx.message.author.mention))
        else:
            emoji = random.choice(text.HUGS)
            await self.bot.send_message(ctx.message.channel, '{} {} {}'.format(
                ctx.message.author.mention,
                emoji,
                to_hug.mention
            ))

