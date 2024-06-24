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
    Exports intensity, azimuth and elevation data in .txt file.

    Parameters
    ----------
    time: np.ndarray,
        ...
    w_channel: np.ndarray,
        ...
    intensity : np.ndarray
        Intensity array.
    azimuth : np.ndarray
        Azimuth array.
    Elevation : np.ndarray
        Elevation array.
    filename : str
        .txt file name.
    """

    with open(filename, "w", encoding="utf-8") as file:
        file.write("Time [ms], W Channel, Azimuth,Intensity,Elevation\n")
        for _, (intens, azim, elev) in enumerate(zip(intensity, azimuth, elevation)):
            file.write(f"{time}, {w_channel}, {azim},{intens},{elev}\n")