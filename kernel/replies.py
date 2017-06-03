from discord.ext import commands
import discord

REPLIES = {
    'musicbot/playdeny': '{}'
}

async def reply(message: discord.Message, bot: commands.Bot) -> bool:
    """
    Reply to certain non-command messages.
    TODO: Probably needs a whole class since we will handle reactions and other stuff as well.

    :param message: The message to reply to.
    :param bot: The bot instance to reply.
    :return: True if the message has to be processed here, False if not.
    """
    if message.content == "Can't stop if I'm not playing." and message.author.name == 'Kernel Jukebox':
        await bot.send_file(message.channel,
                            "sources/braingame.jpg",
                            content=REPLIES['musicbot/playdeny'].format(message.author.mention))
        return True

    if message.content.upper() == "SQUISHY":
        await bot.add_reaction(message, 'squishy')
        return True

    else:
        return False
