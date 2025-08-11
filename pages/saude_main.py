from dash import html, register_page, dcc
import dash_bootstrap_components as dbc
from src.config import footer

register_page(__name__, path="/saude", name="Saúde")

from pages.saude.home import layout

saude_layout = html.Div([
    html.Div(layout, style={"marginBottom": "4rem"}),
])

layout = saude_layout