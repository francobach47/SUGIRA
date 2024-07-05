"Generate .txt with exported data"
import numpy as np


def export_data(
    time: np.ndarray,
    w_channel: np.ndarray,
    intensity: np.ndarray,
    azimuth: np.ndarray,
    elevation: np.ndarray,
    filename: str = "sugira_data.txt",
) -> None:
    """
    Exports intensity, azimuth, and elevation data to a .txt file.

    Parameters
    ----------
    time : np.ndarray
        Array of time values in milliseconds.
    w_channel : np.ndarray
        W channel array.
    intensity : np.ndarray
        Intensity array.
    azimuth : np.ndarray
        Azimuth array.
    elevation : np.ndarray
        Elevation array.
    filename : str, optional
        Name of the .txt file to save the data, by default "sugira_data.txt".
    """

    with open(filename, "w", encoding="utf-8") as file:
        file.write("Time [ms], W Channel, Azimuth,Intensity,Elevation\n")
        for _, (intens, azim, elev) in enumerate(zip(intensity, azimuth, elevation)):
            file.write(f"{time}, {w_channel}, {azim},{intens},{elev}\n")
