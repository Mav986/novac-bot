from Miscellaneous.config import *
from Miscellaneous.controller import get_xkcd_url, get_wormhole_stats, get_server_status
import random


class MiscBot:
    def __init__(self, bot):

        @bot.command('xkcd', help='Display an XKCD webcomic. {}'.format(XKCD_USAGE))
        async def xkcd(channel, arg, user):
            if arg:
                args = arg.split(' ', -1)
                if len(args) == 1:
                    message = get_xkcd_url(args[0])
                else:
                    message = 'Invalid number of arguments. {}'.format(XKCD_USAGE)
            else:
                message = get_xkcd_url('random')

            return await bot.post_message(channel, message)


        '''
        Temporarily disabled until solution for posting as other users is found
        '''
        # async @bot.command('dooster', help='Ask the Dooster a question! {}'.format(NICE_USAGE))
        # def dooster(channel, arg, user):
        #     bot.mimic_user('U6VJLPC1G')
        #     message = get_dustey_phrase()
        #
        #     return bot.post_message(channel, message, as_user=False)


        @bot.command('8ball', help='Need an answer to a yes or no question quickly? {}'.format(EIGHTBALL_USAGE))
        async def eightball(channel, arg, user):
            if arg.endswith('?'):
                message = random.choice(EIGHTBALL_VALID_QUESTION)
            else:
                message = random.choice(EIGHTBALL_INVALID_QUESTION)

            return await bot.post_message(channel, message)

        @bot.command('wh', help='Find information on a wormhole type! {}'.format(WH_USAGE), aliases=['wormhole'])
        async def wormhole(channel, arg, user):
            if arg:
                wormhole_id = arg.upper()
                if wormhole_id == 'K162':
                    message = K162ERROR
                else:
                    wh_info = get_wormhole_stats(wormhole_id)
                    if wh_info and wh_info.get('regen_mass') == 0:
                        message = WORMHOLE_ATTR.format(
                            wormhole_id=wormhole_id, leads_to=wh_info.get('leads_to'),
                            jump_mass=wh_info.get('jump_mass'),
                            total_mass=wh_info.get('total_mass'),
                            lifetime=wh_info.get('lifetime'))

                    elif wh_info and wh_info.get('regen_mass') > 0:
                        message = WORMHOLE_ATTR_REGEN.format(
                            wormhole_id=wormhole_id, leads_to=wh_info.get('leads_to'),
                            jump_mass=wh_info.get('jump_mass'),
                            total_mass=wh_info.get('total_mass'),
                            regenMass=wh_info.get('regen_mass'),
                            lifetime=wh_info.get('lifetime'))
                    else:
                        message = "Wormhole type not found"
            else:
                message = "Must supply wormhole ID {}".format(WH_USAGE)

            return await bot.post_message(channel, message)

        @bot.command('status', help="EVE Server status. {}".format(STATUS_USAGE))
        async def status(channel, arg, user):
            if arg == 'sisi':
                result = get_server_status('singularity')
            else:
                result = get_server_status()

            return await bot.post_message(channel, '', embed=result)
