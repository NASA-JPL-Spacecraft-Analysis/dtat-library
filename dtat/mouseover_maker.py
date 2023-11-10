"""Functions to create a properly formatted hovertemplate string for plotly charts"""

import dtat.datachecker as checker


def default_hovertemplate():
    """Return a hovertemplate string for a generic
    graph. This is the only hovertemplate method
    in this module that can used without setting meta
    to the output of make_meta()"""
    template = "X: %{x}<br>" "Y: %{y}<br>"
    return template


def make_meta(zvar, data):
    """Returns the meta value for a chart which should
    be set to allow the Z and time values to be reflected
    in hovertext tooltips made by this module.
    This method should be run on the data and set to meta before
    using any of the below 'ht' hovertemplate methods in this module."""
    meta = ""
    if zvar is not None and zvar in data.columns:
        meta = [
            [data[zvar].iloc[i], data["scet"].iloc[i]]
            for i in range(0, len(data["scet"]))
        ]
    else:
        meta = [[None, data["scet"].iloc[i]] for i in range(0, len(data["scet"]))]
    return meta


def ht_X_Y_Z_names(xaxis="X", yaxis="Y", zaxis="Z"):
    """Return a hovertemplate that uses the x and y
    axis names to label the values. The meta field
    should be set to the output of make_meta() for
    this hovertemplate to work properly."""
    if checker.is_time_type(xaxis):
        x = "%{x|%Y-%jT%H:%M:%S.%L}"
    else:
        x = "%{x}"
    if checker.is_time_type(yaxis):
        y = "%{y|%Y-%jT%H:%M:%S.%L}"
    else:
        y = "%{y}"
    if checker.is_time_type(zaxis):
        z = "%{meta[0]|%Y-%jT%H:%M:%S.%L}"
    else:
        z = "%{meta[0]}"
    template = xaxis + ": " + x + "<br>" + yaxis + ": " + y
    if zaxis is not None:
        template = template + "<br>" + zaxis + ": " + z
    template = template + "<extra></extra>"  # removes the trace tag
    return template


def ht_X_Y_Z_time_names(xaxis="X", yaxis="Y", zaxis="Z"):
    """Return a hovertemplate that uses the x and y
    axis names to label the values. The meta field
    should be set to the output of make_meta() for
    this hovertemplate to work properly."""
    if checker.is_time_type(xaxis):
        x = "%{x|%Y-%jT%H:%M:%S.%L}"
    else:
        x = "%{x}"
    if checker.is_time_type(yaxis):
        y = "%{y|%Y-%jT%H:%M:%S.%L}"
    else:
        y = "%{y}"
    if checker.is_time_type(zaxis):
        z = "%{meta[0]|%Y-%jT%H:%M:%S.%L}"
    else:
        z = "%{meta[0]}"
    time = "%{meta[1]|%Y-%jT%H:%M:%S.%L}"
    template = xaxis + ": " + x + "<br>" + yaxis + ": " + y
    if zaxis is not None:
        template = template + "<br>" + zaxis + ": " + z
    template += "<br>scet: " + time
    template = template + "<extra></extra>"  # removes the trace tag
    return template
