"""Common functions for charts"""
from __future__ import annotations

import dtat.palette as palette
from dtat.types import CustomizedMarker, CustomizedTrace


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
        },
    }
