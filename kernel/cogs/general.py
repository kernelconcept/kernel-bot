from discord.ext import commands

from kernel import enrich_user_id, text, bot
from kernel.replies import reply
from kernel.cogs import Cog

import discord
import random
import re

CREATOR_ID = '132253217529659393'


class ListenersCog(Cog):
    async def on_ready(self):
        print('Online.')
        await self.bot.change_presence(
            game=discord.Game(name=bot.GAME))

    async def on_message(self, message):
        await reply(message, self.bot)

    async def on_message_edit(self, before, after):
        if not await reply(after, self.bot):
            await self.bot.process_commands(after)

    async def on_member_join(self, member):
        await self.bot.send_message(self.bot.welcome_channel, text.NEW_MEMBER.format(bot.SERVER_NAME, member))

    async def on_member_remove(self, member):
        await self.bot.send_message(self.bot.welcome_channel, text.MEMBER_LEAVE.format(member))

    async def on_member_ban(self, member):
        await self.bot.send_message(self.bot.welcome_channel, text.MEMBER_BAN.format(member))

    async def send_test(self, message):
        await self.bot.send_message(self.bot.test_channel, message)


class CommandsCog(Cog):
    """
    General Commands cog.

    This class contains the commands of the bot.
    """

    @commands.command(pass_context=True)
    async def avatar(self, ctx: commands.Context, user_id: str = None):
        author = ctx.message.author
        server = ctx.message.server
        if not user_id:
            await self.bot.reply(text.SELF_AVATAR.format(author), delete_after=bot.MESSAGE_DELETE_AFTER)
        else:
            member = enrich_user_id(server, user_id)
            await self.bot.reply(text.USER_AVATAR.format(member), delete_after=bot.MESSAGE_DELETE_AFTER)

    @commands.command(pass_context=True, aliases=['headshot', 'close', 'expel'])
    async def kill(self, ctx: commands.Context):
        if ctx.message.author.id == CREATOR_ID:
            await self.bot.reply(text.KILL)
            await self.bot.close()
        else:
            await self.bot.reply(text.NO_RIGHTS, delete_after=bot.MESSAGE_DELETE_AFTER)

    @commands.command(aliases=['who', 'quiestu', 'kernelbot'])
    async def whoareyou(self):
        await self.bot.reply(text.WHOAREYOU, delete_after=bot.MESSAGE_DELETE_AFTER)

    @commands.command()
    async def role(self, user: str = None):
        if not user:
            await self.bot.reply(text.COMMAND_NO_ARGS_GIVEN.format('role'), delete_after=bot.MESSAGE_DELETE_AFTER)
        else:
            member = enrich_user_id(self.bot.server, user)
            output = text.ROLE.format(member)
            for role in member.roles:
                if not role.name == '@everyone':
                    output += '* {}\n'.format(
                        re.sub('@', '', role.name)
                    )
            output += '```'
            await self.bot.reply(output, delete_after=bot.MESSAGE_DELETE_AFTER)

    @commands.command(pass_context=True)
    async def hug(self, ctx: commands.Context, user: str):
        to_hug = enrich_user_id(self.bot.server, user)
        print(ctx.message.content)
        if to_hug.id == ctx.message.author.id:
            await self.bot.reply('J\'ai sincèrement pitié de toi.')
        elif 'Kernel Bot' in to_hug.name:
            await self.bot.send_message(ctx.message.channel, text.HUG_BOT.format(ctx.message.author.mention))
            #  TODO: Fix the upper statement (it's REALLY ugly).
        else:
            emoji = random.choice(text.HUGS)
            await self.bot.send_message(ctx.message.channel, '{} {} {}'.format(
                ctx.message.author.mention,
                emoji,
                to_hug.mention
            ))
