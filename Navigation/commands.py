from Navigation.config import DIST_USAGE, RANGE_USAGE
from Navigation.controller import get_dotlan_map, get_jump_dist


# TODO All these nested ifs are gross. Is there a better way?


class NavBot:
    def __init__(self, bot):

        @bot.command('distance', help='Show distance between 2 systems. {}'.format(DIST_USAGE), aliases=['range'])
        async def distance(channel, arg, user):
            if arg:
                args = arg.split(' ', 1)
                if len(args) == 2:
                    dist = get_jump_dist(args)
                    if dist and dist > 0:
                        message = args[0].upper() + ' to ' + args[1].upper() + ': ' + '{:,.2f}ly'.format(dist)
                    else:
                        message = 'Invalid arguments. {}'.format(DIST_USAGE)
                else:
                    message = 'Invalid number of arguments. {}'.format(DIST_USAGE)
            else:
                message = 'Invalid number of systems. {}'.format(DIST_USAGE)

            return await bot.post_message(channel, message)

        @bot.command('rangemap', help='Get a dotlan map showing all locations in jump range from a system. '
                                           '{}'.format(RANGE_USAGE))
        async def rangemap(channel, arg, user):
            if arg:
                args = arg.split(' ', -1)
                if len(args) == 3:
                    url = get_dotlan_map(args)
                    if url:
                        message = url
                    else:
                        message = 'Invalid arguments. {}'.format(RANGE_USAGE)
                else:
                    message = 'Invalid number of arguments. {}'.format(DIST_USAGE)
            else:
                message = 'Invalid number of arguments. {}'.format(RANGE_USAGE)

            return await bot.post_message(channel, message)
