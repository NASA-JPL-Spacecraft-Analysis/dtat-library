"""Module containing type definitions"""
import collections
import json
from collections.abc import MutableMapping
from typing import Any, Optional, TypedDict


class Line(TypedDict):
    width: float
    color: str


class CustomizedTrace(TypedDict):
    size: int
    symbol: str
    color: str
    colorscale: str
    showscale: bool
    line: Line
    solid_color: str
    z_var: Optional[str]
    mode: str


class CustomizationOptions(MutableMapping[str, CustomizedTrace]):
    pass


class CustomizedMarker(TypedDict):
    size: int
    symbol: str
    color: str
    colorscale: str
    showscale: bool
    line: Line
