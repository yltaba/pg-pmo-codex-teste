import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
from pathlib import Path

dash.register_page(__name__, path="/saude/vacinas", name="Painel de Vacinação")


# Função local para criar opções de dropdown
def get_options_dropdown_saude(df, column):
    sorted_values = sorted(df[column].dropna().unique())
    return [{"label": x, "value": x} for x in sorted_values]


DATA_PATH = Path().resolve() / "data"
n_vacinas_escola = pd.read_csv(DATA_PATH / "n_vacinas_escola.csv", sep=";")
n_vacinas_escola = n_vacinas_escola.query("data_vacinacao_ano >= 2015")
n_vacinas_escola["vacina"] = n_vacinas_escola["vacina"].str.capitalize()
n_vacinas_escola["modalidade"] = n_vacinas_escola["modalidade"].str.capitalize()
n_vacinas_escola["tipo_unidade"] = n_vacinas_escola["tipo_unidade"].str.capitalize()

n_alunos = pd.read_csv(DATA_PATH / "n_alunos.csv", sep=";")
anos = sorted(n_vacinas_escola["data_vacinacao_ano"].unique())
ano_min, ano_max = min(anos), max(anos)

layout = dbc.Container(
    [
        html.Br(),
        html.H2("Mapa de imunização"),
        dbc.Row(
            [
                # COLUNA 1: Filtros
                dbc.Col(
                    [
                        html.Div(
                            [
                                dbc.Button(
                                    "Limpar filtros",
                                    id="btn-limpar-filtros",
                                    color="secondary",
                                    outline=True,
                                    style={"marginBottom": "1rem", "width": "100%"},
                                ),
                                html.Br(),
                                html.Strong("Selecione o ano:"),
                                dcc.Dropdown(
                                    id="dropdown-ano",
                                    options=[
                                        {"label": str(ano), "value": ano}
                                        for ano in anos
                                    ],
                                    value=ano_max,
                                    clearable=False,
                                    style={"width": "100%"},
                                ),
                                html.Br(),
                                html.Strong("Selecione a modalidade escolar:"),
                                dcc.Dropdown(
                                    id="dropdown-modalidade",
                                    options=[{"label": "Todas", "value": "Todas"}]
                                    + get_options_dropdown_saude(
                                        n_vacinas_escola, "modalidade"
                                    ),
                                    value="Todas",
                                    clearable=False,
                                ),
                                html.Br(),
                                html.Strong("Selecione o tipo de unidade escolar:"),
                                dcc.Dropdown(
                                    id="dropdown-tp-unidade",
                                    options=[{"label": "Todas", "value": "Todas"}]
                                    + get_options_dropdown_saude(
                                        n_vacinas_escola, "tipo_unidade"
                                    ),
                                    value="Todas",
                                    clearable=False,
                                ),
                                html.Br(),
                                html.Strong("Selecione a escola:"),
                                dcc.Dropdown(
                                    id="select-escola-mapa",
                                    value="Todas",
                                    searchable=True,
                                    style={
                                        "width": "100%",
                                        "fontSize": "14px",
                                        "lineHeight": "1.2",
                                    },
                                    optionHeight=50,
                                ),
                                html.Br(),
                                html.Strong("Selecione a vacina:"),
                                dcc.Dropdown(
                                    id="dropdown-vacina-mapa",
                                    options=[{"label": "Todas", "value": "Todas"}]
                                    + get_options_dropdown_saude(
                                        n_vacinas_escola, "vacina"
                                    ),
                                    value="Todas",
                                    style={
                                        "width": "100%",
                                        "fontSize": "14px",
                                        "lineHeight": "1.2",
                                    },
                                    optionHeight=50,
                                ),
                                html.Br(),
                            ]
                        )
                    ],
                    xs=12,
                    md=3,
                    style={"padding": "2rem 1rem"},
                ),
                # COLUNA 2: Mapa
                dbc.Col(
                    [dcc.Graph(id="mapa-vacinacao", style={"width": "100%"})],
                    xs=12,
                    md=7,
                    style={"padding": "2rem 1rem"},
                ),
                # COLUNA 3: Cards descritivos
                dbc.Col(
                    [
                        html.Div(
                            id="info-escola-selecionada", style={"marginTop": "2rem"}
                        ),
                    ],
                    xs=12,
                    md=2,
                ),
            ],
            style={"height": "100vh"},
        ),
    ],
    fluid=True,
)
