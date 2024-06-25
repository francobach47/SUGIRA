""""Audio utilities"""

from typing import List
import numpy as np  
import soundfile as sf


def read_signals(input_data_dict: dict) -> dict:
    """
    
    """

    signals_dict = {}
    signals_paths = {}
    
    sample_rate = ...

    for key_i, path_i in input_data_dict.items():

        if key_i in ["front_left_up",
                    "front_right_down",
                    "back_right_up",
                    "back_left_down",
                    "stacked_signals",
                    "inverse_filter",
                    "x_channel",
                    "y_channel",
                    "z_channel",
                    "w_channel"
                ]:
            try:
                signal, sample_rate = sf.read(path_i)
                signals_dict[key_i] = signal.T
                signals_paths[key_i] = path_i
            except:
                pass    
        signals_dict["sample_rate"] = sample_rate

    if input_data_dict["channels_per_file"] == 1:
        if input_data_dict["input_mode"] == "bformat":
            bformat_keys = ["w_channel", "x_channel", "y_channel", "z_channel"]
            signals_dict["stacked_signals"] = stack_dict_arrays(signals_dict, bformat_keys)
        else:
            aformat_keys = [
                "front_left_up",
                "front_right_down",
                "back_right_up",
                "back_left_down",
            ]
            stacked_signals = stack_dict_arrays(signals_dict, aformat_keys)
            signals_dict["stacked_signals"] = stacked_signals
        
    audio_data = {**input_data_dict, **signals_dict}

    return audio_data, signals_paths


def stack_dict_arrays(input_data_dict_array: dict, keys: List[str]) -> np.ndarray:
    """
    
    """
    audio_array = []
    for key_i in keys:
        audio_array.append(input_data_dict_array[key_i])

    return audio_array

