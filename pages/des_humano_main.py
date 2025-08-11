from dash import html, register_page, dcc
import dash_bootstrap_components as dbc
from src.config import footer

register_page(__name__, path="/desenvolvimento_humano", name="Desenvolvimento Humano")

from pages.des_humano.home import layout

des_humano_layout = html.Div([
    html.Div(layout, style={"marginBottom": "4rem"}),
])

layout = des_humano_layout