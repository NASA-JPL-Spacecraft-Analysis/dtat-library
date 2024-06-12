"""
Plotly and other functions for a stacked plot graph

This version makes an arrow for each event
"""

from collections.abc import Sequence
from typing import TYPE_CHECKING, Optional

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import dtat.datacacher as datacacher
import dtat.datachecker as datachecker
import dtat.mouseover_maker as mouseover_maker
import dtat.commonchartfuncs as common
import dtat.palette as palette
from dtat.types import CustomizationOptions
#from datetime import datetime


def make_stacked_graph(
    data: "pd.DataFrame",
    y_vars: Sequence[Sequence[str]],
    x_var: str = "scet",
    z_var: Optional[str] = None,
    multi_axis: bool = False,
    plot_lines: bool = True,
    plot_title: str = None,
    customize_dict: Optional[CustomizationOptions] = None,
    unassigned_colors: Optional[list] = None,
    background_color: str = '#fcfcfc',
    axis_line_color: str = '#555555',
    events = {}
):
    """
    creates a stacked-plot graph
    event:
        A dictionary
            - key = y_var name
            - value = lists of tuples 
        example: {"actual": [(5, "event1"), (10, "event3")], "predicted": [(7, "event2")]}
    """
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

    if isinstance(y_vars, list):
        y_vars = [y for y in y_vars if y is not None and len(y) > 0]

    if y_vars is not None and len(y_vars) > 0:
        num_subplots = len(y_vars)
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
            height=max(450, 200 * num_subplots + 2),
        )

        # determine if plot lines should be shown
        line_mode = "lines+markers" if plot_lines else "markers"

        # use time as x variable
        #if not datachecker.is_time_type(x_var):
        #    x_var = "scet"
        
        #z_vals has the interpolated values and adds it as a column to data
        #datacacher.sort_by(data, x_var)
        #-------------------------
        #OLD VERSION
#         data, z_vals = datacacher.column_values_from_state(
#             data, z_var, elapsed_seconds=True, time="scet"
#         )
        #-------------------------------
        
        #for each of the y variables, it starts adding a new column for that event
        for y in y_vars:
            data, temp = datacacher.column_values_from_state(data, y, elapsed_seconds=True, time="scet")
        
        data, temp = datacacher.column_values_from_state(data, x_var, elapsed_seconds=True, time="scet")
        data, z_vals = datacacher.column_values_from_state(data, z_var, elapsed_seconds=True, time="scet") 
        
        vertical_spacing = 0.2 / num_subplots
        #vertical_spacing = 0.5
        subplot_height = (1.0 - vertical_spacing * (num_subplots - 1)) / num_subplots
        
        
        
        #subplot_height = (1.0) / num_subplots

        
        
        trace_num = 1
        x_domain_start = 0

        for subplot_num, y_dropdown in enumerate(y_vars, start=1):
            #print(y_dropdown)
            if isinstance(y_dropdown, str):
                y_dropdown = [y_dropdown]

            # setting to -.06 so it will be incremented to zero
            y_axis_position = -0.06
            y_domain_start = (num_subplots - subplot_num + 1) / num_subplots
            domain = [y_domain_start - subplot_height, y_domain_start]

            y_axis_title = "Y axis ({})".format("Unit")
            y_axis_layout_name = "yaxis{}".format(subplot_num)
            title_color = "#000000"

            for y_val in y_dropdown:
            
                if y_val not in visible_traces:
                    visible_traces.append(y_val)
                data_slice = datacacher.get_data_from_state(data, y_val)
                #print(data_slice)
                data_slice["value"] = pd.to_numeric(
                    data_slice["value"], errors="ignore"
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
                if multi_axis:
                    y_axis_position += 0.06
                    title_color = marker_values[y_val]["line"]["color"]
                    y_axis_title = "{} ({})".format(y_val, "Unit")
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
                            "overlaying": "y{}".format(subplot_num),
                        }
                    }
                )
                #print(data_slice[x_var])
                graph.add_trace(
                    go.Scattergl(
                        x=data_slice[x_var],
                        y=data_slice["value"],
                        name=y_val,
                        meta=mouseover_maker.make_meta(z_var, data_slice),
                        hovertemplate=mouseover_maker.ht_X_Y_Z_names(
                            xaxis=x_var, yaxis=y_val, zaxis=z_var
                        ),
                        mode=line_mode,
                        showlegend=True,
                        opacity=0.7,
                        marker=marker_values[y_val],
                    ),
                    row=subplot_num,
                    col=1,
                )
                
#                 graph.add_trace(
#                     go.Scattergl(
#                         x=[1000]*len(data_slice["value"]),
#                         y=data_slice["value"],
#                         name= "event1",
#                         #meta=mouseover_maker.make_meta(z_var, data_slice),
#                         hovertemplate="hello there",
#                         mode=line_mode,
#                         showlegend=False,
#                         opacity=0.7,
#                         marker=marker_values[y_val],
#                     ),
#                     row=subplot_num,
#                     col=1,
#                 )
                trace_num += 1
                
                #EVENT PLOTTING (ARROW)
                for e in events.get(y_val, []):
                    
                    #if the x variable is time
                    if datachecker.is_time_type(x_var):
                        curr_index = abs(data_slice[x_var] - e[0]).idxmin()
                        
                        curr_x_val = data_slice._get_value(curr_index, x_var)
                        curr_y_val = data_slice._get_value(curr_index, y_val)
                        
                        #print(curr_x_val, curr_y_val)
                        
#                         graph.add_vline(
#                             x= curr_x_val.timestamp()*1000, 
#                             line_width=3, 
#                             line_color="black", 
#                             row = trace_num-1, 
#                             col= 1)
                        graph.add_annotation(
#                             xref='x',
                            yref = "y",
                            ayref= "paper",
                            x= curr_x_val,
                            ay= 1,
                            y = curr_y_val,
                            text= e[1],
                            hovertext=e[2],
                            arrowhead = 1,
                            showarrow = True,
                            xanchor = "right"
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
                'title': {'text': plot_title}
            }
        )
        
        return graph, unassigned_colors, marker_values, visible_traces

    return graph, {}, {}, []
