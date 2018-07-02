from Core.config import SLACK_BOT_TOKEN, BLACKLIST
from slackclient import SlackClient
from Core.slack import Slackbot

import logging
import sys

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
slack = SlackClient(SLACK_BOT_TOKEN)
slackbot = Slackbot(slack_client=slack, logger=logger)


@slackbot.command('ping', help='Check boss presence')
def ping(channel, arg):
    if arg and not arg.startswith(BLACKLIST):
        message = arg
    elif not arg:
        message = 'Pong'
    else:
        message = 'Mentions are not a valid parameter.'

    return slackbot.post_message(channel, message)


@slackbot.command('help', help='Shows list of supported commands.')
def help(channel, arg):
    if arg is None:
        message = 'Supported commands: *{}*.\n*help _command_* for detailed help.'.format(
            ', '.join(slackbot._commands.keys()))
    elif arg in slackbot._command_help:
        message = slackbot._command_help[arg]
    else:
        message = 'No help entry found for {}'.format(arg)

    return slackbot.post_message(channel, message)


if __name__ == '__main__':
    from Navigation.nav_commands import NavBot
    from Miscellaneous.misc_commands import MiscBot
    from Market.market_commands import MarketBot
    from Fleetup.fleetup_commands import FleetupBot

    nav_commands = NavBot(slackbot)
    misc_commands = MiscBot(slackbot)
    market_commands = MarketBot(slackbot)
    fleetup_commands = FleetupBot(slackbot)

    slackbot.run()
