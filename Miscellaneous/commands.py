from Core._config import BLACKLIST
from Miscellaneous.config import XKCD_USAGE, NICE_USAGE
from Miscellaneous.controller import get_xkcd_url


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

        @slackbot.command('nice', help='Receive praise from the Dooster! {}'.format(NICE_USAGE))
        def nice(channel, arg):
            slackbot.set_typing(channel)
            userlist = slackbot.slack_client.api_call("users.list")['members']
            message = 'Nice'
            for user_entry in userlist:
                if 'U6VJLPC1G' in user_entry['id']:
                    slackbot.personality = {"name": user_entry['profile']['real_name_normalized'],
                                            "icon_url": user_entry['profile']['image_72']}
                    return slackbot.post_message(channel, message, as_user=False)

            return slackbot.post_message(channel, message)
