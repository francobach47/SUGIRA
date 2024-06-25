"""Plotting functions for Plan View section."""

import base64
import numpy as np
import plotly.graph_objects as go
from utils.formatter import spherical_to_cartesian
from engine.intensity import min_max_normalization


def setup_plotly_plan_view() -> go.Figure:
    """Set up a single plotly 3D layout in Plan View Section."""
    fig = go.Figure()

    camera, buttons = get_plotly_scenes()

    fig.update_layout(
        scene={
            "aspectmode": "cube",
            "xaxis": {
                "showbackground": False,
                "showgrid": False,
                "zeroline": False,
                "showticklabels": False,
                "title": "",
            },
            "yaxis": {
                "showbackground": False,
                "showgrid": False,
                "zeroline": False,
                "showticklabels": False,
                "title": "",
            },
            "zaxis": {
                "showbackground": False,
                "showgrid": False,
                "zeroline": False,
                "showticklabels": False,
                "title": "",
            },
        },
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        font_color="#FFF",
        paper_bgcolor="#1f1b24",
        plot_bgcolor="#1f1b24",
        scene_camera=camera,
        updatemenus=[
            {
                "buttons": buttons,
                "x": 0.05,
            }
        ],
        showlegend=False,
    )

    return fig


def hedgehog_plan_view(
    fig: go.Figure,
    time_peaks: np.ndarray,
    reflex_to_direct: np.ndarray,
    azimuth_peaks: np.ndarray,
    elevation_peaks: np.ndarray,
) -> go.Figure:
    """Create a hedgehog plot for Plan View Section."""
    # time_peaks *= 1000  # seconds to milliseconds
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
            name="time_colorscale",
            marker={
                "color": zero_inserter(normalized_time_peaks),                              
                "colorscale": [
                    [0.0, '#151d44'],
                    [0.15, '#1c4d61'],
                    [0.2, '#677a7d'],
                    [0.25, '#5ea786'],
                    [0.3, '#b6cbb0'],
                    [0.4, '#fef6f4'],
                    [0.5, '#e6b8a2'],
                    [0.7, '#d4786a'],
                    [0.8, '#ae4060'],
                    [0.92, '#76195d'],
                    [1.0, '#cb0000']
                ],
                "colorbar": {
                    "thickness": 40,
                    "tickmode": "array",
                    "tickvals": np.linspace(0,1,10),
                    "ticktext": [f"{val: .1f}ms" for val in np.linspace(np.max(time_peaks),np.min(time_peaks),10)],
                    "title": {
                        "text": "<b>Time</b>",
                        "side": "top",
                        },
                },
                "size": 1,
            },
            line={
                "width": 8,
                "color": zero_inserter(normalized_time_peaks),                
                "colorscale": [
                    [0.0, '#151d44'],
                    [0.1, '#1c4d61'],
                    [0.15, '#677a7d'],
                    [0.2, '#5ea786'],
                    [0.25, '#b6cbb0'],
                    [0.3, '#fef6f4'],
                    [0.4, '#e6b8a2'],
                    [0.5, '#d4786a'],
                    [0.7, '#ae4060'],
                    [0.92, '#76195d'],
                    [1.0, '#cb0000']
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
    )
    return fig


def zero_inserter(array: np.ndarray) -> np.ndarray:
    """Insert zeros between elements in an array."""
    return np.insert(array, np.arange(len(array)), values=0)


def get_plotly_scenes():
    """Get the default Plotly scene configurations."""
    camera = {
        "up": {"x": 0, "y": 0, "z": 1},
        "center": {"x": 0, "y": 0, "z": 0},
        "eye": {"x": 0, "y": 0, "z": 2},
    }

    button0 = {
        "method": "relayout",
        "args": [
            {
                "scene.camera.eye": {"x": 0.0, "y": 0.0, "z": 2},
                "scene.camera.up": {"x": 0.0, "y": 0.0, "z": 1},
            }
        ],
        "label": "X-Y plane",
    }

    button1 = {
        "method": "relayout",
        "args": [{"scene.camera.eye": {"x": 1.3, "y": 1.3, "z": 0.2}}],
        "label": "3D perspective",
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


def put_background_image(fig: go.Figure, image_background: str):
    """Puts the plan in the plotly figure to be edited and visualized in Plan View section."""
    with open(image_background, "rb") as image_file:
        plan_background = base64.b64encode(image_file.read())
    fig.add_layout_image(
        source=f"data:image/png;base64,{plan_background.decode()}",
        xref="paper",
        yref="paper",
        x=0,
        y=1,
        sizex=1,
        sizey=1,
        xanchor="left",
        yanchor="top",
        opacity=1,
        layer="below",
    )
