"""Default color palette for charts"""
from __future__ import annotations

from typing import Optional, Tuple, cast

"""Default accessible palette"""
DEFAULT_BG_COLOR = "#fefefe"
DEFAULT_AXIS_LINE_COLOR = "#DDE1E7"
default_colors = {
    "#E55166": {"line_color": "#CA243C", "name": "Dark-Red"},
    "#FC8156": {"line_color": "#FC5E24", "name": "Dark-Orange"},
    "#FFF000": {"line_color": "#FFE100", "name": "Dark-Yellow"},
    "#CDD968": {"line_color": "#B9D11B", "name": "Dark-Olive"},
    "#00CAC3": {"line_color": "#00B1BB", "name": "Dark-Teal"},
    "#42D8FF": {"line_color": "#00B6E5", "name": "Dark-Cyan"},
    "#42A5FF": {"line_color": "#0073FF", "name": "Dark-Blue"},
    "#6F5BBF": {"line_color": "#4D25BF", "name": "Dark-Purple"},
    "#9D4280": {"line_color": "#920060", "name": "Dark-Wine-Red"},
    "#711A2E": {"line_color": "#490016", "name": "Dark-Raspberry"},
    "#373737": {"line_color": "#000000", "name": "Dark-Grey"},
    "#FF909F": {"line_color": "#FF6A7F", "name": "Med-Red"},
    "#FDBAA2": {"line_color": "#FF9570", "name": "Med-Orange"},
    "#FFF773": {"line_color": "#FFE900", "name": "Med-Yellow"},
    "#E3EAAC": {"line_color": "#CDD968", "name": "Med-Olive"},
    "#73E2DE": {"line_color": "#00CAC3", "name": "Med-Teal"},
    "#97EAFF": {"line_color": "#42D8FF", "name": "Med-Cyan"},
    "#97CEFF": {"line_color": "#60B3FF", "name": "Med-Blue"},
    "#B0A5DC": {"line_color": "#8773D6", "name": "Med-Purple"},
    "#C997B9": {"line_color": "#BC64A0", "name": "Med-Wine-Red"},
    "#B1818C": {"line_color": "#994155", "name": "Med-Raspberry"},
    # Commenting out because it makes one too many lines, and we have a grey in the instruments
    # '#959595': {'line_color': '#2C2C2C', 'name': 'Med-Grey'},
    "#FFC2CB": {"line_color": "#FF9DAA", "name": "Light-Red"},
    "#FED9CC": {"line_color": "#FDBAA2", "name": "Light-Orange"},
    "#FFFAB3": {"line_color": "#FFF21B", "name": "Light-Yellow"},
    "#F0F4D2": {"line_color": "#E3EAAC", "name": "Light-Olive"},
    "#B3EFED": {"line_color": "#73E2DE", "name": "Light-Teal"},
    "#C6F3FF": {"line_color": "#97EAFF", "name": "Light-Cyan"},
    "#C6E4FF": {"line_color": "#97CEFF", "name": "Light-Blue"},
    "#D4CEEC": {"line_color": "#B0A5DC", "name": "Light-Purple"},
    "#E2C6D9": {"line_color": "#C997B9", "name": "Light-Wine-Red"},
    "#D4BAC0": {"line_color": "#B1818C", "name": "Light-Raspberry"},
    "#C0C0C0": {"line_color": "#959595", "name": "Light-Grey"},
    "#EF8536": {"line_color": "#E06900", "name": "SUDA"},
    "#5494C4": {"line_color": "#0971AE", "name": "ECM"},
    "#F3BE49": {"line_color": "#EEA900", "name": "PIMS"},
    "#83B24E": {"line_color": "#589E1A", "name": "MASPEX"},
    "#9F7D58": {"line_color": "#805325", "name": "ETHEMIS"},
    "#D1352B": {"line_color": "#AC0000", "name": "MISE"},
    "#E3CAA6": {"line_color": "#D2AB79", "name": "UVS"},
    "#8347AA": {"line_color": "#7616A1", "name": "EISNAC"},
    "#C5B3D3": {"line_color": "#B894CB", "name": "EISWAC"},
    "#7F7F7F": {"line_color": "#616161", "name": "REASON"},
}


def get_default_colors():
    """Returns a list of the hex values with default colors"""
    return list(default_colors.keys())


def get_default_color_options():
    """Creates properly formatted dropdown labels for the default color options"""
    labels = []
    for color in default_colors.keys():
        labels.append(
            {
                "label": "",
                "value": color,
                "className": str(
                    default_colors[color]["name"]
                    + "-color-option color-swatch-option fa fa-circle"
                ),
                "title": default_colors[color]["name"],
            }
        )
    return labels


def get_default_shape_options():
    """Creates properly formatted dropdown labels for the default shape options"""
    labels = []
    for shape in [
        ["circle", "circle-icon-option"],
        ["circle-open", "circle-open-icon-option"],
        ["square", "square-icon-option"],
        ["square-open", "square-open-icon-option"],
        ["diamond", "diamond-icon-option"],
        ["diamond-open", "diamond-open-icon-option"],
        ["triangle-up", "triangle-up-icon-option"],
        ["triangle-up-open", "triangle-up-open-icon-option"],
        ["asterisk-open", "fa fa-asterisk"],
        ["cross-thin-open", "fa fa-plus"],
    ]:
        labels.append(
            {
                "label": "",
                "value": shape[0],
                "className": str("color-swatch-option fa " + shape[1]),
                "title": shape[0],
            }
        )
    return labels


def get_line_color(color):
    """Tries to return a related line color.
    If not found, returns pure black."""
    if (
        color is None
        or not isinstance(color, str)
        or color not in default_colors.keys()
    ):
        return "#000000"
    return default_colors[color]["line_color"]


def pop_next_color(
    unassigned_colors=None,
) -> Tuple[str, list]:
    if unassigned_colors is None or not unassigned_colors:
        unassigned_colors = list(default_colors)
    return unassigned_colors.pop(0), unassigned_colors


def remove_unseen_bins(color_set: list, custom_divisions: list):
    combined = []
    for i, c in enumerate(color_set):
        combined.append([custom_divisions[i], c])
    combined.sort()
    low_bin = {"loc": -1, "val": None}
    for i, b in enumerate(combined):
        # remove any high bins that wouldn't be shown
        if b[0] > 1:
            combined.pop(i)
        # remove any low bins that wouldn't be shown; only one bin starting at or below zero should be kept
        elif b[0] <= 0:
            if low_bin["val"] is None:  # first low bin found
                low_bin = {"loc": i, "val": b[0]}
            else:  # there is already a low bin
                if low_bin["val"] < b[0]:
                    combined.pop(low_bin["loc"])
                    low_bin["val"] = b[0]
                    low_bin["loc"] = i - 1
                else:
                    combined.pop(i)
    # force the lowest bin left to start at 0
    if low_bin["loc"] > -1:
        combined[low_bin["loc"]][0] = 0
    # de-aggregate bins
    color_set = [b[1] for b in combined]
    custom_divisions = [b[0] for b in combined]
    return color_set, custom_divisions


def clean_and_sort_colorscale(
    color_set: list, custom_divisions: list, data_min=0, data_max=1
):
    # clean out bins with no start point
    for i, c in enumerate(color_set):
        if custom_divisions[i] is None or len(str(custom_divisions[i])) < 1:
            color_set.pop(i)
            custom_divisions.pop(i)
    # normalize any negative bin division values by shifting everything so the data minimum is 0
    if len(custom_divisions) > 0:
        custom_divisions = [
            ((d - data_min) / (data_max - data_min)) for d in custom_divisions
        ]
    color_set, custom_divisions = remove_unseen_bins(color_set, custom_divisions)
    return color_set, custom_divisions


def make_discrete_colorscale(
    color_set: list, custom_divisions: list, data_min=0, data_max=1
):
    color_set, custom_divisions = clean_and_sort_colorscale(
        color_set, custom_divisions, data_min, data_max
    )
    custom_divisions.append(1)  # add ending bin value
    colorscale = []
    num_colors = len(color_set)
    if num_colors == 0:
        return "jet"  # default rainbow colorscale
    divisions = 1.0 / num_colors
    c_index = 0.0
    for color in color_set:  # Loop over the color sets
        if custom_divisions is not None:
            colorscale.append((custom_divisions.pop(0), color))  # start color block
            colorscale.append((custom_divisions[0] - 0.001, color))  # end color block
        else:
            colorscale.append((c_index, color))  # start color block
            colorscale.append((c_index + divisions - 0.001, color))  # end color block
            c_index = c_index + divisions
    colorscale[-1] = (1, colorscale[-1][1])
    return colorscale
