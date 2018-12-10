import Fleetup.controller as fleetup


class FleetupBot:
    def __init__(self, slackbot):

        @slackbot.command('doctrines', help='Show all available doctrines')
        def doctrines(channel, arg, user):
            all_doctrines = fleetup.get_doctrines()
            slackbot.post_message(channel, '\n'.join(all_doctrines.keys()))

        @slackbot.command('doctrine', help='Show fitting names for a doctrine. Usage: *doctrine _name_*')
        def doctrine(channel, arg, user):
            if arg:
                message, doctrine_fittings = fleetup.get_fittings(doctrine=arg)
                message = '\n'.join([message] + list(doctrine_fittings.keys()))
            else:
                message = "No doctrine name supplied. Usage: *doctrine _name_*"

            return slackbot.post_message(channel, message)

        @slackbot.command('fittings', help='Show all available fittings')
        def fittings(channel, arg, user):
            all_fittings = fleetup.get_fittings()
            if arg:
                filtered = [f for f in all_fittings.keys() if all(w in f.lower() for w in arg.lower().split())]
                if len(filtered) == 0:
                    message = 'No fittings found for keywords {}'.format(arg)
                else:
                    message = '\n'.join(filtered)
            else:
                message = '\n'.join(all_fittings.keys())

            return slackbot.post_message(channel, message)

        @slackbot.command('fitting', help='Show fitting details. Usage: *fitting _name_*')
        def fitting(channel, arg, user):
            if arg:
                fitting_details = fleetup.get_fitting(arg)
                message = fitting_details
            else:
                message = "No fitting name supplied. Usage: *fitting _name_*"

            return slackbot.post_message(channel, message)
