from pathlib import Path
from dash import html
import dash_bootstrap_components as dbc

TEMPLATE = "simple_white"
DATA_PATH = Path().resolve() / "data"

footer = html.Footer(
    "Desenvolvido por InMov - © Prefeitura Municipal de Osasco - email@osasco.sp.gov.br",
    style={
        'backgroundColor': '#DEECFC',
        'padding': '1rem',
        'width': '100%',
        'borderTop': '1px solid #dee2e6',
        'textAlign': 'center',
        'fontSize': '0.8rem',
        'marginTop': 'auto', 
    },
    className="w-100",
)