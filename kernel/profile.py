"""
Du Python, encore et toujours.

profile.py
"""

from raven import Client
from discord.ext import commands
from kernel import enrich_user_id
from typing import List, Union
import redis
import re

sentry = Client('https://62ffbf83e1204334ae60fd85305239f2:c8033d9c0312464f87593d93b7040a11@sentry.io/154891')

USER_DOESNT_EXIST = "Cet utilisateur n'existe pas (ou je n'ai, du moins, pas réussi à le trouver dans ce channel)."
NO_DESC = "Cet utilisateur n'a pas de description."
NO_SELF_DESC = "Tu n'as pas de description."
NO_TITLE = "Cet utilisateur n'a pas de titre."
NO_SELF_TITLE = "Tu n'as pas de titre, pauvre paysan que tu es."
THANKS = "Tu as bien remercié {} ! (déjà remercié {} fois) ```{}```"
THANKS_NO_MSG = "Tu as bien remercié {} ! (déjà remercié {} fois)"
AVAILABILITY_CHANGE = "{0.mention} Tu as bien changé ta disponibilité."
AVAILABILITY_TRUE = "{0.name} est défini comme disponible."
AVAILABILITY_FALSE = "{0.name} est défini comme indisponible ou n'a pas spécifié sa disponibilité."
AVAILABILITY_WRONG_ARGS = "Tu dois fournir une disponibilité (oui/non/y/n) ou un/des utilisateurs."

class Person:
    """
    Person class
    """
    def __init__(self, discord_id: str, redis):
        self.discord_id = discord_id

        #  Set the redis key to True if profile doesn't exist.
        self.init()

    @property
    def exists(self) -> bool:
        return self.redis.get('person/{}'.format(self.discord_id))

    def init(self) -> bool:
        if not self.exists:
            self.redis.set('person/{}'.format(self.discord_id), True)
            return True
        return False

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
            r = r.decode('utf-8')
            print(r)
            if 'False' in r:
                return False
            elif 'True' in r:
                return True
        else:
            return False

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

    def fetch(self, key) -> Union[str, int]:
        value = self.redis.get('person/{}/{}'.format(
            self.discord_id,
            key
        ))
        return value

    def update(self, key, value):
        self.redis.set('person/{}/{}'.format(
            self.discord_id,
            key
        ), value)


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

    @commands.command(pass_context=True)
    async def init(self, ctx: commands.Context):
        count = 0
        for member in self.bot.server.members:
            person = Person(member.id, self.redis)
            if person.init():
                count += 1
        await self.bot.send_message(ctx.message.channel, 'La base de données est maintenant à jour avec {} nouveaux profils.'.format(
            count
        ))

    @commands.command(pass_context=True)
    async def reset(self, ctx: commands.Context):
        pass

    @commands.command(pass_context=True, aliases=['merci'])
    async def thanks(self, ctx: commands.Context, member: str = None, reason: str = None):
        if member:
            user = enrich_user_id(self.bot.server, member) or ''
            if user.id == ctx.message.author.id:
                await self.bot.send_message(ctx.message.channel, 'Bien l\'amour propre ou ..?')
            else:
                person = Person(user.id, self.redis)
                thanks_count = person.thanks()
                if reason:
                    await self.bot.send_message(ctx.message.channel, THANKS.format(
                        user.mention,
                        thanks_count,
                        self.format(reason)
                    ))
                else:
                    await self.bot.send_message(ctx.message.channel, THANKS_NO_MSG.format(
                        user.mention,
                        thanks_count
                    ))
        else:
            person = Person(ctx.message.author.id, self.redis)
            thanks_count = person.fetch('thanks')
            if thanks_count:
                thanks_count = int(thanks_count.decode('utf-8'))
                await self.bot.send_message(ctx.message.channel, 'Tu as été remercié {} fois !'.format(thanks_count))
            else:
                await self.bot.send_message(ctx.message.channel,
                                            'Tu n\'as jamais été remercié, être inutile que tu es.')

    @commands.command(pass_context=True, aliases=['dispo'])
    async def available(self, ctx: commands.Context, cmd: str, *args):
        if cmd == 'oui' or cmd == 'non':
            r = Person(ctx.message.author.id, self.redis).set_availability(cmd)
            await self.bot.send_message(ctx.message.channel, AVAILABILITY_CHANGE.format(
                ctx.message.author
            ))
        else:
            output = '```diff'
            user = enrich_user_id(self.bot.server, cmd)
            if user:
                if Person(user.id, self.redis).available:
                    output += '\n+ {}'.format(AVAILABILITY_TRUE.format(user))
                else:
                    output += '\n- {}'.format(AVAILABILITY_FALSE.format(user))
                if args:
                    for arg in args:
                        user = enrich_user_id(self.bot.server, arg)
                        if user:
                            if Person(user.id, self.redis).available:
                                output += '\n+ {}'.format(AVAILABILITY_TRUE.format(user))
                            else:
                                output += '\n- {}'.format(AVAILABILITY_FALSE.format(user))
                        else:
                            pass
                output += '\n```'
                await self.bot.send_message(ctx.message.channel, output)
            else:
                await self.bot.send_message(ctx.message.channel, AVAILABILITY_WRONG_ARGS)

    @commands.command(pass_context=True, aliases=['titre'])
    async def nick(self, ctx: commands.Context, cmd: str = None, input_title: str = None):
        if cmd:
            if cmd.startswith('<'):
                enriched_user = enrich_user_id(self.bot.server, cmd)
                user_title = Person(enriched_user.id, self.redis).fetch('title')
                if not user_title:
                    await self.bot.send_message(ctx.message.channel, NO_TITLE)
                else:
                    await self.bot.send_message(ctx.message.channel, '{} a le titre de {}.'.format(
                        enriched_user.mention,
                        user_title.decode('utf-8')
                    ))
            if cmd == 'edit':
                if not input_title:
                    await self.bot.send_message(ctx.message.channel,
                                                'Tu dois fournir un titre entre guillemets '
                                                '(e.g. : "Mon titre")')
                else:
                    if len(input_title) > 24:
                        await self.bot.send_message(ctx.message.channel,
                                                    'Ton titre doit avoir maximum 24 caractères.')
                    else:
                        title = re.sub('[`\'"@&^%$!*()+=-]', '', input_title)
                        Person(ctx.message.author.id, self.redis).update('title', title)
                        await self.bot.send_message(ctx.message.channel,
                                                    'Tu as maintenant le titre de {}.'.format(
                                                        title
                                                    ))
        else:
            author = ctx.message.author
            user_title = Person(author.id, self.redis).title
            if not user_title:
                await self.bot.send_message(ctx.message.channel, NO_SELF_TITLE)
            else:
                await self.bot.send_message(ctx.message.channel, '{} dispose du titre de {}.'.format(
                    author.mention,
                    user_title.decode('utf-8')
                ))
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def desc(self, ctx: commands.Context, cmd: str = None, input_desc: str = None):
        if cmd:
            if cmd.startswith('<'):
                enriched_user = enrich_user_id(self.bot.server, cmd)
                user_desc = Person(enriched_user.id, self.redis).fetch('desc')
                if not user_desc:
                    await self.bot.send_message(ctx.message.channel, NO_DESC)
                else:
                    await self.bot.send_message(ctx.message.channel, 'Description de {} : ```diff\n{}\n```'.format(
                        enriched_user.mention,
                        user_desc.decode('utf-8')
                    ))
            if cmd == 'edit':
                if not input_desc:
                    await self.bot.send_message(ctx.message.channel,
                                                'Tu dois fournir une description entre guillemets '
                                                '(e.g. : "Ma description")')
                else:
                    if len(input_desc) > 360:
                        await self.bot.send_message(ctx.message.channel,
                                                    'Ta description doit faire maximum 360 caractères.')
                    else:
                        desc = self.format(input_desc)
                        Person(ctx.message.author.id, self.redis).update('desc', desc)
                        await self.bot.send_message(ctx.message.author,
                                                    'Je vois. J\'approuve donc ta demande en t\'assignant cette description : ```diff\n{}\n```'.format(
                                                        self.format(desc)
                                                    ))
        else:
            author = ctx.message.author
            user_desc = Person(author.id, self.redis).desc
            if not user_desc:
                await self.bot.send_message(ctx.message.channel, NO_SELF_DESC)
            else:
                await self.bot.send_message(ctx.message.channel, 'Description de {} : ```diff\n{}\n```'.format(
                    author.mention,
                    user_desc.decode('utf-8')
                ))
        await self.bot.delete_message(ctx.message)

    def format(self, message):
        output = re.sub('`', '', message)
        output = re.sub('[_]', '\n', output)
        return output

    @commands.command(pass_context=True)
    async def badge(self, ctx: commands.Context, member):
        pass
