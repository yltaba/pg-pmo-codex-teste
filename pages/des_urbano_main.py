from dash import html, register_page, dcc
import dash_bootstrap_components as dbc
from src.config import footer

register_page(__name__, path="/desenvolvimento_urbano", name="Desenvolvimento Urbano")

from pages.des_urbano.home import layout

des_urbano_layout = html.Div([
    html.Div(layout, style={"marginBottom": "4rem"}),
])

layout = des_urbano_layout