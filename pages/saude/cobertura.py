import dash
from dash import dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from pathlib import Path
import numpy as np

dash.register_page(__name__, path="/saude/cobertura", name="Cobertura vacinal")

GOLD_PATH = Path().resolve() / "data"


def processar_tabela_vacina(vacina: str):
    df = pd.read_csv(
        GOLD_PATH / f"gold_{vacina}.csv", sep=";", dtype={"cpf_aluno_bd_alunos": str}
    )

    df = df[
        [
            "modalidade_bd_alunos",
            "nome_unidade_bd_alunos",
            "aluno_bd_alunos",
            "cpf_aluno_bd_alunos",
            "cpf_bd_imunizacao",
            "data_nascimento_bd_alunos",
            "idade_dias",
            "ra_bd_alunos",
            "sexo_bd_alunos",
            "serie_bd_alunos",
            "turma_bd_alunos",
            "responsavel_bd_alunos",
            "data_vacinacao_bd_imunizacao",
            "vacina_bd_imunizacao",
            "dose_bd_imunizacao",
        ]
    ]

    df = renomear_df(df)

    return df


def renomear_df(df):
    df = df.rename(
        columns={
            "nome_unidade_bd_alunos": "Unidade",
            "modalidade_bd_alunos": "Modalidade",
            "aluno_bd_alunos": "Aluno",
            "cpf_aluno_bd_alunos": "CPF",
            "data_nascimento_bd_alunos": "Data de nascimento",
            "idade_dias": "Idade",
            "ra_bd_alunos": "RA",
            "sexo_bd_alunos": "Sexo",
            "serie_bd_alunos": "Série",
            "turma_bd_alunos": "Turma",
            "responsavel_bd_alunos": "Responsável",
            "data_vacinacao_bd_imunizacao": "Data de vacinação",
            "vacina_bd_imunizacao": "Vacina",
            "dose_bd_imunizacao": "Dose",
        }
    )
    return df


def get_cobertura_color(taxa):
    """
    Retorna a cor baseada na taxa de cobertura:
    0-40%: vermelho
    40-70%: laranja
    70-95%: amarelo
    95-100%: verde
    """
    if taxa < 0.4:
        return "#ffebee"  # vermelho claro
    elif taxa < 0.7:
        return "#fff3e0"  # laranja claro
    elif taxa < 0.95:
        return "#fff8e1"  # amarelo claro
    else:
        return "#e8f5e8"  # verde claro


df_febre_amarela = processar_tabela_vacina("febre_amarela")
taxa_cobertura_febre_amarela = len(
    df_febre_amarela.loc[df_febre_amarela["cpf_bd_imunizacao"].notna()]
) / len(df_febre_amarela)


df_bcg = processar_tabela_vacina("bcg")
taxa_cobertura_bcg = len(df_bcg.loc[df_bcg["cpf_bd_imunizacao"].notna()]) / len(df_bcg)


df_hepb = processar_tabela_vacina("hepb")
df_hepb["contador_doses"] = np.where(df_hepb["Vacina"].isna(), 0, 1)
soma_doses_hepb = df_hepb.groupby("cpf_bd_imunizacao", as_index=False).agg(
    {"contador_doses": "sum"}
)
soma_doses_hepb["cobertura"] = np.where(soma_doses_hepb["contador_doses"] >= 3, 1, 0)
taxa_cobertura_hepb = soma_doses_hepb["cobertura"].mean()


df_meningoc1 = processar_tabela_vacina("meningoc1")
df_meningoc1["size_cpf"] = df_meningoc1.groupby("CPF")["CPF"].transform("size")
df_meningoc1["cobertura"] = np.where(df_meningoc1["size_cpf"] >= 2, 1, 0)
taxa_cobertura_meningoc1 = (
    df_meningoc1[["CPF", "cobertura"]].drop_duplicates()["cobertura"].mean()
)

df_meningoc_reforco = processar_tabela_vacina("meningoc_reforco")
taxa_cobertura_meningoc_reforco = len(df_meningoc_reforco.loc[df_meningoc_reforco["Vacina"].notna()]) / len(
    df_meningoc_reforco
)

# Gerar tabelas detalhadas para apresentar no Modal
TABLE_FONT = "'Source Sans Pro', 'Helvetica Neue', Arial, sans-serif"

tabela_detalhada_febre_amarela = dash_table.DataTable(
    id="datatable-febre-amarela",
    columns=[
        {
            "name": col,
            "id": col,
            "filter_options": {
                "case": "insensitive",
                "placeholder_text": "Filtrar dados...",
                "logic": "contains",
            },
        }
        for col in df_febre_amarela.drop(columns=["cpf_bd_imunizacao"]).columns
    ],
    data=df_febre_amarela.drop(columns=["cpf_bd_imunizacao"]).to_dict("records"),
    filter_action="native",
    sort_action="native",
    sort_mode="multi",
    page_action="native",
    page_current=0,
    page_size=5,
    style_table={"overflowX": "auto", "maxHeight": "400px", "marginTop": "20px"},
    style_header={
        "backgroundColor": "rgb(230, 230, 230)",
        "fontWeight": "bold",
        "textAlign": "center",
        "fontFamily": TABLE_FONT,
    },
    style_cell={
        "textAlign": "left",
        "padding": "10px",
        "minWidth": "100px",
        "maxWidth": "500px",
        "overflow": "hidden",
        "textOverflow": "ellipsis",
        "fontFamily": TABLE_FONT,
    },
    style_data_conditional=[
        {
            "if": {"row_index": "odd"},
            "backgroundColor": "rgb(248, 248, 248)",
        }
    ],
    tooltip_header={
        "backgroundColor": "rgb(230, 230, 230)",
        "color": "black",
        "fontFamily": TABLE_FONT,
    },
    tooltip_delay=0,
    tooltip_duration=None,
    export_format="xlsx",
    export_headers="display",
    export_columns="visible",
)

tabela_detalhada_bcg = dash_table.DataTable(
    id="datatable-bcg",
    columns=[
        {
            "name": col,
            "id": col,
            "filter_options": {
                "case": "insensitive",
                "placeholder_text": "Filtrar dados...",
                "logic": "contains",
            },
        }
        for col in df_bcg.drop(columns=["cpf_bd_imunizacao"]).columns
    ],
    data=df_bcg.drop(columns=["cpf_bd_imunizacao"]).to_dict("records"),
    filter_action="native",
    sort_action="native",
    sort_mode="multi",
    page_action="native",
    page_current=0,
    page_size=5,
    style_table={"overflowX": "auto", "maxHeight": "400px", "marginTop": "20px"},
    style_header={
        "backgroundColor": "rgb(230, 230, 230)",
        "fontWeight": "bold",
        "textAlign": "center",
        "fontFamily": TABLE_FONT,
    },
    style_cell={
        "textAlign": "left",
        "padding": "10px",
        "minWidth": "100px",
        "maxWidth": "500px",
        "overflow": "hidden",
        "textOverflow": "ellipsis",
        "fontFamily": TABLE_FONT,
    },
    style_data_conditional=[
        {
            "if": {"row_index": "odd"},
            "backgroundColor": "rgb(248, 248, 248)",
        }
    ],
    tooltip_header={
        "backgroundColor": "rgb(230, 230, 230)",
        "color": "black",
        "fontFamily": TABLE_FONT,
    },
    tooltip_delay=0,
    tooltip_duration=None,
    export_format="xlsx",
    export_headers="display",
    export_columns="visible",
)

tabela_detalhada_hepb = dash_table.DataTable(
    id="datatable-hepb",
    columns=[
        {
            "name": col,
            "id": col,
            "filter_options": {
                "case": "insensitive",
                "placeholder_text": "Filtrar dados...",
                "logic": "contains",
            },
        }
        for col in df_hepb.drop(columns=["cpf_bd_imunizacao", "contador_doses"]).columns
    ],
    data=df_hepb.drop(columns=["cpf_bd_imunizacao", "contador_doses"]).to_dict(
        "records"
    ),
    filter_action="native",
    sort_action="native",
    sort_mode="multi",
    page_action="native",
    page_current=0,
    page_size=5,
    style_table={"overflowX": "auto", "maxHeight": "400px", "marginTop": "20px"},
    style_header={
        "backgroundColor": "rgb(230, 230, 230)",
        "fontWeight": "bold",
        "textAlign": "center",
        "fontFamily": TABLE_FONT,
    },
    style_cell={
        "textAlign": "left",
        "padding": "10px",
        "minWidth": "100px",
        "maxWidth": "500px",
        "overflow": "hidden",
        "textOverflow": "ellipsis",
        "fontFamily": TABLE_FONT,
    },
    style_data_conditional=[
        {
            "if": {"row_index": "odd"},
            "backgroundColor": "rgb(248, 248, 248)",
        }
    ],
    tooltip_header={
        "backgroundColor": "rgb(230, 230, 230)",
        "color": "black",
        "fontFamily": TABLE_FONT,
    },
    tooltip_delay=0,
    tooltip_duration=None,
    export_format="xlsx",
    export_headers="display",
    export_columns="visible",
)

tabela_detalhada_meningoc1 = dash_table.DataTable(
    id="datatable-meningoc1",
    columns=[
        {
            "name": col,
            "id": col,
            "filter_options": {
                "case": "insensitive",
                "placeholder_text": "Filtrar dados...",
                "logic": "contains",
            },
        }
        for col in df_meningoc1.drop(
            columns=["cpf_bd_imunizacao", "size_cpf", "cobertura"]
        ).columns
    ],
    data=df_meningoc1.drop(
        columns=["cpf_bd_imunizacao", "size_cpf", "cobertura"]
    ).to_dict("records"),
    filter_action="native",
    sort_action="native",
    sort_mode="multi",
    page_action="native",
    page_current=0,
    page_size=5,
    style_table={"overflowX": "auto", "maxHeight": "400px", "marginTop": "20px"},
    style_header={
        "backgroundColor": "rgb(230, 230, 230)",
        "fontWeight": "bold",
        "fontFamily": TABLE_FONT,
        "textAlign": "center",
    },
    style_cell={
        "textAlign": "left",
        "padding": "10px",
        "minWidth": "100px",
        "maxWidth": "500px",
        "overflow": "hidden",
        "textOverflow": "ellipsis",
        "fontFamily": TABLE_FONT,
    },
    style_data_conditional=[
        {
            "if": {"row_index": "odd"},
            "backgroundColor": "rgb(248, 248, 248)",
        }
    ],
    tooltip_header={
        "backgroundColor": "rgb(230, 230, 230)",
        "color": "black",
        "fontFamily": TABLE_FONT,
    },
    tooltip_delay=0,
    tooltip_duration=None,
    export_format="xlsx",
    export_headers="display",
    export_columns="visible",
)

tabela_detalhada_meningoc_reforco = dash_table.DataTable(
    id="datatable-meningoc_reforco",
    columns=[
        {
            "name": col,
            "id": col,
            "filter_options": {
                "case": "insensitive",
                "placeholder_text": "Filtrar dados...",
                "logic": "contains",
            },
        }
        for col in df_meningoc_reforco.drop(
            columns=["cpf_bd_imunizacao"]
        ).columns
    ],
    data=df_meningoc_reforco.drop(
        columns=["cpf_bd_imunizacao"]
    ).to_dict("records"),
    filter_action="native",
    sort_action="native",
    sort_mode="multi",
    page_action="native",
    page_current=0,
    page_size=5,
    style_table={"overflowX": "auto", "maxHeight": "400px", "marginTop": "20px"},
    style_header={
        "backgroundColor": "rgb(230, 230, 230)",
        "fontWeight": "bold",
        "fontFamily": TABLE_FONT,
        "textAlign": "center",
    },
    style_cell={
        "textAlign": "left",
        "padding": "10px",
        "minWidth": "100px",
        "maxWidth": "500px",
        "overflow": "hidden",
        "textOverflow": "ellipsis",
        "fontFamily": TABLE_FONT,
    },
    style_data_conditional=[
        {
            "if": {"row_index": "odd"},
            "backgroundColor": "rgb(248, 248, 248)",
        }
    ],
    tooltip_header={
        "backgroundColor": "rgb(230, 230, 230)",
        "color": "black",
        "fontFamily": TABLE_FONT,
    },
    tooltip_delay=0,
    tooltip_duration=None,
    export_format="xlsx",
    export_headers="display",
    export_columns="visible",
)

# Gerar o Modal e Card para mostrar dados detalhados da vacina
modal_febre_amarela = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Vacina Febre Amarela")),
        dbc.ModalBody(
            [
                html.Div(
                    [
                        # Estatísticas resumidas
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardBody(
                                                    [
                                                        html.H6(
                                                            "Alunos elegíveis",
                                                            className="card-title",
                                                        ),
                                                        html.H4(
                                                            f"{len(df_febre_amarela):,}",
                                                            className="text-primary",
                                                        ),
                                                    ]
                                                )
                                            ]
                                        )
                                    ],
                                    width=4,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardBody(
                                                    [
                                                        html.H6(
                                                            "Alunos vacinados",
                                                            className="card-title",
                                                        ),
                                                        html.H4(
                                                            f"{len(df_febre_amarela.loc[df_febre_amarela['cpf_bd_imunizacao'].notna()]):,}",
                                                            className="text-primary",
                                                        ),
                                                    ]
                                                )
                                            ]
                                        )
                                    ],
                                    width=4,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardBody(
                                                    [
                                                        html.H6(
                                                            "Cobertura vacinal",
                                                            className="card-title",
                                                        ),
                                                        html.H4(
                                                            f"{taxa_cobertura_febre_amarela:.1%}",
                                                            className="text-info",
                                                        ),
                                                    ]
                                                )
                                            ]
                                        )
                                    ],
                                    width=4,
                                ),
                            ],
                            className="mb-4",
                        ),
                        # DataTable robusta
                        html.H6("Dados detalhados:", className="mt-3"),
                        tabela_detalhada_febre_amarela,
                    ]
                )
            ]
        ),
        dbc.ModalFooter(
            dbc.Button(
                "Fechar",
                id="close-modal-febre-amarela",
                className="ms-auto",
                n_clicks=0,
            )
        ),
    ],
    id="modal-febre-amarela",
    is_open=False,
    size="xl",
    scrollable=True,
)

card_febre_amarela = [
    dbc.Row(
        [
            dbc.Col(
                [
                    # FEBRE AMARELA - Envolvido em div clicável
                    html.Div(
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    [
                                        html.Span("Febre Amarela"),
                                        html.I(
                                            className="fas fa-eye",
                                            style={
                                                "marginLeft": "8px",
                                                "fontSize": "0.8rem",
                                                "opacity": "0.7",
                                            },
                                        ),
                                    ],
                                    style={
                                        "height": "3rem",
                                        "display": "flex",
                                        "alignItems": "center",
                                        "justifyContent": "center",
                                        "background-color": get_cobertura_color(
                                            taxa_cobertura_febre_amarela
                                        ),
                                        "fontWeight": "bold",
                                        "cursor": "pointer",
                                    },
                                ),
                                dbc.CardBody(
                                    [
                                        html.P(
                                            f"{taxa_cobertura_febre_amarela:.1%}",
                                            style={"fontSize": "1.5rem"},
                                        )
                                    ],
                                ),
                            ],
                            style={
                                "width": "200px",
                                "height": "120px",
                                "marginBottom": "1rem",
                                "textAlign": "center",
                            },
                        ),
                        id="card-febre-amarela",
                        style={"cursor": "pointer"},
                    ),
                ],
                width=3,
            ),
        ]
    ),
]

modal_bcg = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Dados da Cobertura - BCG")),
        dbc.ModalBody(
            [
                html.Div(
                    [
                        # Estatísticas resumidas
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardBody(
                                                    [
                                                        html.H6(
                                                            "Alunos elegíveis",
                                                            className="card-title",
                                                        ),
                                                        html.H4(
                                                            f"{len(df_bcg):,}",
                                                            className="text-primary",
                                                        ),
                                                    ]
                                                )
                                            ]
                                        )
                                    ],
                                    width=4,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardBody(
                                                    [
                                                        html.H6(
                                                            "Alunos vacinados",
                                                            className="card-title",
                                                        ),
                                                        html.H4(
                                                            f"{len(df_bcg.loc[df_bcg['cpf_bd_imunizacao'].notna()]):,}",
                                                            className="text-success",
                                                        ),
                                                    ]
                                                )
                                            ]
                                        )
                                    ],
                                    width=4,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardBody(
                                                    [
                                                        html.H6(
                                                            "Cobertura vacinal",
                                                            className="card-title",
                                                        ),
                                                        html.H4(
                                                            f"{taxa_cobertura_bcg:.1%}",
                                                            className="text-info",
                                                        ),
                                                    ]
                                                )
                                            ]
                                        )
                                    ],
                                    width=4,
                                ),
                            ],
                            className="mb-4",
                        ),
                        # DataTable robusta
                        html.H6("Dados detalhados:", className="mt-3"),
                        tabela_detalhada_bcg,
                    ]
                )
            ]
        ),
        dbc.ModalFooter(
            dbc.Button("Fechar", id="close-modal-bcg", className="ms-auto", n_clicks=0)
        ),
    ],
    id="modal-bcg",
    is_open=False,
    size="xl",
    scrollable=True,
)

card_bcg = [
    dbc.Row(
        [
            dbc.Col(
                [
                    # BCG - Envolvido em div clicável
                    html.Div(
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    [
                                        html.Span("BCG"),
                                        html.I(
                                            className="fas fa-eye",
                                            style={
                                                "marginLeft": "8px",
                                                "fontSize": "0.8rem",
                                                "opacity": "0.7",
                                            },
                                        ),
                                    ],
                                    style={
                                        "height": "3rem",
                                        "display": "flex",
                                        "alignItems": "center",
                                        "justifyContent": "center",
                                        "background-color": get_cobertura_color(
                                            taxa_cobertura_bcg
                                        ),
                                        "fontWeight": "bold",
                                        "cursor": "pointer",
                                    },
                                ),
                                dbc.CardBody(
                                    [
                                        html.P(
                                            f"{taxa_cobertura_bcg:.1%}",
                                            style={"fontSize": "1.5rem"},
                                        )
                                    ],
                                ),
                            ],
                            style={
                                "width": "200px",
                                "height": "120px",
                                "marginBottom": "1rem",
                                "textAlign": "center",
                            },
                        ),
                        id="card-bcg",
                        style={"cursor": "pointer"},
                    ),
                ],
                width=3,
            ),
        ]
    ),
]

modal_hepb = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Dados da Cobertura - HEPB")),
        dbc.ModalBody(
            [
                html.Div(
                    [
                        # Estatísticas resumidas
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardBody(
                                                    [
                                                        html.H6(
                                                            "Alunos elegíveis",
                                                            className="card-title",
                                                        ),
                                                        html.H4(
                                                            f"{len(df_hepb):,}",
                                                            className="text-primary",
                                                        ),
                                                    ]
                                                )
                                            ]
                                        )
                                    ],
                                    width=4,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardBody(
                                                    [
                                                        html.H6(
                                                            "Alunos vacinados",
                                                            className="card-title",
                                                        ),
                                                        html.H4(
                                                            f"{len(df_hepb.loc[df_hepb['cpf_bd_imunizacao'].notna()]):,}",
                                                            className="text-success",
                                                        ),
                                                    ]
                                                )
                                            ]
                                        )
                                    ],
                                    width=4,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardBody(
                                                    [
                                                        html.H6(
                                                            "Cobertura vacinal",
                                                            className="card-title",
                                                        ),
                                                        html.H4(
                                                            f"{taxa_cobertura_hepb:.1%}",
                                                            className="text-info",
                                                        ),
                                                    ]
                                                )
                                            ]
                                        )
                                    ],
                                    width=4,
                                ),
                            ],
                            className="mb-4",
                        ),
                        # DataTable robusta
                        html.H6("Dados detalhados:", className="mt-3"),
                        tabela_detalhada_hepb,
                    ]
                )
            ]
        ),
        dbc.ModalFooter(
            dbc.Button("Fechar", id="close-modal-hepb", className="ms-auto", n_clicks=0)
        ),
    ],
    id="modal-hepb",
    is_open=False,
    size="xl",
    scrollable=True,
)

card_hepb = [
    dbc.Row(
        [
            dbc.Col(
                [
                    # BCG - Envolvido em div clicável
                    html.Div(
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    [
                                        html.Span("Hepatite B"),
                                        html.I(
                                            className="fas fa-eye",
                                            style={
                                                "marginLeft": "8px",
                                                "fontSize": "0.8rem",
                                                "opacity": "0.7",
                                            },
                                        ),
                                    ],
                                    style={
                                        "height": "3rem",
                                        "display": "flex",
                                        "alignItems": "center",
                                        "justifyContent": "center",
                                        "background-color": get_cobertura_color(
                                            taxa_cobertura_hepb
                                        ),
                                        "fontWeight": "bold",
                                        "cursor": "pointer",
                                    },
                                ),
                                dbc.CardBody(
                                    [
                                        html.P(
                                            f"{taxa_cobertura_hepb:.1%}",
                                            style={"fontSize": "1.5rem"},
                                        )
                                    ],
                                ),
                            ],
                            style={
                                "width": "200px",
                                "height": "120px",
                                "marginBottom": "1rem",
                                "textAlign": "center",
                            },
                        ),
                        id="card-hepb",
                        style={"cursor": "pointer"},
                    ),
                ],
                width=3,
            ),
        ]
    ),
]

modal_meningoc1 = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Dados da Cobertura - Meningo 1")),
        dbc.ModalBody(
            [
                html.Div(
                    [
                        # Estatísticas resumidas
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardBody(
                                                    [
                                                        html.H6(
                                                            "Alunos elegíveis",
                                                            className="card-title",
                                                        ),
                                                        html.H4(
                                                            f"{len(df_meningoc1):,}",
                                                            className="text-primary",
                                                        ),
                                                    ]
                                                )
                                            ]
                                        )
                                    ],
                                    width=4,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardBody(
                                                    [
                                                        html.H6(
                                                            "Alunos vacinados",
                                                            className="card-title",
                                                        ),
                                                        html.H4(
                                                            f"{len(df_meningoc1.loc[df_meningoc1['cpf_bd_imunizacao'].notna()]):,}",
                                                            className="text-success",
                                                        ),
                                                    ]
                                                )
                                            ]
                                        )
                                    ],
                                    width=4,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardBody(
                                                    [
                                                        html.H6(
                                                            "Cobertura vacinal",
                                                            className="card-title",
                                                        ),
                                                        html.H4(
                                                            f"{taxa_cobertura_meningoc1:.1%}",
                                                            className="text-info",
                                                        ),
                                                    ]
                                                )
                                            ]
                                        )
                                    ],
                                    width=4,
                                ),
                            ],
                            className="mb-4",
                        ),
                        # DataTable robusta
                        html.H6("Dados detalhados:", className="mt-3"),
                        tabela_detalhada_meningoc1,
                    ]
                )
            ]
        ),
        dbc.ModalFooter(
            dbc.Button(
                "Fechar", id="close-modal-meningoc1", className="ms-auto", n_clicks=0
            )
        ),
    ],
    id="modal-meningoc1",
    is_open=False,
    size="xl",
    scrollable=True,
)

card_meningoc1 = [
    dbc.Row(
        [
            dbc.Col(
                [
                    # BCG - Envolvido em div clicável
                    html.Div(
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    [
                                        html.Span("Meningo C"),
                                        html.I(
                                            className="fas fa-eye",
                                            style={
                                                "marginLeft": "8px",
                                                "fontSize": "0.8rem",
                                                "opacity": "0.7",
                                            },
                                        ),
                                    ],
                                    style={
                                        "height": "3rem",
                                        "display": "flex",
                                        "alignItems": "center",
                                        "justifyContent": "center",
                                        "background-color": get_cobertura_color(
                                            taxa_cobertura_meningoc1
                                        ),
                                        "fontWeight": "bold",
                                        "cursor": "pointer",
                                    },
                                ),
                                dbc.CardBody(
                                    [
                                        html.P(
                                            f"{taxa_cobertura_meningoc1:.1%}",
                                            style={"fontSize": "1.5rem"},
                                        )
                                    ],
                                ),
                            ],
                            style={
                                "width": "200px",
                                "height": "120px",
                                "marginBottom": "1rem",
                                "textAlign": "center",
                            },
                        ),
                        id="card-meningoc1",
                        style={"cursor": "pointer"},
                    ),
                ],
                width=3,
            ),
        ]
    ),
]

modal_meningoc_reforco = dbc.Modal(
    [ 
        dbc.ModalHeader(dbc.ModalTitle("Dados da Cobertura - Meningo C Reforço")),
        dbc.ModalBody(
            [
                html.Div(
                    [
                        # Estatísticas resumidas
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardBody(
                                                    [
                                                        html.H6(
                                                            "Alunos elegíveis",
                                                            className="card-title",
                                                        ),
                                                        html.H4(
                                                            f"{len(df_meningoc_reforco):,}",
                                                            className="text-primary",
                                                        ),
                                                    ]
                                                )
                                            ]
                                        )
                                    ],
                                    width=4,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardBody(
                                                    [
                                                        html.H6(
                                                            "Alunos vacinados",
                                                            className="card-title",
                                                        ),
                                                        html.H4(
                                                            f"{len(df_meningoc_reforco.loc[df_meningoc_reforco['cpf_bd_imunizacao'].notna()]):,}",
                                                            className="text-success",
                                                        ),
                                                    ]
                                                )
                                            ]
                                        )
                                    ],
                                    width=4,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardBody(
                                                    [
                                                        html.H6(
                                                            "Cobertura vacinal",
                                                            className="card-title",
                                                        ),
                                                        html.H4(
                                                            f"{taxa_cobertura_meningoc_reforco:.1%}",
                                                            className="text-info",
                                                        ),
                                                    ]
                                                )
                                            ]
                                        )
                                    ],
                                    width=4,
                                ),
                            ],
                            className="mb-4",
                        ),
                        # DataTable robusta
                        html.H6("Dados detalhados:", className="mt-3"),
                        tabela_detalhada_meningoc_reforco,
                    ]
                )
            ]
        ),
        dbc.ModalFooter(
            dbc.Button(
                "Fechar", id="close-modal-meningoc_reforco", className="ms-auto", n_clicks=0
            )
        ),
    ],
    id="modal-meningoc_reforco",
    is_open=False,
    size="xl",
    scrollable=True,
)

card_meningoc_reforco = [
    dbc.Row(
        [
            dbc.Col(
                [
                    # BCG - Envolvido em div clicável
                    html.Div(
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    [
                                        html.Span("Meningo C (Reforço)"),
                                        html.I(
                                            className="fas fa-eye",
                                            style={
                                                "marginLeft": "8px",
                                                "fontSize": "0.8rem",
                                                "opacity": "0.7",
                                            },
                                        ),
                                    ],
                                    style={
                                        "height": "3rem",
                                        "display": "flex",
                                        "alignItems": "center",
                                        "justifyContent": "center",
                                        "background-color": get_cobertura_color(
                                            taxa_cobertura_meningoc_reforco
                                        ),
                                        "fontWeight": "bold",
                                        "cursor": "pointer",
                                    },
                                ),
                                dbc.CardBody(
                                    [
                                        html.P(
                                            f"{taxa_cobertura_meningoc_reforco:.1%}",
                                            style={"fontSize": "1.5rem"},
                                        )
                                    ],
                                ),
                            ],
                            style={
                                "width": "200px",
                                "height": "120px",
                                "marginBottom": "1rem",
                                "textAlign": "center",
                            },
                        ),
                        id="card-meningoc_reforco",
                        style={"cursor": "pointer"},
                    ),
                ],
                width=3,
            ),
        ]
    ),
]

layout = dbc.Container(
    [
        html.Br(),
        html.Div(
            [
                html.H2("Cobertura vacinal"),
            ]
        ),
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H6("Legenda da cobertura:", className="mb-3"),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    style={
                                                        "width": "20px",
                                                        "height": "20px",
                                                        "backgroundColor": "#ffebee",
                                                        "border": "1px solid #ccc",
                                                        "display": "inline-block",
                                                        "marginRight": "8px",
                                                    }
                                                ),
                                                html.Span("0-40%"),
                                            ],
                                            style={
                                                "display": "flex",
                                                "alignItems": "center",
                                            },
                                        )
                                    ],
                                    width=6,
                                ),
                                dbc.Col(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    style={
                                                        "width": "20px",
                                                        "height": "20px",
                                                        "backgroundColor": "#fff3e0",
                                                        "border": "1px solid #ccc",
                                                        "display": "inline-block",
                                                        "marginRight": "8px",
                                                    }
                                                ),
                                                html.Span("40-70%"),
                                            ],
                                            style={
                                                "display": "flex",
                                                "alignItems": "center",
                                            },
                                        )
                                    ],
                                    width=6,
                                ),
                            ],
                            className="mb-2",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    style={
                                                        "width": "20px",
                                                        "height": "20px",
                                                        "backgroundColor": "#fff8e1",
                                                        "border": "1px solid #ccc",
                                                        "display": "inline-block",
                                                        "marginRight": "8px",
                                                    }
                                                ),
                                                html.Span("> 70 %"),
                                            ],
                                            style={
                                                "display": "flex",
                                                "alignItems": "center",
                                            },
                                        )
                                    ],
                                    width=6,
                                ),
                                dbc.Col(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    style={
                                                        "width": "20px",
                                                        "height": "20px",
                                                        "backgroundColor": "#e8f5e8",
                                                        "border": "1px solid #ccc",
                                                        "display": "inline-block",
                                                        "marginRight": "8px",
                                                    }
                                                ),
                                                html.Span(
                                                    "Maior ou igual a meta de cobertura"
                                                ),
                                            ],
                                            style={
                                                "display": "flex",
                                                "alignItems": "center",
                                            },
                                        )
                                    ],
                                    width=6,
                                ),
                            ]
                        ),
                    ]
                )
            ],
            style={
                "marginBottom": "20px",
                "backgroundColor": "#f8f9fa",
                "maxWidth": "600px",
            },
        ),
        html.Div(
            [
                html.P("Clique nos cards para ver os dados detalhados."),
            ]
        ),
        html.Div(
            [
                html.H5("Ao nascer:"),
                html.Br(),
                html.Div(card_bcg),
                html.Br(),
            ]
        ),
        html.Div(
            [
                html.H5("Menores de um ano de idade:"),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(html.Div(card_febre_amarela), width=3),
                        dbc.Col(html.Div(card_hepb), width=3),
                        dbc.Col(html.Div(card_meningoc1), width=3),
                    ]
                ),
                html.Br(),
            ]
        ),
        html.Div(
            [
                html.H5("1 ano de idade:"),
                html.Br(),
                html.Div(card_meningoc_reforco),
                html.Br(),
            ]
        ),
        # Modais para mostrar os dados
        modal_febre_amarela,
        modal_bcg,
        modal_hepb,
        modal_meningoc1,
        modal_meningoc_reforco,
    ]
)


# Callback para abrir o modal da Febre Amarela
@callback(
    Output("modal-febre-amarela", "is_open"),
    [
        Input("card-febre-amarela", "n_clicks"),
        Input("close-modal-febre-amarela", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def toggle_modal_febre_amarela(n1, n2):
    ctx = dash.callback_context
    if not ctx.triggered:
        return False

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "card-febre-amarela":
        return True
    elif button_id == "close-modal-febre-amarela":
        return False

    return False


# Callback para abrir o modal do BCG
@callback(
    Output("modal-bcg", "is_open"),
    [Input("card-bcg", "n_clicks"), Input("close-modal-bcg", "n_clicks")],
    prevent_initial_call=True,
)
def toggle_modal_bcg(n1, n2):
    ctx = dash.callback_context
    if not ctx.triggered:
        return False

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "card-bcg":
        return True
    elif button_id == "close-modal-bcg":
        return False

    return False


# Callback para abrir o modal do Hepatite B
@callback(
    Output("modal-hepb", "is_open"),
    [Input("card-hepb", "n_clicks"), Input("close-modal-hepb", "n_clicks")],
    prevent_initial_call=True,
)
def toggle_modal_hepb(n1, n2):
    ctx = dash.callback_context
    if not ctx.triggered:
        return False

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "card-hepb":
        return True
    elif button_id == "close-modal-hepb":
        return False

    return False


# Callback para abrir o modal do Meningo C
@callback(
    Output("modal-meningoc1", "is_open"),
    [Input("card-meningoc1", "n_clicks"), Input("close-modal-meningoc1", "n_clicks")],
    prevent_initial_call=True,
)
def toggle_modal_meningoc1(n1, n2):
    ctx = dash.callback_context
    if not ctx.triggered:
        return False

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "card-meningoc1":
        return True
    elif button_id == "close-modal-meningoc1":
        return False

    return False

# Callback para abrir o modal do Meningo C
@callback(
    Output("modal-meningoc_reforco", "is_open"),
    [Input("card-meningoc_reforco", "n_clicks"), Input("close-modal-meningoc_reforco", "n_clicks")],
    prevent_initial_call=True,
)
def toggle_modal_meningoc_reforco(n1, n2):
    ctx = dash.callback_context
    if not ctx.triggered:
        return False

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "card-meningoc_reforco":
        return True
    elif button_id == "close-modal-meningoc_reforco":
        return False

    return False
