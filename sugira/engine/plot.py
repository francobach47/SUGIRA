"""Plotting functions."""
from typing import Tuple, Dict
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


from utils.formatter import spherical_to_cartesian
from engine.intensity import min_max_normalization


def hedgehog(
    fig: go.Figure,
    time_peaks: np.ndarray,
    reflex_to_direct: np.ndarray,
    azimuth_peaks: np.ndarray,
    elevation_peaks: np.ndarray,
    signal_parameters: dict
) -> go.Figure:
    """
    Create a hedgehog plot.
    """
    
    time_peaks *= 1000  # seconds to miliseconds
    normalized_intensities = min_max_normalization(reflex_to_direct)
    x, y, z = spherical_to_cartesian(
        normalized_intensities, azimuth_peaks, elevation_peaks
    )
    normalized_time_peaks = np.flip(min_max_normalization(time_peaks))
        
    fig.add_trace(
        go.Scatter3d(
            x=zero_inserter(x),
            y=zero_inserter(y),
            z=zero_inserter(z),
            marker={
                "color": zero_inserter(normalized_intensities),
                 "colorscale": [
                    [0.0, '#353535'],
                    [0.1, '#595854'],
                    [0.15, '#7d7967'],
                    [0.2, '#9b9066'],
                    [0.25, '#bcab67'],
                    [0.4, '#f6ab2c'],
                    [0.5, '#f6832c'],
                    [0.7, '#f65d2c'],
                    [0.9, '#dd2942'],
                    [1.0, '#ff0800']
                ],
                "colorbar": {
                    "thickness": 40,
                    "tickmode": "array",
                    "tickvals": np.linspace(0,1,10),
                    "ticktext": [f"{val: .1f} dB" for val in np.linspace(np.min(reflex_to_direct),np.max(reflex_to_direct),10)],
                    "title": {
                        "text": "<b>Level</b>",
                        "side": "top",
                        },
                },
                "size": 3,
            },
            line={
                "width": 8,
                "color": zero_inserter(normalized_intensities),
                "colorscale": [
                    [0.0, '#353535'],
                    [0.1, '#595854'],
                    [0.15, '#7d7967'],
                    [0.2, '#9b9066'],
                    [0.25, '#bcab67'],
                    [0.4, '#f6ab2c'],
                    [0.5, '#f6832c'],
                    [0.7, '#f65d2c'],
                    [0.9, '#dd2942'],
                    [1.0, '#ff0800']
                ],
            },
            customdata=np.stack(
                (
                    zero_inserter(reflex_to_direct),
                    zero_inserter(time_peaks),
                    zero_inserter(azimuth_peaks),
                    zero_inserter(elevation_peaks),
                ),
                axis=-1,
            ),
            hovertemplate="<b>Reflection-to-direct [dB]:</b> %{customdata[0]:.2f} dB <br>"
            + "<b>Time [ms]: </b>%{customdata[1]:.2f} ms <br>"
            + "<b>Azimuth [°]: </b>%{customdata[2]:.2f}° <br>"
            + "<b>Elevation [°]: </b>%{customdata[3]:.2f}° <extra></extra>",
            showlegend=False,
        ),
        row=1,
        col=1,
    )

    fig.update_layout(
        scene={
            "aspectmode": "cube",
            "xaxis": {
                "showbackground": False,
                "showticklabels": True,
            },
            "xaxis_title": "◀ Front - Rear ▶",
            "yaxis": {
                "showbackground": False,
                "showticklabels": True,
            },
            "yaxis_title": "◀ Left - Right ▶",
            "zaxis": {
                "showbackground": False,
                "showticklabels": True,
            },
            "zaxis_title": "◀ Up - Down ▶",
        },
    )

    add_info_box(fig, signal_parameters)

    return fig

def w_channel(
    fig: go.Figure,
    time: np.ndarray,
    w_channel: np.ndarray,
    ylim: float,
    time_reflections: np.ndarray,
) -> go.Figure:
    """_summary_

    Parameters
    ----------
    fig : go.Figure
        _description_
    """
    fig.add_trace(
        go.Scatter(
            x=time,
            y=w_channel,
            line={
                "color": "rgba(255, 99, 71, 1)",
                
            },
            customdata=time, 
            hovertemplate="<b>Time [ms]:</b> %{customdata:.2f} ms <extra></extra>",
            showlegend=False,
        )
    )
    fig.update_layout(yaxis_range=[0, 1], xaxis_range=[0, max(time)])
    fig.update_xaxes(title_text="Time [ms]", row=2, col=1)
    fig.update_yaxes(title_text="Amplitude", row=2, col=1)


def setup_plotly_layout() -> go.Figure:
    """_summary_

    Parameters
    ----------
    fig : go.Figure
        _description_

    Returns
    -------
    _type_
        _description_
    """
    initial_fig = go.Figure()
    fig = make_subplots(
        rows=2,
        cols=1,
        row_heights=[0.8, 0.2],
        vertical_spacing=0.05,
        specs=[[{"type": "scene"}], [{"type": "xy"}]],
        subplot_titles=("<b>Hedgehog</b>", "<b>Omnidirectional channel</b>"),
        figure=initial_fig,
    )

    camera, buttons = get_plotly_scenes()

    fig.update_layout(
        margin={"l": 0, "r": 100, "t": 30, "b": 0},
        font_color="#FFF",
        paper_bgcolor="#1f1b24",
        plot_bgcolor="#1f1b24",
        scene_camera=camera,
        updatemenus=[{
            "buttons": buttons,
            "x": 0.05, 
        }],
        showlegend=False,   
    )
    return fig


def get_plotly_scenes() -> Tuple[Dict]:
    """_summary_

    Returns
    -------
    Tuple[Dict]
        _description_
    """
    camera = {
        "up": {"x": 0, "y": 0, "z": 1},
        "center": {"x": 0, "y": 0, "z": 0},
        "eye": {"x": 1.3, "y": 1.3, "z": 0.2},
    }

    button0 = {
        "method": "relayout",
        "args": [{"scene.camera.eye": {"x": 1.3, "y": 1.3, "z": 0.2}}],
        "label": "3D perspective",
    }

    button1 = {
        "method": "relayout",
        "args": [
            {
                "scene.camera.eye": {"x": 0.0, "y": 0.0, "z": 2},
                "scene.camera.up": {"x": 0.0, "y": 0.0, "z": 2},
            }
        ],
        "label": "X-Y plane",
    }

    button2 = {
        "method": "relayout",
        "args": [{"scene.camera.eye": {"x": 0.0, "y": 2, "z": 0.0}}],
        "label": "X-Z plane",
    }

    button3 = {
        "method": "relayout",
        "args": [{"scene.camera.eye": {"x": 2, "y": 0.0, "z": 0.0}}],
        "label": "Y-Z plane",
    }
    buttons = [button0, button1, button2, button3]
    return camera, buttons


def add_info_box(fig: go.Figure, signal_parameters: dict) -> go.Figure:
    info_text = (
        f"<b>Threshold:</b> {signal_parameters['intensity_threshold']} dB<br>"
        f"<b>Analysis Length:</b> {signal_parameters['analysis_length']} s<br>"
        f"<b>Integration Window:</b> {signal_parameters['integration_time']} s<br>"
        f"<b>Frequency Correction:</b> {signal_parameters['frequency_correction']}<br>"
    )
    
    fig.add_annotation(
        text=info_text,
        xref="paper", yref="paper",
        x=1,
        y=1,
        showarrow=False,
        align="left",
        font=dict(
            family="Arial",
            size=14,
            color="#FFF"
        ),
        bordercolor="#FFFFFF",
        borderwidth=2,
        borderpad=4,
        bgcolor="#1f1b24",
        opacity=1
    )
    return fig


def zero_inserter(array: np.ndarray) -> np.ndarray:
    """_summary_

    Parameters
    ----------
    array : np.ndarray
        _description_

    Returns
    -------
    np.ndarray
        _description_
    """
    return np.insert(array, np.arange(len(array)), values=0)
