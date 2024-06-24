""""Audio utilities"""

from typing import List
import numpy as np  
import soundfile as sf


def read_signals(input_data_dict: dict) -> dict:
    """
    
    """

    sample_rate = 48000

    for key_i, path_i in input_data_dict.items():
        try:
            signal, sample_rate = sf.read(path_i)
            input_data_dict[key_i] = signal.T
        except:
            pass    
    
    input_data_dict["sample_rate"] = sample_rate

    if input_data_dict["channels_per_file"] == 1:
        if input_data_dict["input_mode"] == "bformat":
            bformat_keys = ["w_channel", "x_channel", "y_channel", "z_channel"]
            input_data_dict["stacked_signals"] = stack_dict_arrays(input_data_dict, bformat_keys)
        else:
            aformat_keys = [
                "front_left_up",
                "front_right_down",
                "back_right_up",
                "back_left_down",
            ]
            input_data_dict["stacked_signals"] = stack_dict_arrays(input_data_dict, aformat_keys)
    
    return input_data_dict


def stack_dict_arrays(input_data_dict_array: dict, keys: List[str]) -> np.ndarray:
    """
    
    """
    audio_array = []
    for key_i in keys:
        audio_array.append(input_data_dict_array[key_i])

    return audio_array

