"""Definition of methods for reflexion detection of a room impulse response."""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Tuple, Union

import numpy as np
from scipy.signal import find_peaks, find_peaks_cwt


# pylint: disable=too-few-public-methods
class ReflectionDetection(ABC):
    """Base interface for a reflection detection algorithm."""

    @staticmethod
    @abstractmethod
    def get_indeces_of_reflections(intensity_magnitude: np.ndarray) -> np.ndarray:
        """Abstract method to be overwritten by concrete implementations of
        reflection detection."""


# pylint: disable=too-few-public-methods
class PeakStrategy(ReflectionDetection):
    """Algorithm for detecting reflections based on the surrounding values
    of local maxima."""

    @staticmethod
    def get_indeces_of_reflections(intensity_magnitude: np.ndarray) -> np.ndarray:
        """
        Find local maxima in the intensity magnitude signal.

        Parameters
        ----------
        intensity_magnitude : np.ndarray
            Intensity magnitude signal.

        Returns
        -------
        np.ndarray
            An array with the indices of the peaks.
        """
        # Drop peak properties ([0]) and direct sound peak ([1])
        return find_peaks(intensity_magnitude)[0]


class WaveletStrategy(ReflectionDetection):
    """Algorithm for detecting reflections based on the wavelet transform"""

    @staticmethod
    def get_indeces_of_reflections(intensity_magnitude: np.ndarray) -> np.ndarray:
        """
        Find local maxima in the intensity magnitude signal.

        Parameters
        ----------
        intensity_magnitude : np.ndarray
            Intensity magnitude signal.

        Returns
        -------
        np.ndarray
            An array with the indices of the peaks.
        """
        # Drop peak properties ([0]) and direct sound peak ([1])
        return find_peaks_cwt(intensity_magnitude, widths=np.arange(5, 15))[0]


class DetectionStrategy(Enum):
    """Enum class for accessing the existing Detection Strategies"""

    PEAK = PeakStrategy
    WAVELET = WaveletStrategy


def detect_reflections(
    intensity: np.ndarray,
    azimuth: np.ndarray,
    elevation: np.ndarray,
    strategy_selected: Union[
        ReflectionDetection, DetectionStrategy
    ] = DetectionStrategy.PEAK,
) -> Tuple[np.ndarray]:
    """
    Analyzes the normalized intensity, azimuth, and elevation arrays to look for
    reflections. Timeframes that don't contain a reflection are masked.

    Parameters
    ----------
    intensity : np.ndarray
        Normalized intensity array.
    azimuth : np.ndarray
        Array with horizontal angles with respect to the XZ plane.
    elevation : np.ndarray
        Array with vertical angles with respect to the XY plane.

    Returns
    -------
    np.ndarray
        Masked intensities with only reflections different than 0.
    np.ndarray
        Masked azimuths with only reflections different than 0.
    np.ndarray
        Masked elevations with only reflections different than 0.
    """

    if isinstance(strategy_selected, DetectionStrategy):
        strategy_selected = strategy_selected.value

    reflections_idxs = strategy_selected.get_indeces_of_reflections(intensity)
    # Add direct sound
    reflections_idxs = np.insert(reflections_idxs, 0, 0)
    return (
        intensity[reflections_idxs],
        azimuth[reflections_idxs],
        elevation[reflections_idxs],
        reflections_idxs,
    )
