"""Implementations for filtering signals."""

import numpy as np 
from scipy.signal import bilinear, firwin, kaiserord, lfilter

MIC_CENTER = 1.5
SOUND_SPEED = 340
FILTER_TRANSITION_WIDTH_HZ = 250.0
FILTER_RIPPLE_DB = 60.0


class CapsuleMicsCorrection:
    """

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

        """
        #Analog/Digital convertion
        zeros, poles = bilinear(b, a, self.sample_rate)

        #Filtering
        array_filtered = lfilter(zeros, poles, array)

        return array_filtered

    def axis_correction(
        self,
        axis_signal: np.ndarray,
    ) -> np.ndarray:
        """

        """
        #Filter equations
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

        """
        #Filter equations
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

    """
    nyquist = sample_rate / 2.0

    #Compute FIR filter parameters and apply to signal.
    transition_width_normalized = FILTER_TRANSITION_WIDTH_HZ / nyquist
    filter_length, filter_beta = kaiserord(
        FILTER_RIPPLE_DB, transition_width_normalized
    )
    filter_coefficients = firwin(
        filter_length, cutoff_frec / nyquist, window = ("kaiser", filter_beta)
    )

    return lfilter(filter_coefficients, 1.0, signal)

def moving_average(
    array: np.ndarray,
    window_size: int,
) -> np.ndarray:
    """

    """
    window = np.ones(window_size) / window_size

    return np.convolve(array, window, mode = "valid")