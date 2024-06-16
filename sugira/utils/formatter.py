from functools import singledispatch
from typing import List, Tuple, Union
import numpy as np


@singledispatch
def convert_ambisonics_a_to_b(
    front_left_up: np.ndarray,
    front_right_down: np.ndarray,
    back_right_up: np.ndarray,
    back_left_down: np.ndarray,
) -> np.ndarray:
    """Converts Ambisonics A-format to B-format."""

    w_channel = front_left_up + front_right_down + back_left_down + back_right_up
    x_channel = front_left_up + front_right_down - back_left_down - back_right_up
    y_channel = front_left_up - front_right_down + back_left_down - back_right_up
    z_channel = front_left_up - front_right_down - back_left_down + back_right_up

    b_format = np.array([w_channel, x_channel, y_channel, z_channel])

    return b_format


@convert_ambisonics_a_to_b.register(dict)
def _(a_format_channels: dict) -> np.ndarray:
    """Converts Ambisonics A-format to B-format."""

    back_left_down = a_format_channels["back_left_down"]
    back_right_up = a_format_channels["back_right_up"]
    front_left_up = a_format_channels["front_left_up"]
    front_right_down = a_format_channels["front_right_down"]

    w_channel = front_left_up + front_right_down + back_left_down + back_right_up
    x_channel = front_left_up + front_right_down - back_left_down - back_right_up
    y_channel = front_left_up - front_right_down + back_left_down - back_right_up
    z_channel = front_left_up - front_right_down - back_left_down + back_right_up

    b_format = np.array([w_channel, x_channel, y_channel, z_channel])

    return b_format


@convert_ambisonics_a_to_b.register(list)
def _(a_format_channels: List[np.ndarray]) -> np.ndarray:
    """Converts Ambisonics A-format to B-format."""

    assert (
        len(a_format_channels) == 4
    ), "Conversion from A-format to B-format requires 4 channels"

    back_left_down = a_format_channels[3]
    back_right_up = a_format_channels[2]
    front_left_up = a_format_channels[0]
    front_right_down = a_format_channels[1]

    b_format = convert_ambisonics_a_to_b.dispatch(np.ndarray)(
        front_left_up, front_right_down, back_right_up, back_left_down
    )

    return b_format


def cartesian_to_spherical(intensity_windowed: np.ndarray):

    # Convert to total intensity, azimuth and elevation
    intensity = np.sqrt((intensity_windowed**2).sum(axis=0))
    azimuth = np.rad2deg(np.arctan2(intensity_windowed[1], intensity_windowed[0]))
    elevation = np.rad2deg(np.arcsin(intensity_windowed[2] / intensity))

    return intensity, azimuth, elevation


def spherical_to_cartesian(
        radius: Union[float, np.ndarray],
        azimuth: Union[float, np.ndarray],
        elevation: Union[float, np.ndarray],
        
)-> Tuple[Union[float, np.ndarray]]:
  
    return (
        radius * np.cos(np.deg2rad(azimuth)) * np.cos(np.deg2rad(elevation)),
        radius * np.sin(np.deg2rad(azimuth)) * np.cos(np.deg2rad(elevation)),
        radius * np.sin(np.deg2rad(elevation)),
    )
