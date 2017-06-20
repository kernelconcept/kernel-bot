from raven import Client

from typing import List, Union

from discord.ext import commands

from kernel import text, enrich_user_id, has_admin, fetch_users_from_role, enrich_role_id, enrich_role_name, bot
from kernel.image import generate_profile
from kernel.cogs import Cog
from kernel import db

import re

sentry = Client('https://62ffbf83e1204334ae60fd85305239f2:c8033d9c0312464f87593d93b7040a11@sentry.io/154891')


class Badge(db.RedisMixin):
    """
    Badge class
    """
    def __init__(self, item_id: str, redis_inst):
        super().__init__(item_id, redis_inst)

        self.key = 'badge'

    @property
    def name(self) -> str:
        return self.fetch('name')

    @property
    def desc(self):
        return self.fetch('desc')


class Person(db.RedisMixin):
    """
    Person class
    """
    def __init__(self, item_id: str, redis_inst):
        super().__init__(item_id, redis_inst)

        self.key = 'person'

    @property
    def title(self) -> str:
        return self.fetch('title')

    @property
    def desc(self) -> str:
        return self.fetch('desc')

    @property
    def thanks_count(self) -> int:
        thanks = self.fetch('thanks')
        if thanks:
            return int(thanks)

    @property
    def available(self) -> bool:
        r = self.fetch('availability')
        if r:
            if 'False' in r:
                return False
            elif 'True' in r:
                return True
        else:
            return False

    @property
    def badges(self) -> List[str]:
        if self.scan('badges'):
            return [str(b.decode('utf-8')).split('/')[-1] for b in self.scan('badges')]

    def set_availability(self, cmd) -> bool:
        if cmd == 'oui':
            self.update('availability', True)
            return True
        elif cmd == 'non':
            self.update('availability', False)
            return True
        else:
            return False

    def thanks(self) -> int:
        thanks = self.thanks_count or 0
        self.update('thanks', thanks + 1)
        return self.thanks_count - 1


class ProfileCog(Cog):
    """
    Profile cog.

    This cog creates a Redis connection to store and fetch `profiles`.
    These consists in adding more custom fields to a discord_id according to
    Kernel Concept's works. The code itself is pretty self-explanatory so it doesn't require much documentation.
    """

    @commands.command()
    async def init(self):
        count = 0
        for member in self.bot.server.members:
            person = Person(member.id, self.bot.redis)
            if person.was_just_created:
                count += 1
        if count:
            if count == 1:
                await self.bot.reply(text.INIT_ONE, delete_after=bot.MESSAGE_DELETE_AFTER)
            await self.bot.reply(text.INIT_MULTIPLE.format(count), delete_after=bot.MESSAGE_DELETE_AFTER)
        else:
            await self.bot.reply(text.INIT_NOBODY, delete_after=bot.MESSAGE_DELETE_AFTER)

    @commands.command(pass_context=True, aliases=['bonbonalafraise', 'vroumvroum', 'chaussonsauxpommes'])
    async def reset(self, ctx: commands.Context):
        Person(ctx.message.author.id, self.bot.redis).reset()
        await self.bot.reply(text.RESET, delete_after=bot.MESSAGE_DELETE_AFTER)

    @commands.command(pass_context=True)
    async def drift(self, ctx:commands.context, person_id, thanks_only):
        person = enrich_user_id(self.bot.server, person_id)

        if ctx.message.author.id == '132253217529659393':
            if thanks_only == 'y':
                Person(person.id, self.bot.redis).update('thanks', 0)
                await self.bot.reply(text.RESET, delete_after=bot.MESSAGE_DELETE_AFTER)
            else:
                Person(person.id, self.bot.redis).reset()
                await self.bot.reply(text.RESET, delete_after=bot.MESSAGE_DELETE_AFTER)

    @commands.command(pass_context=True)
    async def turbocharge(self, ctx: commands.context, person_id):
        person = enrich_user_id(self.bot.server, person_id)

        if ctx.message.author.id == '132253217529659393':
            person = Person(person.id, self.bot.redis)
            person.update('turbo', True)
            person.update('thanks', 99)
            person.update('title', 'TURBOCHARGED DUDE')
            person.update('desc', 'I\'VE JUST BEEN TURBOCHARGED AND IT FEELS GREAT !')
            await self.bot.reply('TU-TU-TU-TURBOCHARGED !', delete_after=bot.MESSAGE_DELETE_AFTER)

    @commands.command(pass_context=True, aliases=['doom'])
    async def cleanse(self, ctx: commands.Context):
        if has_admin(self.bot.server, ctx.message.author):
            for member in self.bot.server.members:
                Person(member.id, self.bot.redis).reset()
            await self.bot.reply(text.CLEANSE, delete_after=bot.MESSAGE_DELETE_AFTER)
        else:
            await self.bot.reply(text.NO_RIGHTS, delete_after=bot.MESSAGE_DELETE_AFTER)

    @commands.command(pass_context=True, aliases=['profil', 'carte', 'card'])
    async def profile(self, ctx: commands.Context, member_id: str = None):
        member = None
        if member_id:
            member = enrich_user_id(self.bot.server, member_id)
        profile = member or ctx.message.author
        redis_profile = Person(profile.id, self.bot.redis)
        profile_title = redis_profile.title
        profile_thanks = redis_profile.thanks_count
        profile_desc = redis_profile.desc
        profile_disp = redis_profile.available
        profile_badges = redis_profile.badges
        turbo = redis_profile.fetch('turbo')
        if profile_thanks:
            profile_thanks = int(profile_thanks)
        picture = generate_profile(
            profile,
            profile.name,
            profile_title or 'Aucun titre',
            profile_desc or 'Pas de description',
            profile_disp,
            profile.avatar_url,
            profile_thanks or 0,
            profile_badges or None,
            turbo
        )
        if picture:
            await self.bot.send_file(
                ctx.message.channel,
                picture,
                content=text.PROFILE_SUCCESS.format(profile),
            )
        else:
            await self.bot.reply(text.PROFILE_FAILURE, delete_after=bot.MESSAGE_DELETE_AFTER)

    @commands.command(pass_context=True, aliases=['merci'])
    async def thanks(self, ctx: commands.Context, member: str = None, reason: str = None):
        if member:
            user = enrich_user_id(self.bot.server, member) or ''
            if user.id == ctx.message.author.id:
                await self.bot.reply(text.THANKS_SELF, delete_after=bot.MESSAGE_DELETE_AFTER)
            else:
                person = Person(user.id, self.bot.redis)
                thanks_count = person.thanks()
                if reason:
                    await self.bot.reply(text.THANKS_ACTION_MSG.format(
                        user.mention,
                        thanks_count,
                        reason,
                    ), delete_after=bot.MESSAGE_DELETE_AFTER)
                else:
                    await self.bot.reply(text.THANKS_ACTION.format(
                        user.mention,
                        thanks_count
                    ), delete_after=bot.MESSAGE_DELETE_AFTER)
        else:
            person = Person(ctx.message.author.id, self.bot.redis)
            thanks_count = person.fetch('thanks')
            if thanks_count:
                thanks_count = int(thanks_count)
                await self.bot.reply(text.THANKS.format(thanks_count), delete_after=bot.MESSAGE_DELETE_AFTER)
            else:
                await self.bot.reply(text.THANKS_NONE, delete_after=bot.MESSAGE_DELETE_AFTER)

    @commands.command(pass_context=True, aliases=['dispo'])
    async def available(self, ctx: commands.Context, cmd: str, *args):
        output = '```diff'
        if cmd.startswith('<@&') or cmd.startswith('roletest'):
            if cmd.startswith('roletest'):
                role = enrich_role_name(self.bot.server, 'Artiste 2D')
            else:
                role = enrich_role_id(self.bot.server, cmd)
            output += '\n {}s disponibles:\n'.format(role.name)
            members = fetch_users_from_role(self.bot.server, role)
            if members:
                for member in members:
                    if Person(member.id, self.bot.redis).available:
                        if len(output + '\n+ {}'.format(text.AVAILABILITY_TRUE.format(member))) >= 1800:
                            await self.bot.reply(output, delete_after=bot.MESSAGE_DELETE_AFTER)
                            output = '```diff'
                        output += '\n+ {}'.format(text.AVAILABILITY_TRUE.format(member))
            output += '```'
            await self.bot.reply(output, delete_after=bot.MESSAGE_DELETE_AFTER)
        elif cmd == 'oui' or cmd == 'non':
            r = Person(ctx.message.author.id, self.bot.redis).set_availability(cmd)
            await self.bot.reply(text.AVAILABILITY_CHANGE.format(
                ctx.message.author
            ), delete_after=bot.MESSAGE_DELETE_AFTER)
        else:
            user = enrich_user_id(self.bot.server, cmd)
            if user:
                if Person(user.id, self.bot.redis).available:
                    output += '\n+ {}'.format(text.AVAILABILITY_TRUE.format(user))
                else:
                    output += '\n- {}'.format(text.AVAILABILITY_FALSE.format(user))
                if args:
                    for arg in args:
                        user = enrich_user_id(self.bot.server, arg)
                        if user:
                            if Person(user.id, self.bot.redis).available:
                                output += '\n+ {}'.format(text.AVAILABILITY_TRUE.format(user))
                            else:
                                output += '\n- {}'.format(text.AVAILABILITY_FALSE.format(user))
                        else:
                            pass
                output += '\n```'
                await self.bot.reply(output, delete_after=bot.MESSAGE_DELETE_AFTER)
            else:
                await self.bot.reply(text.AVAILABILITY_WRONG_ARGS, delete_after=bot.MESSAGE_DELETE_AFTER)

    @commands.command(pass_context=True, aliases=['titre', 'title'])
    async def nick(self, ctx: commands.Context, cmd: str = None, input_title: str = None):
        if cmd:
            if cmd.startswith('<'):
                enriched_user = enrich_user_id(self.bot.server, cmd)
                user_title = Person(enriched_user.id, self.bot.redis).fetch('title')
                if not user_title:
                    await self.bot.reply(text.NO_NICK, delete_after=bot.MESSAGE_DELETE_AFTER)
                else:
                    await self.bot.reply(text.HAS_NICK.format(
                        enriched_user.mention,
                        user_title
                    ), delete_after=bot.MESSAGE_DELETE_AFTER)
            if cmd == 'edit' or cmd== 'set':
                if not input_title:
                    await self.bot.reply(text.USAGE_NICK, delete_after=bot.MESSAGE_DELETE_AFTER)
                else:
                    if len(input_title) > 24:
                        await self.bot.reply(text.TOO_LONG_NICK, delete_after=bot.MESSAGE_DELETE_AFTER)
                    else:
                        title = re.sub('[`\'"@&^%$!*()+=-]', '', input_title)
                        Person(ctx.message.author.id, self.bot.redis).update('title', title)
                        await self.bot.reply(text.UPDATED_NICK.format(title), delete_after=bot.MESSAGE_DELETE_AFTER)
        else:
            author = ctx.message.author
            user_title = Person(author.id, self.bot.redis).title
            if not user_title:
                await self.bot.reply(text.NO_SELF_NICK, delete_after=bot.MESSAGE_DELETE_AFTER)
            else:
                await self.bot.reply(text.HAS_SELF_NICK.format(
                    author.mention,
                    user_title
                ), delete_after=bot.MESSAGE_DELETE_AFTER)

    @commands.command(pass_context=True, aliases=['description'])
    async def desc(self, ctx: commands.Context, cmd: str = None, input_desc: str = None):
        if cmd:
            if cmd.startswith('<'):
                enriched_user = enrich_user_id(self.bot.server, cmd)
                user_desc = Person(enriched_user.id, self.bot.redis).fetch('desc')
                if not user_desc:
                    await self.bot.reply(text.NO_DESC, delete_after=bot.MESSAGE_DELETE_AFTER)
                else:
                    await self.bot.reply(text.HAS_DESC.format(
                        enriched_user.mention,
                        user_desc
                    ), delete_after=bot.MESSAGE_DELETE_AFTER)
            if cmd == 'edit' or cmd == 'set':
                if not input_desc:
                    await self.bot.reply(text.USAGE_DESC, delete_after=bot.MESSAGE_DELETE_AFTER)
                else:
                    if len(input_desc) > 150:
                        await self.bot.reply(text.TOO_LONG_DESC, delete_after=bot.MESSAGE_DELETE_AFTER)
                    else:
                        Person(ctx.message.author.id, self.bot.redis).update('desc', input_desc)
                        await self.bot.reply(text.UPDATED_DESC.format(input_desc), delete_after=bot.MESSAGE_DELETE_AFTER)
        else:
            author = ctx.message.author
            user_desc = Person(author.id, self.bot.redis).desc
            if not user_desc:
                await self.bot.reply(text.NO_SELF_DESC, delete_after=bot.MESSAGE_DELETE_AFTER)
            else:
                await self.bot.reply(text.HAS_SELF_DESC.format(
                    user_desc), delete_after=bot.MESSAGE_DELETE_AFTER)

    @commands.command()
    async def badge(self, member):
        user = enrich_user_id(self.bot.server, member)
        if user:
            if Person(user.id, self.bot.redis).badges:
                badges = [Badge(b, self.bot.redis) for b in Person(user.id, self.bot.redis).badges]
                output = '```\n'
                for badge in badges:
                    output += '- {}: {}\n{}\n\n'.format(
                        badge.item_id,
                        badge.name,
                        badge.desc
                    )
                output += '```'
                await self.bot.reply(text.HAS_BADGES.format(user.name, output))
            else:
                await self.bot.reply(text.NO_BADGES.format(user.name))
        elif member.startswith('<@&'):
            await self.bot.reply(text.COMMAND_NO_ROLES)
        else:
            await self.bot.reply(text.COMMAND_USER_NOT_FOUND)

    @commands.command()
    async def badgesee(self, badge_id):
        badge = Badge(badge_id, self.bot.redis)
        if badge.exists:
            await self.bot.reply('{}:\n\n{}'.format(badge.name, badge.desc))
        else:
            await self.bot.reply(text.BADGE_NOT_FOUND)

    @commands.command(pass_context=True)
    async def badgeedit(self, ctx: commands.Context, badge_id, key, value):
        if ctx.message.author.id == '132253217529659393':
            badge = Badge(badge_id, self.bot.redis)
            badge.update(key, value)
            await self.bot.reply('la valeur est mise à jour.')

    @commands.command(pass_context=True)
    async def badgegrant(self, ctx: commands.Context, member_id, badge_id):
        member = enrich_user_id(self.bot.server, member_id)

        if ctx.message.author.id == '132253217529659393':
            member_redis = Person(member.id, self.bot.redis)
            badge = Badge(badge_id, self.bot.redis)
            if badge.exists:
                member_redis.update('badges/{}'.format(badge_id), True)
                await self.bot.reply('{} a maintenant le badge de {}.'.format(member.mention, badge.name))
