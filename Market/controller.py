import pandas as pd
import numpy as np
import Core.esi as esi


def min_sell_for_types(names, region_id=10000002, station_id=60003760):
    types = [name['id'] for name in names]
    prices = [order for res in esi.get_sell_orders(types, region_id) for order in res]

    df1 = pd.DataFrame.from_records(prices)
    df2 = pd.DataFrame.from_records(names)

    if len(df1) == 0:
        return[(d['name'], None) for d in df1.to_dict(orient='records')]

    data = pd.merge(
        df1[df1.location_id == station_id].groupby('type_id').agg({'price': np.min}).reset_index(),
        df2,
        right_on='id', left_on='type_id', how='inner'
    )

    return [(d['name'], d['price']) for d in data.to_dict(orient='records')]
