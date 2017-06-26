from discord.ext import commands

from kernel import has_power, enrich_user_id
from kernel.cogs.profile import Person
from kernel.cogs import Cog


class AdminCog(Cog):
    @commands.command(pass_context=True)
    async def rewind(self, ctx: commands.Context, number: int):
        if has_power(ctx.message.author):
            messages = []
            async for message in self.bot.logs_from(ctx.message.channel, limit=number):
                messages.append(message)
            await self.bot.delete_messages(messages)

    @commands.command(pass_context=True)
    async def mute(self, ctx: commands.Context, member):
        if has_power(ctx.message.author):
            user = enrich_user_id(self.bot.server, member)
            user_redis = Person(user.id, self.bot.redis)
            user_redis.update('muted', True)
            await self.bot.reply('{} a été réduit au silence.'.format(
                user.mention
            ))

    @commands.command(pass_context=True)
    async def demute(self, ctx: commands.Context, member):
        if has_power(ctx.message.author):
            user = enrich_user_id(self.bot.server, member)
            user_redis = Person(user.id, self.bot.redis)
            user_redis.update('muted', False)
            await self.bot.reply('{} a maintenant de nouveau la parole.'.format(
                user.mention
            ))

    async def on_message(self, message):
        if Person(message.author.id, self.bot.redis).muted:
            await self.bot.delete_message(message)
