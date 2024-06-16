"""Input module"""
from enum import Enum
from abc import ABC, abstractmethod

import numpy as np
from scipy.signal import fftconvolve

from utils.filters import CapsuleMicsCorrection
from utils.formatter import convert_ambisonics_a_to_b


class InputFormat(Enum):
    """Enum class for accessing the existing Input Formats"""

    LSS = "lss"
    AFORMAT = "aformat"
    BFORMAT = "bformat"
 

class InputProcessor(ABC):
    """Base interface for the input processor."""

    @abstractmethod
    def process(self,input_dict: dict) -> dict:
        """Abstract method to be overwritten by concrete implementations of
        the input processor."""


class LSSInputProcessor(InputProcessor):
    """Algorithm for obtaining RIRs from LSS+IF."""
    def process(self,input_dict: dict) -> dict:
        """Reads all measurementes, convolves with IF, obtains new A-format signals array.  

        Args:
            input_dict: Dictionary with LSS measurement arrays and IF.

        Returns:
            dict: Overwritten input_dict with A-Format signals.
        """
        if input_dict["input_mode"] != InputFormat.LSS:
            return input_dict
    
        input_dict["stacked_signals"] = np.apply_along_axis(
            lambda array: fftconvolve(array, input_dict["inverse_filter"], mode = "full"),
            axis = 1,
            arr = input_dict["stacked_signals"],
        )
        input_dict["input_mode"] = InputFormat.AFORMAT
        
        return input_dict


class AFormatProcessor(InputProcessor):
    """
    """
    def process(self, input_dict: dict) -> dict:
        """
        """
        if input_dict["input_mode"] != InputFormat.AFORMAT:
            return input_dict
        input_dict["stacked_signals"] = convert_ambisonics_a_to_b(
            input_dict["stacked_signals"][0, :],
            input_dict["stacked_signals"][1, :],
            input_dict["stacked_signals"][2, :],
            input_dict["stacked_signals"][3, :],
        )
        input_dict["input_mode"] = InputFormat.BFORMAT
        return input_dict
    

class BFormatProcessor(InputProcessor):
    """
    """
    def process(self, input_dict: dict) -> dict:    
        """
        """
        if input_dict["input_mode"] != InputFormat.BFORMAT and not bool(input_dict["frequency_correction"]):
            input_dict = input_dict
        
        
        mic_corrector = CapsuleMicsCorrection(input_dict["sample_rate"])
        input_dict["stacked_signals"][0, :] = mic_corrector.omni_correction(input_dict["stacked_signals"][0, :])
        input_dict["stacked_signals"][1:, :] = mic_corrector.axis_correction(input_dict["stacked_signals"][1:, :])
        input_dict["input_mode"] = InputFormat.BFORMAT

        return input_dict
    

class InputProcessorChain:
    """
    """
    def __init__(self):
        self.processors = [LSSInputProcessor(), AFormatProcessor(), BFormatProcessor()]
    
    def process(self, input_dict: dict) -> dict:
        """
        """
        for processor in self.processors:
            input_dict = processor.process(input_dict)

        return input_dict["stacked_signals"]