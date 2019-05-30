import logging
import sys

from Core._config import TOKEN
from Core.discord_bot import DiscordBot
from discord.ext import commands

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create a file handler
# handler = logging.FileHandler('debug.log')
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

# create the bot instance
client = commands.Bot(command_prefix='!')
bot = DiscordBot(client=client, logger=logger)


@bot.command('ping', help='Check boss presence')
async def ping(channel, arg, user):
    if arg and '@' not in arg:
        message = arg
    elif not arg:
        message = 'Pong'
    else:
        message = user.mention

    return await bot.post_message(channel, message)


@bot.command('help', help='Shows list of supported commands.', aliases=['halp'])
async def help(channel, arg, user):
    if arg is None:
        message = 'Supported commands: *{}*.\n*help _command_* for detailed help.'.format(
            ', '.join(bot._commands.keys()))
    elif arg in bot._command_help:
        message = bot._command_help[arg]
    else:
        message = 'No help entry found for {}'.format(arg)

    return await bot.post_message(channel, message)


# TODO Refactor all commands to take a context argument rather than separate channel, args, user arguments
if __name__ == '__main__':
    from Navigation.commands import NavBot
    from Miscellaneous.commands import MiscBot
    from Market.commands import MarketBot
    from Fleetup.commands import FleetupBot
    from Corp.commands import CorpBot

    nav_commands = NavBot(bot)
    misc_commands = MiscBot(bot)
    market_commands = MarketBot(bot)
    fleetup_commands = FleetupBot(bot)
    corp_commands = CorpBot(bot)

    bot.run(TOKEN)
