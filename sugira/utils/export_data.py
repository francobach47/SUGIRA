"Generate .txt with exported data"
import numpy as np


def export_data(
    time: np.ndarray,
    time_w_channel: np.ndarray,
    w_channel: np.ndarray,
    intensity: np.ndarray,
    azimuth: np.ndarray,
    elevation: np.ndarray,
) -> None:
    """
    Exports intensity, azimuth, and elevation data to a .txt file.

    Parameters
    ----------
    time : np.ndarray
        Array of time values in milliseconds.'
    time_w_channel : np.ndarray
        Array of time values in milliseconds for W channel.
    w_channel : np.ndarray
        W channel array.
    intensity : np.ndarray
        Intensity array.
    azimuth : np.ndarray
        Azimuth array.
    elevation : np.ndarray
        Elevation array.
    """

    with open("hedgehog.txt", "w", encoding="utf-8") as file:
        file.write("Time [ms],Azimuth,Intensity,Elevation\n")
        for _, (time_i, intens, azim, elev) in enumerate(
            zip(time, intensity, azimuth, elevation)
        ):
            file.write(f"{time_i},{azim},{intens},{elev}\n")

    with open("w_channel.txt", "w", encoding="utf-8") as file:
        file.write("Time [ms],W Channel\n")
        for _, (time_i_w, w) in enumerate(zip(time_w_channel, w_channel)):
            file.write(f"{np.round(time_i_w, 3)},{w}\n")
