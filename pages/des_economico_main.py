from dash import html, register_page, dcc
import dash_bootstrap_components as dbc
from src.config import footer

register_page(__name__, path="/desenvolvimento_economico", name="Desenvolvimento Econômico")

from pages.des_economico.home import layout

des_economico_layout = html.Div([
    html.Div(layout, style={"marginBottom": "4rem"}),
])

layout = des_economico_layout