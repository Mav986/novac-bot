import Fleetup.controller as fleetup


class FleetupBot:
    def __init__(self, bot):

        @bot.command('doctrines', help='Show all available doctrines')
        async def doctrines(channel, arg, user):
            all_doctrines = fleetup.get_doctrines()
            return await bot.post_message(channel, '\n'.join(all_doctrines.keys()))

        @bot.command('doctrine', help='Show fitting names for a doctrine. Usage: *doctrine _name_*')
        async def doctrine(channel, arg, user):
            if arg:
                message, doctrine_fittings = fleetup.get_fittings(doctrine=arg)
                message = '\n'.join([message] + list(doctrine_fittings.keys()))
            else:
                message = "No doctrine name supplied. Usage: *doctrine _name_*"

            return await bot.post_message(channel, message)

        @bot.command('fittings', help='Show all available fittings')
        async def fittings(channel, arg, user):
            all_fittings = fleetup.get_fittings()
            if arg:
                filtered = [f for f in all_fittings.keys() if all(w in f.lower() for w in arg.lower().split())]
                if len(filtered) == 0:
                    message = 'No fittings found for keywords {}'.format(arg)
                else:
                    message = '\n'.join(filtered)
            else:
                message = '\n'.join(all_fittings.keys())

            return await bot.post_message(channel, message)

        @bot.command('fitting', help='Show fitting details. Usage: *fitting _name_*')
        async def fitting(channel, arg, user):
            if arg:
                fitting_details = fleetup.get_fitting(arg)
                message = fitting_details
            else:
                message = "No fitting name supplied. Usage: *fitting _name_*"

            return await bot.post_message(channel, message)
