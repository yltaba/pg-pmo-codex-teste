from dash import html, register_page
import dash_bootstrap_components as dbc
from src.utils import create_info_popover

register_page(__name__, path="/desenvolvimento_urbano/loteamento", name="Mapa de Loteamento")

layout = html.Div(
    [
        html.Br(),
        # LOTEAMENTO DE OSASCO
        html.Div(
            [
                html.H4("Loteamento de Osasco", id="mapa_loteamento"),
                html.P([
                    "Fonte: ",
                    html.A("OzMundi", href="https://ozmundi.osasco.sp.gov.br/forms/login.php", target="_blank")
                ]),
                create_info_popover(
                    "info-zoneamento",
                    "urbano_loteamento",
                ),
                html.Iframe(
                    src="https://ozmundi.osasco.sp.gov.br/misc/base_loteamento/", # https://ozmundi.osasco.sp.gov.br/misc/base_zoneamento/
                    style={
                        "width": "100%",
                        "height": "1000px",
                        "border": "none",
                    },
                ),
            ],
            className="section-container",
            style={"marginBottom": "3rem"},
        )

    ]
)
