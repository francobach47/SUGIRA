"""Script to generate .html files to be embed in GUI as plot."""

from plotly import graph_objects as go
import plotly.express


def generate_html(fig: go.Figure, html_name: str = "sugira.html") -> None:
    """
    Generates a .html file with the plotly code associated.

    Parameters
    ----------
    fig : go.Figure
        Plotly figure.
    html_name : str
        .html file name.
    """

    fig.write_html(html_name, full_html=True)
    with open(html_name, "r") as file:
        html_content = file.read()

    style_to_insert = """
        <style>
            body {
                background-color: #1f1b24;
            }
        </style>
    """

    html_content = html_content.replace("<head>", "<head>" + style_to_insert)

    with open(html_name, "w") as file:
        file.write(html_content)


def generate_plan_view_json(
    fig: go.Figure, json_name: str = "sugira_plan_view.json"
) -> None:
    """
    Generates a .json file to be edited in the plan view.

    Parameters
    ----------
    fig : go.Figure
        Plotly figure.
    json_name : str
        .json file name.
    """
    fig.write_json(json_name)


def read_from_json(json_name: str = "sugira_plan_view.json") -> go.Figure:
    """
    Read a .json file as plotly figure object.

    Parameters
    ----------
    json_name : str
        .json file name.

    Returns
    -------
    go.Figure object.
    """
    return plotly.io.read_json(json_name)
