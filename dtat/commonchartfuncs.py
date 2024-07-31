"""Common functions for charts"""
from __future__ import annotations
import datetime as dt

import dtat.palette as palette
from dtat.types import CustomizedMarker, CustomizedTrace
import dtat.datachecker as datachecker


def get_plotly_marker_values(customize_dict: CustomizedTrace) -> CustomizedMarker:
    keys = customize_dict.keys()
    if "color" not in keys or customize_dict["color"] is None:
        customize_dict["color"] = "#000000"
    if "symbol" not in keys or customize_dict["symbol"] is None:
        customize_dict["symbol"] = "circle"
    if "size" not in keys or customize_dict["size"] is None:
        customize_dict["size"] = 5
    if "z_var" not in keys:
        customize_dict["z_var"] = None
    if "showscale" not in keys or not isinstance(customize_dict["showscale"], bool):
        customize_dict["showscale"] = False
    if "colorscale" not in keys or customize_dict["colorscale"] is None:
        customize_dict["colorscale"] = palette.make_discrete_colorscale([], [])
    return {
        "size": customize_dict["size"],
        "symbol": customize_dict["symbol"],
        "color": customize_dict["color"],
        "colorscale": customize_dict["colorscale"],
        "showscale": customize_dict["showscale"],
        "line": {
            "width": 0.5 if customize_dict["z_var"] is None else 0,
            "color": palette.get_line_color(customize_dict["color"]),
        }
    }

def make_colorbar_dict(data, z_var) -> dict:
    colorbar = {
        "title": z_var
    }
    if z_var is not None and datachecker.is_time_type(z_var) and 'elapsed_seconds' in data.columns:
        label_alias_dict = {}
        es_min = data["elapsed_seconds"].min()
        es_max = data["elapsed_seconds"].max()
        es_step = (es_max - es_min) / 6
        colorbar['tickmode'] = 'array'
        colorbar['tickvals'] = [
            es_min, 
            es_min + (es_step * 1),
            es_min + (es_step * 2),
            es_min + (es_step * 3),
            es_min + (es_step * 4),
            es_min + (es_step * 5),
            es_max
        ]
        colorbar['ticktext'] = [elapsed_seconds_to_dt_str(d) for d in colorbar['tickvals']]
    return colorbar

def elapsed_seconds_to_dt_str(es_flt) -> str:
    es_dt = dt.datetime(2018, 1, 1) + dt.timedelta(seconds = es_flt)
    es_str = es_dt.strftime('%Y-%jT%H:%M:%S')
    return es_str
