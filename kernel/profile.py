"""
Du Python, encore et toujours.

profile.py
"""

from raven import Client
from discord.ext import commands
from kernel import text, enrich_user_id, has_admin, fetch_users_from_role, enrich_role_id, enrich_role_name
from kernel.bot import MESSAGE_DELETE_AFTER
from kernel.image import generate_profile
from typing import List, Union
import redis
import re

sentry = Client('https://62ffbf83e1204334ae60fd85305239f2:c8033d9c0312464f87593d93b7040a11@sentry.io/154891')


class RedisMixin:
    """
    Mixin for Redis classes.
    """
    def __init__(self, item_id: str, redis_inst):
        self.item_id = item_id
        self.redis = redis_inst
        self.key = None

    @property
    def exists(self) -> bool:
        return bool(self.redis.get('{}/{}'.format(self.key, self.item_id)))

    def init(self) -> bool:
        if not self.exists:
            self.redis.set('{}/{}'.format(self.key, self.item_id), True)
            return True
        return False

    def reset(self):
        for key in self.scan():
            self.redis.delete(key)

    def fetch(self, key) -> Union[str, int]:
        value = self.redis.get('{}/{}/{}'.format(
            self.key,
            self.item_id,
            key
        ))
        if value:
            return value.decode('utf-8')

    def scan(self, key=None):
        return [k for k in self.redis.scan_iter(match='{}/{}{}*'.format(
            self.key,
            self.item_id,
            '/{}'.format(key) or ''
        ))] or None

    def update(self, key, value):
        self.redis.set('{}/{}/{}'.format(
            self.key,
            self.item_id,
            key
        ), value)


class Badge(RedisMixin):
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


class Person(RedisMixin):
    """
    Person class
    """
    def __init__(self, item_id: str, redis_inst):
        super().__init__(item_id, redis_inst)

        self.key = 'person'
        #  Set the redis key to True if profile doesn't exist.
        self.was_just_created = self.init()

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


class Profile:
    """
    Profile cog.

    This cog creates a Redis connection to store and fetch `profiles`.
    These consists in adding more custom fields to a discord_id according to
    Kernel Concept's works. The code itself is pretty self-explanatory so take a look.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.redis = self.load() or None

    def load(self, host='127.0.0.1', port=6379):
        """
        Create a connection to redis.

        :param host: Redis' server IP
        :param port: Redis' server port
        :return: Redis connection object.
        """

        connection = redis.StrictRedis(host=host, port=port)
        return connection

    @commands.command()
    async def init(self):
        count = 0
        for member in self.bot.server.members:
            person = Person(member.id, self.redis)
            if person.was_just_created:
                count += 1
        if count:
            if count == 1:
                await self.bot.reply(text.INIT_ONE, delete_after=MESSAGE_DELETE_AFTER)
            await self.bot.reply(text.INIT_MULTIPLE.format(count), delete_after=MESSAGE_DELETE_AFTER)
        else:
            await self.bot.reply(text.INIT_NOBODY, delete_after=MESSAGE_DELETE_AFTER)

    @commands.command(pass_context=True, aliases=['bonbonalafraise'])
    async def reset(self, ctx: commands.Context):
        Person(ctx.message.author.id, self.redis).reset()
        await self.bot.reply(text.RESET, delete_after=MESSAGE_DELETE_AFTER)

    @commands.command(pass_context=True, aliases=['doom'])
    async def cleanse(self, ctx: commands.Context):
        if has_admin(self.bot.server, ctx.message.author):
            for member in self.bot.server.members:
                Person(member.id, self.redis).reset()
            await self.bot.reply(text.CLEANSE, delete_after=MESSAGE_DELETE_AFTER)
        else:
            await self.bot.reply(text.NO_RIGHTS, delete_after=MESSAGE_DELETE_AFTER)

    @commands.command(pass_context=True, aliases=['profil', 'carte', 'card'])
    async def profile(self, ctx: commands.Context, member_id: str = None):
        member = None
        if member_id:
            member = enrich_user_id(self.bot.server, member_id)
        profile = member or ctx.message.author
        redis_profile = Person(profile.id, self.redis)
        profile_title = redis_profile.title
        profile_thanks = redis_profile.thanks_count
        profile_desc = redis_profile.desc
        profile_disp = redis_profile.available
        profile_badges = redis_profile.badges
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
        )
        if picture:
            await self.bot.send_file(
                ctx.message.channel,
                picture,
                content=text.PROFILE_SUCCESS.format(profile),
            )
        else:
            await self.bot.reply(text.PROFILE_FAILURE, delete_after=MESSAGE_DELETE_AFTER)

    @commands.command(pass_context=True, aliases=['merci'])
    async def thanks(self, ctx: commands.Context, member: str = None, reason: str = None):
        if member:
            user = enrich_user_id(self.bot.server, member) or ''
            if user.id == ctx.message.author.id:
                await self.bot.reply(text.THANKS_SELF, delete_after=MESSAGE_DELETE_AFTER)
            else:
                person = Person(user.id, self.redis)
                thanks_count = person.thanks()
                if reason:
                    await self.bot.reply(text.THANKS_ACTION_MSG.format(
                        user.mention,
                        thanks_count,
                        reason,
                    ), delete_after=MESSAGE_DELETE_AFTER)
                else:
                    await self.bot.reply(text.THANKS_ACTION.format(
                        user.mention,
                        thanks_count
                    ), delete_after=MESSAGE_DELETE_AFTER)
        else:
            person = Person(ctx.message.author.id, self.redis)
            thanks_count = person.fetch('thanks')
            if thanks_count:
                thanks_count = int(thanks_count.decode('utf-8'))
                await self.bot.reply(text.THANKS.format(thanks_count), delete_after=MESSAGE_DELETE_AFTER)
            else:
                await self.bot.reply(text.THANKS_NONE, delete_after=MESSAGE_DELETE_AFTER)

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
                    if Person(member.id, self.redis).available:
                        if len(output + '\n+ {}'.format(text.AVAILABILITY_TRUE.format(member))) >= 1800:
                            await self.bot.reply(output, delete_after=MESSAGE_DELETE_AFTER)
                            output = '```diff'
                        output += '\n+ {}'.format(text.AVAILABILITY_TRUE.format(member))
            output += '```'
            await self.bot.reply(output, delete_after=MESSAGE_DELETE_AFTER)
        elif cmd == 'oui' or cmd == 'non':
            r = Person(ctx.message.author.id, self.redis).set_availability(cmd)
            await self.bot.reply(text.AVAILABILITY_CHANGE.format(
                ctx.message.author
            ), delete_after=MESSAGE_DELETE_AFTER)
        else:
            user = enrich_user_id(self.bot.server, cmd)
            if user:
                if Person(user.id, self.redis).available:
                    output += '\n+ {}'.format(text.AVAILABILITY_TRUE.format(user))
                else:
                    output += '\n- {}'.format(text.AVAILABILITY_FALSE.format(user))
                if args:
                    for arg in args:
                        user = enrich_user_id(self.bot.server, arg)
                        if user:
                            if Person(user.id, self.redis).available:
                                output += '\n+ {}'.format(text.AVAILABILITY_TRUE.format(user))
                            else:
                                output += '\n- {}'.format(text.AVAILABILITY_FALSE.format(user))
                        else:
                            pass
                output += '\n```'
                await self.bot.reply(output, delete_after=MESSAGE_DELETE_AFTER)
            else:
                await self.bot.reply(text.AVAILABILITY_WRONG_ARGS, delete_after=MESSAGE_DELETE_AFTER)

    @commands.command(pass_context=True, aliases=['titre', 'title'])
    async def nick(self, ctx: commands.Context, cmd: str = None, input_title: str = None):
        if cmd:
            if cmd.startswith('<'):
                enriched_user = enrich_user_id(self.bot.server, cmd)
                user_title = Person(enriched_user.id, self.redis).fetch('title')
                if not user_title:
                    await self.bot.reply(text.NO_NICK, delete_after=MESSAGE_DELETE_AFTER)
                else:
                    await self.bot.reply(text.HAS_NICK.format(
                        enriched_user.mention,
                        user_title.decode('utf-8')
                    ), delete_after=MESSAGE_DELETE_AFTER)
            if cmd == 'edit':
                if not input_title:
                    await self.bot.reply(text.USAGE_NICK, delete_after=MESSAGE_DELETE_AFTER)
                else:
                    if len(input_title) > 24:
                        await self.bot.reply(text.TOO_LONG_NICK, delete_after=MESSAGE_DELETE_AFTER)
                    else:
                        title = re.sub('[`\'"@&^%$!*()+=-]', '', input_title)
                        Person(ctx.message.author.id, self.redis).update('title', title)
                        await self.bot.reply(text.UPDATED_NICK.format(title), delete_after=MESSAGE_DELETE_AFTER)
        else:
            author = ctx.message.author
            user_title = Person(author.id, self.redis).title
            if not user_title:
                await self.bot.reply(text.NO_SELF_NICK, delete_after=MESSAGE_DELETE_AFTER)
            else:
                await self.bot.reply(text.HAS_SELF_NICK.format(
                    author.mention,
                    user_title.decode('utf-8')
                ), delete_after=MESSAGE_DELETE_AFTER)

    @commands.command(pass_context=True, aliases=['description'])
    async def desc(self, ctx: commands.Context, cmd: str = None, input_desc: str = None):
        if cmd:
            if cmd.startswith('<'):
                enriched_user = enrich_user_id(self.bot.server, cmd)
                user_desc = Person(enriched_user.id, self.redis).fetch('desc')
                if not user_desc:
                    await self.bot.reply(text.NO_DESC, delete_after=MESSAGE_DELETE_AFTER)
                else:
                    await self.bot.reply(text.HAS_DESC.format(
                        enriched_user.mention,
                        user_desc.decode('utf-8')
                    ), delete_after=MESSAGE_DELETE_AFTER)
            if cmd == 'edit':
                if not input_desc:
                    await self.bot.reply(text.USAGE_DESC, delete_after=MESSAGE_DELETE_AFTER)
                else:
                    if len(input_desc) > 150:
                        await self.bot.reply(text.TOO_LONG_DESC, delete_after=MESSAGE_DELETE_AFTER)
                    else:
                        Person(ctx.message.author.id, self.redis).update('desc', input_desc)
                        await self.bot.reply(text.UPDATED_DESC.format(input_desc), delete_after=MESSAGE_DELETE_AFTER)
        else:
            author = ctx.message.author
            user_desc = Person(author.id, self.redis).desc
            if not user_desc:
                await self.bot.reply(text.NO_SELF_DESC, delete_after=MESSAGE_DELETE_AFTER)
            else:
                await self.bot.reply(text.HAS_SELF_DESC.format(
                    user_desc.decode('utf-8')), delete_after=MESSAGE_DELETE_AFTER)

    @commands.command()
    async def badge(self, member):
        user = enrich_user_id(self.bot.server, member)
        if user:
            if Person(user.id, self.redis).badges:
                badges = [Badge(b, self.redis) for b in Person(user.id, self.redis).badges]
                output = '```\n'
                for badge in badges:
                    output += '- {}: {}\n{}\n\n'.format(
                        badge.item_id,
                        badge.name,
                        badge.desc
                    )
                output += '```'
                await self.bot.reply('{} dispose des badges suivants: \n\n{}'.format(user.name, output))
            else:
                await self.bot.reply('{} n\'a pas de badges.'.format(user.name))
        elif member.startswith('<@&'):
            await self.bot.reply('cette commande ne fonctionne pas pour les rôles.')
        else:
            await self.bot.reply('cette personne n\'existe pas dans ce serveur.')

    @commands.command()
    async def see(self, badge_id):
        badge = Badge(badge_id, self.redis)
        if badge.exists:
            await self.bot.reply('{}:\n\n{}'.format(badge.name, badge.desc))
        else:
            await self.bot.reply('ce badge n\'existe pas (ou tu n\'as simplement pas donné un ID de badge).')
