"""Datacache object functions for a cache for data from one or more sources"""

import logging
import datetime
import warnings

import pandas as pd

import dtat.datachecker as datachecker
import dtat.datainterpolator as interpolate
#import appmgr.utilfuncs as utils
#import connectors.bin_connector as binc
#import connectors.csv_connector as csvc
#import connectors.mcws_connector as mcwsc
#import connectors.states_connector as statesc


def make_pd_cache_from_data(data_lists):
    cache = pd.DataFrame(columns=datachecker.header())
    for d in data_lists:
        new_df = pd.read_json(d)
        for col in datachecker.header():
            if col not in new_df.columns:
                new_df[col] = None
        cache = pd.concat([cache, new_df[datachecker.header()]], ignore_index=True, axis=0, join='outer')
    for time_type in datachecker.valid_time_type_cols():
        cache[time_type] = pd.to_datetime(
            cache[time_type], unit="ms", utc=True
        )  # PSA: pd.to_json saves in ms, pd.to_datetime expects ns
    return cache


def get_min_date(data):
    """Returns the minimum date of data in this cache"""
    if len(data["scet"]) > 0:
        return data["scet"].min()
    else:
        return None


def get_max_date(data):
    """Returns the maximum date of data in this cache"""
    if len(data["scet"]) > 0:
        return data["scet"].max()
    else:
        return None


def sort_by(data, col, ascending=True):
    """Sorts the data by the given column name"""
    if col not in data.columns:
        return data
    data = data.sort_values(by=col, ignore_index=True, ascending=ascending)
    logging.debug("sort data log")
    log_data(data)
    return data


def get_data_from_state(data, state):
    """Returns only the data for the given state.
    Does not modify the cache.
    Returns empty if state is invalid."""
    if state in data.name.unique():
        return data[data["name"] == state]
    else:
        return pd.DataFrame(columns=datachecker.header())


def get_data_from_states(data, filter_states):
    """Returns only data for the given list of states.
    Does not modify the cache.
    Returns empty if all states are invalid,
    otherwise skips invalid states."""
    if set(filter_states):
        return data.loc[data.name.isin(filter_states)]
    return pd.DataFrame(columns=datachecker.header())


def column_values_from_state(data, state, time, elapsed_seconds=False):
    """Makes a column of values for the given state.
    Returns the data and column name."""
    data = sort_by(data, time)
    interpolator = interpolate.DefaultInterpolator(data)
    data = interpolator.make_column_values(state, elapsed_seconds)
    state='z_numeric'
    log_data(data)
    if datachecker.is_time_type(state) and elapsed_seconds:
        state = "elapsed_seconds"
    return data, state


def log_data(data):
    """Log the current data as a debug message"""
    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        logging.debug("\n %s", data)


def print_data(data):
    """Print the current data to console"""
    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        print("\n %s", data)


def get_units_from_states(data, states):
    if isinstance(states, list):
        units = []
        for state in states:
            r = get_unit_from_state(data, state)
            units.append(r)
        return units
    else: 
        return get_unit_from_state(data, states)

def get_unit_from_state(data, state):
    if datachecker.is_time_type(state):
        return 'Time'
    if 'unit' in data.columns:
        state_data = get_data_from_state(data, state)
        if len(state_data) > 0:
            unit = state_data['unit'].unique()
            if len(unit) == 1:
                return unit[0]
            warnings.warn(f'DTAT has detected multiple units for a single state. {state} has units {unit}.')
            return unit
    return 'Unknown'


def make_doy_from_state(data, state):
    print (data.columns)
    if datachecker.is_time_type(state) and 'doy' not in data.columns:
        data['doy'] = data.apply(
            lambda row: datetime.datetime.strftime(row[state], '%Y/%jT%H:%M:%S.%f'), 
            axis=1)
        #print (data['doy'])
    return data
