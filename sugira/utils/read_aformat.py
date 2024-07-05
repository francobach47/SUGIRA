from pathlib import Path
from functools import singledispatch
from traceback import print_exc
from typing import List, Dict, Tuple, Union

import numpy as np
import soundfile as sf


@singledispatch
def read_a(audio_path: Union[str, Path]) -> Tuple[np.ndarray, float]:
    """
    Read Ambisonics A-format audio file.

    Parameters
    ----------
    audio_path : Union[str, Path]
        Path to the audio file.

    Returns
    -------
    Tuple[np.ndarray, float]
        Tuple containing the audio signal array and the sample rate.
    """

    signal, sample_rate = sf.read(audio_path)
    signal = signal.T
    assert signal.shape[0] == 4, (
        f"Audio file {str(audio_path)} with shape {signal.shape} does not contain 4 channels "
        f"so it cannot be an A-format Ambisonics"
    )

    return signal, sample_rate


@read_a.register(list)
def _(audio_paths: List[str]) -> Tuple[np.ndarray, float]:
    """
    Read multiple Ambisonics A-format audio files.

    Parameters
    ----------
    audio_paths : List[str]
        List of paths to the audio files.

    Returns
    -------
    Tuple[np.ndarray, float]
        Tuple containing the concatenated audio signal array and the sample rate.
    """

    assert (isinstance(audio_paths, (str, Path, list))) or (
        len(audio_paths) in (1, 4)
    ), "A list of four .WAV files or one .WAV file with four channels is espected"

    audio_array = []
    for audio_i in audio_paths:
        try:
            audio_array_i, sample_rate = sf.read(audio_i)
            audio_array.append(audio_array_i)
        except sf.SoundFileError:
            print_exc()

    return np.array(audio_array), sample_rate


@read_a.register(dict)
def _(audio_paths: Dict[str, str]) -> Tuple[np.ndarray, float]:
    """
    Read Ambisonics A-format audio files from a dictionary of paths.

    Parameters
    ----------
    audio_paths : Dict[str, str]
        Dictionary where keys are channel names and values are paths to the audio files.

    Returns
    -------
    Tuple[np.ndarray, float]
        Tuple containing the concatenated audio signal array and the sample rate.
    """

    ordered_aformat_channels = (
        "front_left_up",
        "front_right_down",
        "back_right_up",
        "back_left_down",
    )
    try:
        audio_data = {
            cardioid_channel: dict(zip(("signal", "sample_rate"), sf.read(path)))
            for cardioid_channel, path in audio_paths.items()
        }

        # refactor from here
        audio_signals = [
            audio_data[channel_name]["signal"]
            for channel_name in ordered_aformat_channels
        ]
        sample_rates = [
            audio_data[channel_name]["sample_rate"]
            for channel_name in ordered_aformat_channels
        ]
        assert len(set(sample_rates)) == 1, "Differents sample rates were found"

        signals_array = np.array(audio_signals)
        return signals_array, sample_rates[0]
    except sf.SoundFileError:
        print_exc()
