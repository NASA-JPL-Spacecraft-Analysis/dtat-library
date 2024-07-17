"""
Plotly and other functions for a stacked plot graph

This version makes an arrow for each event
"""

from collections.abc import Sequence
from typing import TYPE_CHECKING, Optional
from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import dtat.datacacher as datacacher
import dtat.datachecker as datachecker
import dtat.mouseover_maker as mouseover_maker
import dtat.commonchartfuncs as common
import dtat.palette as palette
from dtat.types import CustomizationOptions

import warnings
warnings.filterwarnings('ignore')


def make_stacked_graph(
    data: "pd.DataFrame",
    y_vars: Sequence[Sequence[str]],
    x_var: str = "scet",
    z_var: Optional[str] = None,
    multi_axis: bool = False,
    plot_lines: bool = True,
    figure_title: str = None,
    customize_dict: Optional[CustomizationOptions] = None,
    unassigned_colors: Optional[list] = None,
    background_color: str = '#fcfcfc',
    axis_line_color: str = '#555555',
    figure_margins: dict = None,
    figure_height: int = None,
    figure_width: int = None,
    events: dict[tuple] = {},
    event_line: bool = None,
):
    '''
    events:
        A dictionary
            - key = y_var name
            - value = lists of tuples of (time, name, message)
        example: {"actual": [(time1, "event1", "message1"), (time2, "event2", "message2")], "predicted": [(time3, "event3", "message3")]}
    ''' 
    graph = go.Figure()
    graph.update_layout(
        plot_bgcolor=background_color,
        xaxis=dict(
            showline=True,
            showgrid=True,
            gridcolor=axis_line_color,
            zerolinecolor=axis_line_color,
            linecolor=axis_line_color,
            linewidth=2,
        ),
        yaxis=dict(
            showline=True,
            showgrid=True,
            gridcolor=axis_line_color,
            zerolinecolor=axis_line_color,
            linecolor=axis_line_color,
            linewidth=2,
        ),
    )
    
    visible_traces = []
    marker_values = {}
    if customize_dict is not None and len(customize_dict) > 0:
        for t in customize_dict.keys():
            marker_values[t] = common.get_plotly_marker_values(customize_dict[t])

    if unassigned_colors is None:
        unassigned_colors = palette.get_default_colors()

    num_subplots = len(y_vars)

    figure_margins = dict(l=75, b=100, t=50, r=75) if figure_margins is None else figure_margins

    if figure_height is None:
        figure_height = max(450, 200 * num_subplots + 2)

    if y_vars is not None and len(y_vars) > 0:
        graph = make_subplots(num_subplots, cols=1, shared_xaxes=True, vertical_spacing = 0.2).update_layout(
            plot_bgcolor=background_color,
            xaxis=dict(
                showline=True,
                showgrid=True,
                gridcolor=axis_line_color,
                zerolinecolor=axis_line_color,
                linecolor=axis_line_color,
                linewidth=2,
            ),
            yaxis=dict(
                showline=True,
                showgrid=True,
                gridcolor=axis_line_color,
                zerolinecolor=axis_line_color,
                linecolor=axis_line_color,
                linewidth=2,
            ),
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
            height=figure_height
        )

        # determine if plot lines should be shown
        line_mode = "lines+markers" if plot_lines else "markers"

        data, temp = datacacher.column_values_from_state(data, x_var, elapsed_seconds=True, time="scet")
        data, z_vals = datacacher.column_values_from_state(data, z_var, elapsed_seconds=True, time="scet") 
        
        vertical_spacing = 0.2 / num_subplots
        subplot_height = (1.0 - vertical_spacing * (num_subplots - 1)) / num_subplots
        
        trace_num = 1
        x_domain_start = 0

        for subplot_num, plot_y_vars in enumerate(y_vars, start=1):

            # setting to -.06 so it will be incremented to zero
            y_axis_position = -0.1
            y_domain_start = (num_subplots - subplot_num + 1) / num_subplots
            domain = [y_domain_start - subplot_height, y_domain_start]
            y_axis_units = datacacher.get_units_from_state(data, plot_y_vars[0])

            if len(plot_y_vars) == 1:
                y_axis_title = f'{plot_y_vars[0]} ({y_axis_units})'
            else:
                y_axis_title = f'Y axis ({y_axis_units[subplot_num-1]})' if len(y_axis_units) > 0 else 'Y axis'
            y_axis_layout_name = "yaxis{}".format(subplot_num)
            title_color = "#000000"

            for y_val in plot_y_vars:
            
                if y_val not in visible_traces:
                    visible_traces.append(y_val)
                data_slice = datacacher.get_data_from_state(data, y_val)
                data_slice["value"] = pd.to_numeric(
                    data_slice["value"], errors='ignore'
                )
                if y_val not in marker_values.keys():
                    if z_var is not None and z_var in data.columns:
                        color = data_slice[z_vals]
                        line_color = "#000000"
                    else:
                        color, unassigned_colors = palette.pop_next_color(
                            unassigned_colors
                        )
                        if color in palette.default_colors.keys():
                            line_color = palette.default_colors[color]["line_color"]
                        else:
                            line_color = "#000000"
                    marker_values[y_val] = {
                        "size": 5,
                        "symbol": "circle",
                        "color": color,
                        "colorscale": palette.make_discrete_colorscale([], []),
                        "showscale": (z_var is not None),
                        "line": {
                            "width": 0.5 if z_var is None else 0,
                            "color": line_color,
                        },
                    }
                else:
                    if z_var is not None and z_var in data.columns:
                        marker_values[y_val]["color"] = data_slice[z_vals]
                if multi_axis:
                    y_axis_position += 0.1
                    title_color = marker_values[y_val]["line"]["color"]
                    y_axis_title = f"{y_val} ({y_axis_units})"
                    y_axis_layout_name = "yaxis{}".format(trace_num)

                graph.update_layout(
                    {
                        y_axis_layout_name: {
                            "title": {
                                "text": y_axis_title,
                                "font": {"color": title_color},
                            },
                            "position": max(y_axis_position, 0),
                            "anchor": "free",
                            "tickfont": {"color": title_color},
                            "domain": domain,
                            "overlaying": "y{}".format(subplot_num)
                        }
                    }
                )
                graph.add_trace(
                    go.Scattergl(
                        x=data_slice[x_var],
                        y=data_slice["value"],
                        name=y_val,
                        meta=mouseover_maker.make_meta(z_var, data_slice),
                        hovertemplate=mouseover_maker.ht_X_Y_Z_time_names(
                            xaxis=x_var, yaxis=y_val, zaxis=z_var
                        ),
                        mode=line_mode,
                        showlegend=True,
                        opacity=0.7,
                        marker=marker_values[y_val],
                        #"tickvals": [],
                        #"ticktext": []
                    ),
                    row=subplot_num,
                    col=1,
                )
                trace_num += 1

                #EVENT PLOTTING (ARROW)
                for e in events.get(y_val, []):

                    #for each of the y variables, it starts adding a new column for that event
                    if y_val not in data_slice.columns:
                        data, temp = datacacher.column_values_from_state(data, y_val, elapsed_seconds=True, time="scet")
                        
                    #if the x variable is time (otherwise don't bother trying to plot non-time events)
                    if datachecker.is_time_type(x_var):
                        if len(e) == 2:
                            e = (datetime.strptime(e[0], "%Y-%jT%H:%M:%S.%f"), e[1])
                        else:
                            e = (datetime.strptime(e[0], "%Y-%jT%H:%M:%S.%f"), e[1], e[2])
                                                
                        if event_line:
                            graph.add_vline(
                                x=e[0],
                                line_width=3, 
                                line_color="black", 
                                row = subplot_num-1, 
                                col= 1
                            )
                        
                        graph.add_annotation(
                            x = e[0],
                            yref = f'y{subplot_num} domain' if subplot_num > 1 else 'y domain',
                            ayref=f'y{subplot_num} domain' if subplot_num > 1 else 'y domain',
                            y=0,
                            ay = -0.1,
                            text= e[1],
                            hovertext=e[2] if len(e) > 2 else e[1],
                            arrowhead = 1,
                            showarrow = True
                        )

            x_domain_start = max(x_domain_start, y_axis_position)
        

        if multi_axis:
            # adding multiple traces to a subplot resets the axis assignment
            # re-assign y-axes to traces
            for trace_num, trace in enumerate(graph.data, start=1):
                trace.yaxis = "y{}".format(trace_num)
            # set shared x-axis domain based on positions of y-axes
            graph.update_xaxes(
                domain=[x_domain_start, 1], anchor="y{}".format(trace_num)
            )

        graph.update_xaxes(
            showline=True,
            showgrid=True,
            gridcolor=axis_line_color,
            zerolinecolor=axis_line_color,
            linecolor=axis_line_color,
            linewidth=2,
        )
        graph.update_yaxes(
            showline=True,
            showgrid=True,
            gridcolor=axis_line_color,
            zerolinecolor=axis_line_color,
            linecolor=axis_line_color,
            linewidth=2,
        )

        graph.update_layout(
            {
                'title': {'text': figure_title},
                'font_family': 'Arial',
                'margin': figure_margins
            }
        )

        x_unit = datacacher.get_units_from_state(data, x_var)
        graph.update_xaxes(
            title_text=f'{x_var} ({x_unit})'
        )

        if figure_width is not None:
            graph.update_layout({'width': figure_width})
        
        return graph, unassigned_colors, marker_values, visible_traces

    return graph, {}, {}, []



def make_diff_graph(
    data: "pd.DataFrame",
    y1: str,
    y2: str,
    y_axis_units: Sequence[str] = [],
    x_var: str = "scet",
    figure_title: str = None,
    unassigned_colors: Optional[list] = None,
    background_color: str = '#fcfcfc',
    axis_line_color: str = '#555555',
    figure_margins: dict = None,
    figure_height: int = None,
    figure_width: int = None,
):
    '''
    events:
        A dictionary
            - key = y_var name
            - value = lists of tuples of (time, name, message)
        example: {"actual": [(time1, "event1", "message1"), (time2, "event2", "message2")], "predicted": [(time3, "event3", "message3")]}
    ''' 
    graph = go.Figure()
    graph.update_layout(
        plot_bgcolor=background_color,
        xaxis=dict(
            showline=True,
            showgrid=True,
            gridcolor=axis_line_color,
            zerolinecolor=axis_line_color,
            linecolor=axis_line_color,
            linewidth=2,
        ),
        yaxis=dict(
            showline=True,
            showgrid=True,
            gridcolor=axis_line_color,
            zerolinecolor=axis_line_color,
            linecolor=axis_line_color,
            linewidth=2,
        ),
    )
    
    visible_traces = []
    marker_values = {}

    if unassigned_colors is None:
        unassigned_colors = palette.get_default_colors()

    num_subplots = 1

    figure_margins = dict(l=75, b=100, t=50, r=75) if figure_margins is None else figure_margins

    if figure_height is None:
        figure_height = max(450, 200 * num_subplots + 2)

    graph = make_subplots(num_subplots, cols=1, shared_xaxes=True, vertical_spacing = 0.2).update_layout(
        plot_bgcolor=background_color,
        xaxis=dict(
            showline=True,
            showgrid=True,
            gridcolor=axis_line_color,
            zerolinecolor=axis_line_color,
            linecolor=axis_line_color,
            linewidth=2,
        ),
        yaxis=dict(
            showline=True,
            showgrid=True,
            gridcolor=axis_line_color,
            zerolinecolor=axis_line_color,
            linecolor=axis_line_color,
            linewidth=2,
        ),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
        ),
        height=figure_height
    )

    data, temp = datacacher.column_values_from_state(data, x_var, elapsed_seconds=True, time="scet")

    y1_data_slice = datacacher.get_data_from_state(data, y1)
    y2_data_slice = datacacher.get_data_from_state(data, y2)

    graph.add_trace(go.Scatter(
        x = y1_data_slice[x_var], 
        y = y1_data_slice["value"], 
        fill='tozeroy',
        name=y1,
        meta=mouseover_maker.make_meta(None, y1_data_slice),
        hovertemplate=mouseover_maker.ht_X_Y_Z_time_names(
            xaxis=x_var, yaxis=y1, zaxis=None
        ),
    ))
    graph.add_trace(go.Scatter(
            x = y2_data_slice[x_var], 
            y = y2_data_slice["value"], 
            fill='tozeroy',
            name=y2,
            meta=mouseover_maker.make_meta(None, y2_data_slice),
            hovertemplate=mouseover_maker.ht_X_Y_Z_time_names(
                xaxis=x_var, yaxis=y2, zaxis=None
            ),
        ))

    graph.update_layout(showlegend=False)
    graph.update_layout(xaxis_title = x_var, title = f"Difference between {y1} and {y2}")

            
    graph.update_xaxes(
            showline=True,
            showgrid=True,
            gridcolor=axis_line_color,
            zerolinecolor=axis_line_color,
            linecolor=axis_line_color,
            linewidth=2,
        )
    graph.update_yaxes(
            showline=True,
            showgrid=True,
            gridcolor=axis_line_color,
            zerolinecolor=axis_line_color,
            linecolor=axis_line_color,
            linewidth=2,
            title_text=f'{y1} diff {y2}'
        )

    graph.update_layout(
            {
                'title': {'text': figure_title},
                'font_family': 'Arial',
                'margin': figure_margins
            }
        )

    graph.update_xaxes(
            title_text=x_var
        )

    if figure_width is not None:
            graph.update_layout({'width': figure_width})
        
    return graph, unassigned_colors, marker_values, visible_traces



def make_bar_graph(
    data: "pd.DataFrame",
    y1: str,
    y2: str,
    y_axis_units: Sequence[str] = [],
    x_var: str = "scet",
    figure_title: str = None,
    unassigned_colors: Optional[list] = None,
    background_color: str = '#fcfcfc',
    axis_line_color: str = '#555555',
    figure_margins: dict = None,
    figure_height: int = None,
    figure_width: int = None,
    bar_width: int = 1,
    plot_lines: bool = False,
    bar_color: str= "#005500"
):
    '''
    events:
        A dictionary
            - key = y_var name
            - value = lists of tuples of (time, name, message)
        example: {"actual": [(time1, "event1", "message1"), (time2, "event2", "message2")], "predicted": [(time3, "event3", "message3")]}
    ''' 
    graph = go.Figure()
    graph.update_layout(
        plot_bgcolor=background_color,
        xaxis=dict(
            showline=True,
            showgrid=True,
            gridcolor=axis_line_color,
            zerolinecolor=axis_line_color,
            linecolor=axis_line_color,
            linewidth=2,
        ),
        yaxis=dict(
            showline=True,
            showgrid=True,
            gridcolor=axis_line_color,
            zerolinecolor=axis_line_color,
            linecolor=axis_line_color,
            linewidth=2,
        ),
    )
    
    visible_traces = []
    marker_values = {}

    if unassigned_colors is None:
        unassigned_colors = palette.get_default_colors()

    num_subplots = 1

    figure_margins = dict(l=75, b=100, t=50, r=75) if figure_margins is None else figure_margins

    if figure_height is None:
        figure_height = max(450, 200 * num_subplots + 2)

    graph = make_subplots(num_subplots, cols=1, shared_xaxes=True, vertical_spacing = 0.2).update_layout(
        plot_bgcolor=background_color,
        xaxis=dict(
            showline=True,
            showgrid=True,
            gridcolor=axis_line_color,
            zerolinecolor=axis_line_color,
            linecolor=axis_line_color,
            linewidth=2,
        ),
        yaxis=dict(
            showline=True,
            showgrid=True,
            gridcolor=axis_line_color,
            zerolinecolor=axis_line_color,
            linecolor=axis_line_color,
            linewidth=2,
        ),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
        ),
        height=figure_height
    )

    data, temp = datacacher.column_values_from_state(data, x_var, elapsed_seconds=True, time="scet")

    interpolated = datacacher.column_values_from_state(data, y2, x_var)[0]
    
    y1_data_slice = datacacher.get_data_from_state(interpolated, y1)
    y2_data_slice = datacacher.get_data_from_state(interpolated, y2)

    diff_slice = y1_data_slice['value'] - y1_data_slice[y2]

    average_time = y1_data_slice[x_var].max() - y1_data_slice[x_var].min()
    if datachecker.is_time_type(x_var):
        average_time = average_time.total_seconds()

    graph.add_traces(go.Bar(x=y1_data_slice[x_var], y = diff_slice, 
                        width=average_time*bar_width,
                        marker_color= bar_color,
                        opacity=0.7
                    ))
        
    if plot_lines:
        graph.add_trace(go.Scatter(
            x = y1_data_slice[x_var], 
            y = y1_data_slice["value"], 
            name=y1,
            meta=mouseover_maker.make_meta(None, y1_data_slice),
            hovertemplate=mouseover_maker.ht_X_Y_Z_time_names(
                xaxis=x_var, yaxis=y1, zaxis=None
            )
        ))
        graph.add_trace(go.Scatter(
            x = y2_data_slice[x_var], 
            y = y2_data_slice["value"], 
            name=y2,
            meta=mouseover_maker.make_meta(None, y2_data_slice),
            hovertemplate=mouseover_maker.ht_X_Y_Z_time_names(
                xaxis=x_var, yaxis=y2, zaxis=None
            )
    ))
            
    graph.update_xaxes(
            showline=True,
            showgrid=True,
            gridcolor=axis_line_color,
            zerolinecolor=axis_line_color,
            linecolor=axis_line_color,
            linewidth=2,
        )
    graph.update_yaxes(
            showline=True,
            showgrid=True,
            gridcolor=axis_line_color,
            zerolinecolor=axis_line_color,
            linecolor=axis_line_color,
            linewidth=2,
            title_text=f'{y1} diff {y2}'
        )

    graph.update_layout(
            {
                'title': {'text': figure_title},
                'font_family': 'Arial',
                'margin': figure_margins
            }
        )

    graph.update_xaxes(
            title_text=x_var
        )

    if figure_width is not None:
            graph.update_layout({'width': figure_width})
        
    return graph, unassigned_colors, marker_values, visible_traces
