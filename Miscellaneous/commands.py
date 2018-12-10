from Miscellaneous.config import *
from Miscellaneous.controller import get_xkcd_url, get_dustey_phrase, get_wormhole_stats, get_server_status
import random


class MiscBot:
    def __init__(self, slackbot):

        @slackbot.command('xkcd', help='Display an XKCD webcomic. {}'.format(XKCD_USAGE))
        def xkcd(channel, arg, user):
            if arg:
                args = arg.split(' ', -1)
                if len(args) == 1:
                    message = get_xkcd_url(args[0])
                else:
                    message = 'Invalid number of arguments. {}'.format(XKCD_USAGE)
            else:
                message = get_xkcd_url('random')

            return slackbot.post_message(channel, message)


        @slackbot.command('dooster', help='Ask the Dooster a question! {}'.format(NICE_USAGE))
        def dooster(channel, arg, user):
            slackbot.mimic_user('U6VJLPC1G')
            message = get_dustey_phrase()

            return slackbot.post_message(channel, message, as_user=False)


        @slackbot.command('8ball', help='Need an answer to a yes or no question quickly? {}'.format(EIGHTBALL_USAGE))
        def eightball(channel, arg, user):
            if arg.endswith('?'):
                message = random.choice(EIGHTBALL_VALID_QUESTION)
            else:
                message = random.choice(EIGHTBALL_INVALID_QUESTION)

            return slackbot.post_message(channel, message)

        @slackbot.command('wh', help='Find information on a wormhole type! {}'.format(WH_USAGE), aliases=['wormhole'])
        def wormhole(channel, arg, user):
            if arg:
                wormhole_id = arg.upper()
                if wormhole_id == 'K162':
                    message = K162ERROR
                else:
                    wh_info = get_wormhole_stats(wormhole_id)
                    if wh_info:
                        message = WORMHOLE_ATTR.format(wormhole_id=wormhole_id, leads_to=wh_info["leadsTo"],
                                                       jump_mass=wh_info["jumpMass"],
                                                       total_mass=wh_info["totalMass"],
                                                       lifetime=wh_info["maxLifetime"])
                    else:
                        message = "Wormhole type not found"
            else:
                message = "Must supply wormhole ID {}".format(WH_USAGE)

            return slackbot.post_message(channel, message)

        @slackbot.command('status', help="EVE Server status. {}".format(STATUS_USAGE))
        def status(channel, arg):
            if arg == 'sisi':
                result = get_server_status('singularity')
            else:
                result = get_server_status()

            print(result)

            return slackbot.post_message(channel, '', attachments=[result])
