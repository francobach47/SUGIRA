"""Implementations for filtering signals."""

import numpy as np
from scipy.signal import bilinear, firwin, kaiserord, lfilter

MIC_CENTER = 1.5
SOUND_SPEED = 340
FILTER_TRANSITION_WIDTH_HZ = 250.0
FILTER_RIPPLE_DB = 60.0


class CapsuleMicsCorrection:
    """
    Class for correcting microphone signals based on capsule characteristics.

    Parameters
    ----------
    sample_rate : int
        Sample rate in Hz.
    mic_to_center : float, optional
        Distance from microphone to center in cm, by default MIC_CENTER.
    sound_speed : float, optional
        Speed of sound in m/s, by default SOUND_SPEED.
    """

    def __init__(
        self,
        sample_rate: int,
        mic_to_center: float = MIC_CENTER,
        sound_speed: float = SOUND_SPEED,
    ) -> None:
        self.sample_rate = sample_rate
        self.mic_to_center = mic_to_center / 100
        self.sound_speed = sound_speed
        self.delay_to_center = self.mic_to_center / self.sound_speed

    def _filter(
        self,
        b: np.ndarray,
        a: np.ndarray,
        array: np.ndarray,
    ) -> np.ndarray:
        """
        Applies a digital filter to the input array.

        Parameters
        ----------
        b : np.ndarray
            Numerator polynomial coefficients of the filter.
        a : np.ndarray
            Denominator polynomial coefficients of the filter.
        array : np.ndarray
            Input array to be filtered.

        Returns
        -------
        np.ndarray
            Filtered array.
        """

        zeros, poles = bilinear(b, a, self.sample_rate)
        array_filtered = lfilter(zeros, poles, array)

        return array_filtered

    def axis_correction(
        self,
        axis_signal: np.ndarray,
    ) -> np.ndarray:
        """
        Applies axis correction to the input signal.

        Parameters
        ----------
        axis_signal : np.ndarray
            Input signal to be corrected.

        Returns
        -------
        np.ndarray
            Corrected signal.
        """

        b = np.sqrt(6) * np.array(
            [1, 1j * (1 / 3) * self.mic_to_center, -(1 / 3) * self.delay_to_center**2]
        )
        a = np.array([1, 1j * (1 / 3) * self.delay_to_center])
        axis_corrected = self._filter(b, a, axis_signal)

        return axis_corrected

    def omni_correction(
        self,
        omni_signal: np.ndarray,
    ) -> np.ndarray:
        """
        Applies omnidirectional correction to the input signal.

        Parameters
        ----------
        omni_signal : np.ndarray
            Input omnidirectional signal to be corrected.

        Returns
        -------
        np.ndarray
            Corrected signal.
        """

        a = np.array([1, 1j * (1 / 3) * self.delay_to_center])
        b = np.array([1, 1j * self.delay_to_center, -(1 / 3) * self.delay_to_center**2])
        omni_corrected = self._filter(b, a, omni_signal)

        return omni_corrected


def low_pass_filter(
    signal: np.ndarray,
    cutoff_frec: int,
    sample_rate: int,
) -> np.ndarray:
    """
    Applies a low-pass filter to the input signal.

    Parameters
    ----------
    signal : np.ndarray
        Input signal to be filtered.
    cutoff_frec : int
        Cutoff frequency in Hz.
    sample_rate : int
        Sample rate in Hz.

    Returns
    -------
    np.ndarray
        Filtered signal.
    """

    nyquist = sample_rate / 2.0

    # Compute FIR filter parameters and apply to signal.
    transition_width_normalized = FILTER_TRANSITION_WIDTH_HZ / nyquist
    filter_length, filter_beta = kaiserord(
        FILTER_RIPPLE_DB, transition_width_normalized
    )
    filter_coefficients = firwin(
        filter_length, cutoff_frec / nyquist, window=("kaiser", filter_beta)
    )

    return lfilter(filter_coefficients, 1.0, signal)


def moving_average(
    array: np.ndarray,
    window_size: int,
) -> np.ndarray:
    """
    Applies a moving average filter to the input array.

    Parameters
    ----------
    array : np.ndarray
        Input array to be filtered.
    window_size : int
        Size of the moving average window.

    Returns
    -------
    np.ndarray
        Filtered array.
    """

    window = np.ones(window_size) / window_size

    return np.convolve(array, window, mode="valid")
