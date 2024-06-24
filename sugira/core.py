import numpy as np
from dataclasses import dataclass
from plotly import graph_objects as go
from engine.input import InputProcessorChain
from engine.intensity import (
    bformat_to_intensity,
    crop_2d,
    integrate_intensity_directions,
    reflection_threshold,
)
from engine.w_channel_pre import w_preprocess
from engine.plot import hedgehog, w_channel, setup_plotly_layout
from engine.plot_plan_view import hedgehog_plan_view, setup_plotly_plan_view
from engine.reflections import detect_reflections
from utils.audio_stack import read_signals
from utils.formatter import cartesian_to_spherical
from utils.embed_files import generate_html, generate_plan_view_json
from utils.export_data import export_data


@dataclass
class SeaUrchinAnalyzer:
    """Main class for analyzing Ambisonics impulse responses"""

    input_builder = InputProcessorChain()

    def analyze(
        self,
        input_dict: dict,
        signal_parameters: dict,
        show: bool = False,
    ) -> go.Figure:
        """Analyzes a set of measurements in Ambisonics format and plots a hedgehog
        with the estimated reflections direction.

        Parameters
        ----------
        input_dict : dict
            Dictionary with all the data needed to analyze a set of measurements
            (paths of the measurements, input mode and channels per file).
        signal_parameters : dict
            Dictionary with signal parameters loaded by the user in the main window
            (analysis length, integration window, threshold and frequency correction).
        show : bool, optional
            Shows plotly figure in browser, by default False.

        Returns
        -------
        go.Figure
            Plotly figure with hedgehog and w-channel plot
        """

        input_data_dict = read_signals(input_dict)
        sample_rate = input_data_dict["sample_rate"]

        bformat_signals = self.input_builder.process(input_dict)

        intensity_directions = bformat_to_intensity(
            bformat_signals, sample_rate, signal_parameters["frequency_correction"]
        )

        intensity_directions_cropped = crop_2d(
            signal_parameters["analysis_length"], sample_rate, intensity_directions
        )

        intensity_windowed, time = integrate_intensity_directions(
            intensity_directions_cropped,
            signal_parameters["integration_time"],
            sample_rate,
        )

        intensity, azimuth, elevation = cartesian_to_spherical(intensity_windowed)

        (
            intensity_peaks,
            azimuth_peaks,
            elevation_peaks,
            reflections_idx,
        ) = detect_reflections(intensity, azimuth, elevation)

        (
            reflex_to_direct,
            azimuth_peaks,
            elevation_peaks,
            reflections_idx,
        ) = reflection_threshold(
            signal_parameters["intensity_threshold"],
            intensity_peaks,
            azimuth_peaks,
            elevation_peaks,
            reflections_idx,
        )

        time = time[reflections_idx]

        fig = setup_plotly_layout()
        hedgehog(
            fig,
            time,
            reflex_to_direct,
            azimuth_peaks,
            elevation_peaks,
            signal_parameters,
        )

        w_channel_signal = w_preprocess(
            bformat_signals[0, :],
            int(signal_parameters["integration_time"] * sample_rate),
            signal_parameters["analysis_length"],
            sample_rate,
        )

        export_data(time, w_channel_signal, reflex_to_direct, azimuth, elevation)

        w_channel(
            fig,
            np.arange(0, signal_parameters["analysis_length"], 1 / sample_rate) * 1000,
            w_channel_signal,
            signal_parameters["intensity_threshold"],
            time,
        )

        generate_html(fig)

        # .Json for plan view plot
        fig_plan_view = setup_plotly_plan_view()
        hedgehog_plan_view(
            fig_plan_view, time, reflex_to_direct, azimuth_peaks, elevation_peaks
        )
        generate_plan_view_json(fig_plan_view)

        if show:
            fig.show(
                post_script=["""document.body.style.backgroundColor = "#1f1b24"; """]
            )

        return fig
