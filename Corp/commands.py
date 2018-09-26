from Corp._config import *
from Corp.controller import submit_srp, valid_lossmail, valid_character


class CorpBot:
    def __init__(self, slackbot):

        @slackbot.command('srp', help='Submit for SRP from within slack. {}'.format(SRP_USAGE))
        def srp(channel, arg):
            try:
                args = arg.split(",", 2)
                url = args[1].strip().replace('<', '').replace('>', '')
                loss_valid = valid_lossmail(url)
                character_valid = valid_character(args[0])
                if loss_valid and character_valid:
                    if len(args) == 3:
                        submit_srp(args[0], url, args[2])
                    else:
                        submit_srp(args[0], url)
                    message = "SRP submitted."
                elif not loss_valid:
                    message = 'Invalid lossmail, please try again.'.format(SRP_USAGE)
                elif not character_valid:
                    message = 'Invalid character, please try again.'.format(SRP_USAGE)
            except (AttributeError, IndexError) as e:  # If user doesn't enter 2 or 3 arguments (CSV's)
                print(e)
                message = 'Invalid arguments. {}'.format(SRP_USAGE)

            return slackbot.post_message(channel, message)
