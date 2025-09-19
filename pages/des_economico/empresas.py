from dash import dcc, html, register_page
import dash_bootstrap_components as dbc
import plotly.express as px
from babel.numbers import format_decimal, format_currency, format_percent

from src.utils import (
    calcular_pib_atual,
    calcular_variacao_pib,
    create_info_popover,
    get_options_dropdown,
)
from src.config import TEMPLATE
from src.load_data import load_data


register_page(
    __name__, path="/desenvolvimento_economico/empresas", name="Empresas"
)

################################ DESENVOLVIMENTO ECONÔMICO #################################
# CARREGAR DADOS
all_data = load_data()

# ABERTURA E ENCERRAMENTO DE EMPRESAS
opcoes_des_atividade = get_options_dropdown(
    all_data, "abertura_encerramento_empresas_cleaned", "des_atividade"
)
opcoes_cnae_rais_tamanho = get_options_dropdown(
    all_data, "rais_tamanho_estabelecimento", "descricao_secao_cnae"
)

dropdown_des_atividade = dcc.Dropdown(
    id="filtro-des-atividade",
    options=[{"label": "Todos", "value": "Todos"}] + opcoes_des_atividade,
    value="Todos",
    clearable=False,
    className="mb-3",
)

fig_empresas_ano = dbc.Col(
    html.Div(
        [
            dropdown_des_atividade,
            dcc.Graph(id="fig-abertura-encerramento", config={"displayModeBar": False}),
        ]
    ),
    width=10,
)

saldo_empresas = (
    all_data["abertura_encerramento_empresas_cleaned"]
    .loc[
        all_data["abertura_encerramento_empresas_cleaned"]["ano"]
        == all_data["abertura_encerramento_empresas_cleaned"]["ano"].max()
    ]["n_empresas_abertas"]
    .sum()
)

card_saldo_empresas = html.Div(
    [
        html.Div(
            [
                html.H5(
                    "Saldo de empresas",
                    className="card-title",
                ),
                html.Div(
                    [
                        html.Div(
                            id="card-saldo-empresas-value", className="card-value"
                        ),
                        html.Span(
                            id="card-variacao-saldo-empresas-arrow",
                            style={"fontSize": "24px", "marginLeft": "8px"},
                        ),
                    ],
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "center",
                    },
                    className="card-value-container",
                ),
                html.P(
                    f"{all_data['abertura_encerramento_empresas_cleaned']['ano'].max()}",
                    className="card-subtitle",
                    style={
                        "fontSize": "12px",
                        "textAlign": "center",
                        "color": "#6c757d",
                    },
                ),
            ],
            className="card-content",
        )
    ],
    className="custom-card",
)

coluna_cartao_saldo_empresas = dbc.Col(
    [
        card_saldo_empresas,
        html.Div(style={"height": "20px"}),
    ],
    width=2,
    className="cards-container",
)

cartoes_abertura_encerramento = dbc.Row(
    [
        coluna_cartao_saldo_empresas,
        fig_empresas_ano,
    ],
    className="main-content-row",
)


fig_rais_tamanho_estabelecimento = html.Div(
    [
        html.H4("Porte das empresas de Osasco"),
        create_info_popover(
            "info-rais-tamanho-estabelecimento",
            "economico_porte_empresas",
        ),
        html.Div(
            [
                html.Label("Selecione um ano:", style={"fontWeight": "light"}),
                dcc.Slider(
                    id="filtro-ano-rais-tamanho-estabelecimento",
                    min=min(all_data["rais_tamanho_estabelecimento"]["ano"]),
                    max=max(all_data["rais_tamanho_estabelecimento"]["ano"]),
                    value=2024,
                    marks={
                        str(year): str(year)
                        for year in all_data["rais_tamanho_estabelecimento"]["ano"].unique()
                    },
                    step=None,
                    className="mb-3",
                    updatemode="drag",
                    included=False,
                    tooltip={"placement": "bottom", "always_visible": True},
                ),
                html.Label("Selecione uma Seção da CNAE:", style={"fontWeight": "light"}),
                dcc.Dropdown(
                    id="filtro-cnae-rais-tamanho-estabelecimento",
                    options=[{"label": "Todos", "value": "Todos"}] + opcoes_cnae_rais_tamanho,
                    value="Todos",
                    clearable=False,
                    className="mb-3",
                    style={"width": "70%"},
                ),
                dcc.Graph(id="fig-rais-tamanho-estabelecimento"),
            ]
        ),
    ],
    className="section-container",
    style={"marginBottom": "3rem"},
)


# LAYOUT DA PÁGINA
layout = html.Div(
    [
        html.Br(),
        # ABERTURA E ENCERRAMENTO DE EMPRESAS
        html.Div(
            [
                html.H4("Abertura e encerramento de empresas computadas pelo SIGT"),
                create_info_popover(
                    "info-abertura-encerramento",
                    "economico_abertura_encerramento_empresas",
                ),
                cartoes_abertura_encerramento,
            ],
            className="section-container",
            style={"marginBottom": "3rem"},
        ),
        fig_rais_tamanho_estabelecimento,
    ]
)
