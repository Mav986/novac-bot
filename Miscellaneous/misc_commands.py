from Miscellaneous.misc_controller import get_xkcd_url
from Miscellaneous.misc_config import XKCD_USAGE
from Core.config import BLACKLIST


class MiscBot:
    def __init__(self, slackbot):

        @slackbot.command('xkcd', help='Display an XKCD webcomic. {}'.format(XKCD_USAGE))
        def xkcd(channel, arg):
            slackbot.set_typing(channel)
            if arg:
                args = arg.split(' ', -1)
                if len(args) == 1 and not any(element.startswith(BLACKLIST) for element in args):
                    message = get_xkcd_url(args[0])
                elif not len(args) == 1:
                    message = 'Invalid number of arguments. {}'.format(XKCD_USAGE)
                else:
                    message = 'Mentions are not a valid parameter.'
            else:
                message = 'Invalid number of arguments. {}'.format(XKCD_USAGE)

            return slackbot.post_message(channel, message)
