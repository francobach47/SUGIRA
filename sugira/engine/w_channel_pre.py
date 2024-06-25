""""W channel preprocessing"""
import numpy as np

from utils.filters import moving_average
from engine.intensity import crop_1d

def w_preprocess(
    w_channel: np.ndarray,
    window_size: int,
    analysis_length: float,
    sample_rate: int,
) -> np.ndarray:
    """
    """
    w_channel_cropped = np.abs(crop_1d(w_channel, analysis_length, sample_rate))
    w_channel_filtered = moving_average(w_channel_cropped, int(window_size / 2))
    w_channel_filtered /= np.max(w_channel_filtered)
    
    #PRUEBA DE ENERGIA
    w_db = 10 * np.log10(w_channel_filtered**2)

    return w_channel_filtered, w_db