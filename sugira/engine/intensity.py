"""Intensity computation"""
from typing import Tuple

import numpy as np

from utils.filters import low_pass_filter

FILTER_CUTOFF = 500
OVERLAP_RATIO = 0.5


def crop_1d(
    array: np.ndarray,
    analysis_length: float,
    sample_rate: int,
):
    """
    """
     #Get analysis length max index
    analysis_length_idx = int(analysis_length * sample_rate)

    #Slice from intensity max to analysis length
    earliest_peak_idx = np.argmax(np.abs(array))
    array_cropped = array[earliest_peak_idx : earliest_peak_idx + analysis_length_idx]

    return array_cropped


def crop_2d(
    analysis_length: float,
    sample_rate: int,
    intensity_direction: np.ndarray,
): 
    """
    """
    #Get analysis length max index
    analysis_length_idx = int(analysis_length * sample_rate)

    #Slice from intensity max to analysis length
    earliest_peak_idx = np.argmax(np.abs(intensity_direction), axis = 1).min()
    intensity_directions_cropped = intensity_direction[:, earliest_peak_idx : earliest_peak_idx + analysis_length_idx]

    return intensity_directions_cropped


def bformat_to_intensity(signal: np.ndarray, sample_rate) -> Tuple[np.ndarray]:
    """
    """
    #Calculate intensity from directions. Intensity = pressure(W channel) * pressure_gradient(XYZ channel)
    signal_filtered = low_pass_filter(signal, FILTER_CUTOFF, sample_rate)
    #signal_filtered = signal
    intensity_directions = (signal_filtered[0, :] * signal_filtered[1:, :])

    return intensity_directions


def intensity_to_dB(intensity_array: np.ndarray) -> np.ndarray:
    """
    """
    p_ref = 1e-12
    return 10 * np.log10(intensity_array / p_ref)


def reflection_threshold(
    threshold: float,
    intensity: np.ndarray,
    azimuth: np.ndarray,
    elevation: np.ndarray,
    reflections: np.ndarray,
) -> Tuple[np.ndarray]:
    """
    """
    reflex_to_direct = intensity_to_dB(intensity) - intensity_to_dB(intensity[0])
    threshold_mask = reflex_to_direct > threshold

    return (
        reflex_to_direct[threshold_mask],
        azimuth[threshold_mask],
        elevation[threshold_mask],
        reflections[threshold_mask],
    )


def min_max_normalization(array: np.ndarray) -> np.ndarray:
    """
    """
    normalization = (array - array.min() * 1.1) / (array.max() - array.min() * 1.1)
    return normalization


def integrate_intensity_directions(
    intensity_directions: np.ndarray,
    duration_secs: float,
    sample_rate: int,
) -> np.ndarray:
    """
    """
    #ValueError
    if intensity_directions.shape[0] == 4:
        intensity_directions = intensity_directions[1:, :]
    elif (intensity_directions.shape[0] < 3) or (intensity_directions.shape[0] > 4):
        raise ValueError(f"Incorrect input shape {intensity_directions.shape}")
    
    #Convert integration time to samples
    duration_samples = np.round(duration_secs * sample_rate).astype(np.int64)

    #Padding and Windowing
    hop_size = int(duration_samples * (1 - OVERLAP_RATIO))
    intensity_directions = np.concatenate([intensity_directions, np.zeros((3, intensity_directions.shape[1] % hop_size))], axis = 1,)
    output_shape = (3, int(intensity_directions.shape[1] / duration_samples / OVERLAP_RATIO) - 1,)
    intensity_windowed = np.zeros(output_shape)
    time = np.zeros(output_shape[1])
    window = np.hamming(duration_samples)

    for i in range(0, output_shape[1]):
        intensity_segment = intensity_directions[:, i * hop_size : i * hop_size + duration_samples]
        intensity_windowed[:, i] = np.mean(intensity_segment * window, axis = 1)
        time[i] = i * hop_size / sample_rate
    
    #Add direct sound with no window
    intensity_windowed = np.insert(intensity_windowed, 0, intensity_directions[:, 0], axis = 1)

    return intensity_windowed, time