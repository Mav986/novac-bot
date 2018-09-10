import numpy as np

import Core.esi as esi
import Market.controller as market

hubs = [
    {'name': 'Amarr', 'region_id': 10000043, 'station_id': 60008494},
    {'name': 'Jita', 'region_id': 10000002, 'station_id': 60003760},
    {'name': 'Dodixie', 'region_id': 10000032, 'station_id': 60011866}
]


class MarketBot:
    def __init__(self, slackbot):

        @slackbot.command('price', help='Get lowest sell price in Jita 4-4')
        def price(channel, arg):
            slackbot.set_typing(channel)
            if arg:
                types = []
                for type in arg.splitlines():
                    if len(type) < 3:
                        continue
                    types.extend(esi.search_type(type))
                if len(types) > 50:
                    message = 'Too many possible matches ({}). Aborting.'.format(len(types))
                elif len(types) > 0:
                    names = esi.names(types)
                    names = list(filter(lambda x: filter_types(arg, x['name']), names))
                    prices = market.min_sell_for_types(names)
                    items = '\n'.join(['{}:\t{:0,.2f} ISK'.format(name, price) for name, price in prices])
                    total = '\n\nSet total: *{:0,.2f} ISK*'.format(np.sum(price for name, price in prices))
                    message = '*Lowest sell orders in Jita 4-4:*\n{}{}'.format(items, total if len(prices) > 1 else '')
                else:
                    message = 'No results found'
            else:
                message = 'No query supplied. Usage: *price _item(s)_*'

            return slackbot.post_message(channel, message)

        @slackbot.command('pricehub', help='Get Prices in market hubs')
        def pricehub(channel, arg):
            slackbot.set_typing(channel)
            if arg:
                types = []

                for type in arg.splitlines():
                    if len(type) < 3:
                        continue
                    types.extend(esi.search_type(type) or [])
                if len(types) > 50:
                    message = 'Too many possible matches ({}). Aborting.'.format(len(types))
                elif len(types) > 0:
                    names = esi.names(types)
                    names = list(filter(lambda x: filter_types(arg.lower(), x['name']), names))
                    # TODO: Refactor. This is horrifying.
                    totals = []
                    for hub in hubs:
                        prices = market.min_sell_for_types(names, hub['region_id'], hub['station_id'])
                        totals.append('{}: *{:,.2f} ISK* ({}/{} items)'.format(
                            hub['name'],
                            np.sum(price for name, price in prices),
                            len(prices),
                            len(names)
                        ))
                    message = '{}\n_______________________\n{}'.format('\n'.join(set(name['name'] for name in names)),
                                                                       '\n'.join(totals) if len(
                                                                           totals) > 0 else 'No orders found')
                else:
                    message = 'No results found'
            else:
                message = 'No query supplied. Usage: *pricehub _item(s)_*'

            return slackbot.post_message(channel, message)

        def filter_types(search, name):
            blacklist = ['Blueprint', 'SKIN', 'Issue']
            for term in blacklist:
                if term.lower() in name.lower() and not term.lower() in search.lower():
                    return False

            return True
