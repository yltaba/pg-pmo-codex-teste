from dash import html, register_page
import dash_bootstrap_components as dbc
from src.utils import create_info_popover

register_page(__name__, path="/desenvolvimento_urbano/zoneamento", name="Mapa de Zoneamento")

layout = html.Div(
    [
        html.Br(),
        # ZONEAMENTO DE OSASCO
        html.Div(
            [
                html.H4("Zoneamento de Osasco", id="mapa_zoneamento"),
                html.P([
                    "Fonte: ",
                    html.A("OzMundi", href="https://ozmundi.osasco.sp.gov.br/forms/login.php", target="_blank")
                ]),
                create_info_popover(
                    "info-zoneamento",
                    "urbano_zoneamento",
                ),
                html.Iframe(
                    src="https://ozmundi.osasco.sp.gov.br/misc/base_zoneamento_2024_v2/",
                    style={
                        "width": "100%",
                        "height": "1000px",
                        "border": "none",
                    },
                ),
            ],
            className="section-container",
            style={"marginBottom": "3rem"},
        ),

    ]
)
