from Miscellaneous.config import *
from Miscellaneous.controller import get_xkcd_url
import random


class MiscBot:
    def __init__(self, slackbot):

        @slackbot.command('xkcd', help='Display an XKCD webcomic. {}'.format(XKCD_USAGE))
        def xkcd(channel, arg):
            if arg:
                args = arg.split(' ', -1)
                if len(args) == 1:
                    message = get_xkcd_url(args[0])
                else:
                    message = 'Invalid number of arguments. {}'.format(XKCD_USAGE)
            else:
                message = get_xkcd_url('random')

            return slackbot.post_message(channel, message)

        @slackbot.command('nice', help='Receive praise from the Dooster! {}'.format(NICE_USAGE))
        def nice(channel, arg):
            slackbot.set_personality('U6VJLPC1G')
            message = 'Nice'

            return slackbot.post_message(channel, message, as_user=False)

        @slackbot.command('8ball', help='Need an answer to a yes or no question quickly? {}'.format(EIGHTBALL_USAGE))
        def eightball(channel, arg):
            if arg.endswith('?'):
                message = random.choice(EIGHTBALL_VALID_QUESTION)
            else:
                message = random.choice(EIGHTBALL_INVALID_QUESTION)

            return slackbot.post_message(channel, message)
