"""
ColumnLayer
===========

Real estate values for select properties in Taipei. Data is from 2012-2013.
The height of a column indicates increasing price per unit area, and the color indicates distance from a subway stop.

The real estate valuation data set from UC Irvine's Machine Learning repository, viewable here:

https://archive.ics.uci.edu/ml/datasets/Real+estate+valuation+data+set
"""

import pydeck
import pandas as pd

with open('../../../mapbox_key.txt', 'r') as f:
    mapbox_key = f.readline()
    print('Mapbox key =', mapbox_key)

DATA_URL = "https://raw.githubusercontent.com/ajduberstein/geo_datasets/master/housing.csv"
df = pd.read_csv(DATA_URL)

view = pydeck.data_utils.compute_view(df[["lng", "lat"]])
view.pitch = 75
view.bearing = 60

column_layer = pydeck.Layer(
    "ColumnLayer",
    data=df,
    get_position=["lng", "lat"],
    get_elevation="price_per_unit_area",
    elevation_scale=100,
    radius=50,
    get_fill_color=["mrt_distance * 10", "mrt_distance", "mrt_distance * 10", 140],
    pickable=True,
    auto_highlight=True,
)

tooltip = {
    "html": "<b>{mrt_distance}</b> meters away from an MRT station, costs <b>{price_per_unit_area}</b> NTD/sqm",
    "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
}

r = pydeck.Deck(
    column_layer, initial_view_state=view, tooltip=tooltip, map_style="mapbox://styles/mapbox/satellite-v9", mapbox_key=mapbox_key)

r.to_html("column_layer.html", notebook_display=False)
