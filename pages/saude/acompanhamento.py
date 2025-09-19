import dash
from dash import dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from pathlib import Path
import numpy as np
import glob

dash.register_page(__name__, path="/saude/acompanhamento", name="Acompanhamento")

GOLD_PATH = Path().resolve() / "data"
tb_acompanhamento = pd.read_csv(GOLD_PATH / "tb_acompanhamento_vacina.csv", sep=";")

COLUMN_MAPPING = {
    # Colunas de identificação
    "aluno_bd_alunos": "Nome do Aluno",
    "cpf": "CPF",
    "ra_bd_alunos": "RA",
    "data_nascimento_bd_alunos": "Data de Nascimento",
    "idade_dias": "Idade (dias)",
    "sexo_bd_alunos": "Sexo",
    "serie_bd_alunos": "Série",
    "turno_bd_alunos": "Turno",
    "turma_bd_alunos": "Turma",
    "responsavel_bd_alunos": "Responsável",
    "nome_unidade_bd_alunos": "Unidade Escolar",
    "modalidade_bd_alunos": "Modalidade",
    "ubs_referencia": "UBS de Referência",
    "Febre Amarela Dose 1 - Analise": "Febre Amarela Dose 1",
    "Meningo C Dose 1 - Analise": "Meningo C Dose 1",
    "Meningo C Dose 2 - Analise": "Meningo C Dose 2",
    "Meningo C Dose 3 - Analise": "Meningo C Dose 3",
    "BCG Dose 1 - Analise": "BCG Dose 1",
    "Hepatite B Dose 1 - Analise": "Hepatite B Dose 1",
    "Hepatite B Dose 2 - Analise": "Hepatite B Dose 2",
    "Hepatite B Dose 3 - Analise": "Hepatite B Dose 3",
    "Hepatite B Dose 4 - Analise": "Hepatite B Dose 4",
    "Pneumo 10 Dose 1 - Analise": "Pneumo 10 Dose 1",
    "Pneumo 10 Dose 2 - Analise": "Pneumo 10 Dose 2",
    "Pneumo 10 Dose 3 - Analise": "Pneumo 10 Dose 3",
    "Sarampo Dose 1 - Analise": "Sarampo Dose 1",
    "Sarampo Dose 2 - Analise": "Sarampo Dose 2",
    "Penta Dose 1 - Analise": "Penta Dose 1",
    "Penta Dose 2 - Analise": "Penta Dose 2",
    "Penta Dose 3 - Analise": "Penta Dose 3",
    "Varicela Dose 1 - Analise": "Varicela Dose 1",
}


def get_display_name(column_name):
    return COLUMN_MAPPING.get(column_name, column_name)


# Obter todas as colunas disponíveis
todas_colunas = list(tb_acompanhamento.columns)

# Separar colunas de identificação das colunas de vacinas
colunas_identificacao = [
    col
    for col in todas_colunas
    if any(
        termo in col.lower()
        for termo in [
            "nome",
            "cpf",
            "aluno_bd_alunos",
            "ra",
            "data_nascimento",
            "idade",
            "sexo",
            "serie",
            "turno",
            "turma",
            "responsavel",
            "unidade",
            "modalidade",
            "ubs_referencia",
        ]
    )
    and not any(
        termo in col.lower()
        for termo in [
            "dose",
            "analise",
            "bcg",
            "febre amarela",
            "meningo",
            "hepatite",
            "pneumo",
            "sarampo",
        ]
    )
]

# Colunas de vacinas são todas as que contêm termos relacionados a vacinas
colunas_vacinas = [
    col
    for col in todas_colunas
    if any(
        termo in col.lower()
        for termo in [
            "dose",
            "analise",
            "bcg",
            "febre amarela",
            "meningo",
            "hepatite",
            "pneumo",
            "sarampo",
        ]
    )
]


# Layout da página
layout = dbc.Container(
    [
        html.Br(),
        html.H2("Acompanhamento de imunizações", className="mb-4"),
        # Seção de filtros
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader("Filtros e Configurações"),
                                        dbc.CardBody(
                                            [
                                                # Filtro por unidade
                                                html.Strong(
                                                    "Filtrar por Unidade Escolar:"
                                                ),
                                                dcc.Dropdown(
                                                    id="filtro-unidade",
                                                    options=[
                                                        {
                                                            "label": "Todas",
                                                            "value": "Todas",
                                                        }
                                                    ]
                                                    + [
                                                        {
                                                            "label": unidade,
                                                            "value": unidade,
                                                        }
                                                        for unidade in sorted(
                                                            tb_acompanhamento.get(
                                                                "nome_unidade_bd_alunos",
                                                                [],
                                                            ).unique()
                                                        )
                                                    ],
                                                    value="Todas",
                                                    clearable=False,
                                                    style={
                                                        "marginBottom": "1rem",
                                                        "width": "100%",
                                                        "fontSize": "14px",
                                                        "lineHeight": "1.2",
                                                    },
                                                    optionHeight=50,
                                                ),
                                                # Filtro por série
                                                html.Strong(
                                                    "Filtrar por série do aluno:"
                                                ),
                                                dcc.Dropdown(
                                                    id="filtro-serie",
                                                    options=[
                                                        {
                                                            "label": "Todas",
                                                            "value": "Todas",
                                                        }
                                                    ]
                                                    + [
                                                        {"label": serie, "value": serie}
                                                        for serie in sorted(
                                                            tb_acompanhamento.get(
                                                                "serie_bd_alunos", []
                                                            ).unique()
                                                        )
                                                    ],
                                                    value="Todas",
                                                    clearable=False,
                                                    style={"marginBottom": "1rem"},
                                                ),
                                                # Seleção de colunas de identificação
                                                html.Strong(
                                                    "Colunas de Identificação:"
                                                ),
                                                dcc.Checklist(
                                                    id="colunas-identificacao",
                                                    options=[
                                                        {
                                                            "label": get_display_name(
                                                                col
                                                            ),
                                                            "value": col,
                                                        }
                                                        for col in colunas_identificacao
                                                    ],
                                                    value=colunas_identificacao[
                                                        :2
                                                    ],  # Primeiras 5 colunas por padrão
                                                    style={"marginBottom": "1rem"},
                                                ),
                                                # Seleção de colunas de vacinas
                                                html.Strong("Colunas de Vacinas:"),
                                                dcc.Checklist(
                                                    id="colunas-vacinas",
                                                    options=[
                                                        {
                                                            "label": get_display_name(
                                                                col
                                                            ),
                                                            "value": col,
                                                        }
                                                        for col in colunas_vacinas
                                                    ],
                                                    value=colunas_vacinas[
                                                        :2
                                                    ],  # Primeiras 3 vacinas por padrão
                                                    style={"marginBottom": "1rem"},
                                                ),
                                                # Botões de ação
                                                dbc.Button(
                                                    "Selecionar Todas as Vacinas",
                                                    id="btn-todas-vacinas",
                                                    color="primary",
                                                    outline=True,
                                                    size="sm",
                                                    style={"marginRight": "0.5rem"},
                                                ),
                                                dbc.Button(
                                                    "Limpar Seleção de Vacinas",
                                                    id="btn-limpar-vacinas",
                                                    color="secondary",
                                                    outline=True,
                                                    size="sm",
                                                ),
                                            ]
                                        ),
                                    ],
                                    style={
                                        "height": "100%",
                                        "display": "flex",
                                        "flexDirection": "column",
                                    },
                                )
                            ],
                            width=3,
                        ),
                        # Tabela de dados
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader(
                                            [
                                                html.H5(
                                                    "Tabela de acompanhamento",
                                                    className="mb-0",
                                                ),
                                                html.Small(
                                                    f"Total de registros: {len(tb_acompanhamento)}",
                                                    id="total-registros",
                                                    className="text-muted",
                                                ),
                                            ]
                                        ),
                                        dbc.CardBody(
                                            [
                                                dash_table.DataTable(
                                                    id="tabela-acompanhamento",
                                                    columns=[],
                                                    data=[],
                                                    fixed_rows={"headers": True},
                                                    style_table={
                                                        "overflowX": "auto",
                                                        "overflowY": "auto",
                                                        "height": "100%",
                                                        "border": "thin lightgrey solid",
                                                        "borderRadius": "8px",
                                                        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                                                        "marginTop": "1rem",
                                                    },
                                                    style_cell={
                                                        "fontFamily": 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
                                                        "textAlign": "left",
                                                        "padding": "12px 15px",
                                                        "backgroundColor": "white",
                                                        "minWidth": "100px",
                                                        "maxWidth": "300px",
                                                        "overflow": "hidden",
                                                        "textOverflow": "ellipsis",
                                                    },
                                                    style_header={
                                                        "backgroundColor": "#f8f9fa",
                                                        "fontWeight": "bold",
                                                        "border": "none",
                                                        "borderBottom": "2px solid #dee2e6",
                                                        "textAlign": "left",
                                                        "padding": "12px 15px",
                                                        "whiteSpace": "normal",
                                                    },
                                                    style_data={
                                                        "border": "none",
                                                        "borderBottom": "1px solid #f2f2f2",
                                                        "whiteSpace": "normal",
                                                        "height": "auto",
                                                    },
                                                    style_filter={
                                                        "backgroundColor": "#f8f9fa",
                                                        "padding": "8px 15px",
                                                    },
                                                    filter_action="native",
                                                    export_format="xlsx",
                                                    export_headers="display",
                                                    tooltip_delay=0,
                                                    tooltip_duration=None,
                                                    editable=False,
                                                    row_selectable=False,
                                                    row_deletable=False,
                                                    page_action="native",
                                                    page_current=0,
                                                    page_size=50,
                                                    css=[
                                                        {
                                                            "selector": ".dash-table-tooltip",
                                                            "rule": "background-color: white; font-family: system-ui; padding: 8px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);",
                                                        },
                                                        # {
                                                        #     "selector": ".dash-table-container",
                                                        #     "rule": "height: 900px !important; max-height: 900px !important;",
                                                        # },
                                                        # {
                                                        #     "selector": ".dash-spreadsheet-container",
                                                        #     "rule": "height: 900px !important; max-height: 900px !important;",
                                                        # },
                                                        {
                                                            "selector": ".export::after",
                                                            "rule": "content: 'Exportar Excel'; font-size: 12px;",
                                                        },
                                                        {
                                                            "selector": ".export",
                                                            "rule": "font-size: 0;",
                                                        },
                                                    ],
                                                )
                                            ],
                                            style={
                                                "padding": "1rem",
                                                "height": "100%",
                                                "display": "flex",
                                                "flexDirection": "column",
                                            },
                                        ),
                                    ],
                                    style={
                                        "height": "100%",
                                        "display": "flex",
                                        "flexDirection": "column",
                                    },
                                )
                            ],
                            width=9,
                        ),
                    ],
                    style={"height": "100%"},
                ),
            ],
        ),
    ],
    fluid=True,
)


# Callbacks
@callback(
    [
        Output("tabela-acompanhamento", "columns"),
        Output("tabela-acompanhamento", "data"),
        Output("tabela-acompanhamento", "style_data_conditional"),
    ],
    [
        Input("filtro-unidade", "value"),
        Input("filtro-serie", "value"),
        Input("colunas-identificacao", "value"),
        Input("colunas-vacinas", "value"),
    ],
)
def atualizar_tabela(unidade, serie, col_id, col_vac):
    # Aplicar filtros
    df_filtrado = tb_acompanhamento.copy()

    if unidade != "Todas":
        df_filtrado = df_filtrado[df_filtrado["nome_unidade_bd_alunos"] == unidade]

    if serie != "Todas":
        df_filtrado = df_filtrado[df_filtrado["serie_bd_alunos"] == serie]

    # Combinar colunas selecionadas
    colunas_selecionadas = col_id + col_vac

    # Filtrar apenas as colunas que existem no dataframe
    colunas_existentes = [
        col for col in colunas_selecionadas if col in df_filtrado.columns
    ]

    if not colunas_existentes:
        return [], [], []

    df_final = df_filtrado[colunas_existentes]

    # Criar colunas para a tabela
    columns = [{"name": get_display_name(col), "id": col} for col in colunas_existentes]

    # Converter para formato de dados da tabela
    data = df_final.to_dict("records")

    # Gerar estilização condicional dinamicamente para colunas de vacinas
    style_conditional = []

    # Adicionar estilização para linhas ímpares
    style_conditional.append(
        {
            "if": {"row_index": "odd"},
            "backgroundColor": "#fcfcfc",
        }
    )

    # Adicionar estilização para colunas de vacinas
    for col in col_vac:
        if col in colunas_existentes:
            # Estilização para "Atrasada" - vermelho
            style_conditional.append(
                {
                    "if": {"filter_query": f'{{{col}}} = "Atrasada"', "column_id": col},
                    "backgroundColor": "#ffebee",
                    "color": "#c62828",
                    "fontWeight": "bold",
                }
            )

            # Estilização para "Programada" - amarelo
            style_conditional.append(
                {
                    "if": {
                        "filter_query": f'{{{col}}} = "Programada"',
                        "column_id": col,
                    },
                    "backgroundColor": "#fff3e0",
                    "color": "#ef6c00",
                    "fontWeight": "bold",
                }
            )

    return columns, data, style_conditional


@callback(
    Output("colunas-vacinas", "value"),
    [Input("btn-todas-vacinas", "n_clicks"), Input("btn-limpar-vacinas", "n_clicks")],
    prevent_initial_call=True,  # Adiciona esta linha para evitar execução inicial
)
def controlar_selecao_vacinas(btn_todas, btn_limpar):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "btn-todas-vacinas":
        return colunas_vacinas
    elif button_id == "btn-limpar-vacinas":
        return []

    return dash.no_update


@callback(
    Output("total-registros", "children"),
    [
        Input("filtro-unidade", "value"),
        Input("filtro-serie", "value"),
        Input("colunas-identificacao", "value"),
        Input("colunas-vacinas", "value"),
    ],
)
def atualizar_total_registros(unidade, serie, col_id, col_vac):
    # Aplicar filtros (mesma lógica do callback da tabela)
    df_filtrado = tb_acompanhamento.copy()

    if unidade != "Todas":
        df_filtrado = df_filtrado[df_filtrado["nome_unidade_bd_alunos"] == unidade]

    if serie != "Todas":
        df_filtrado = df_filtrado[df_filtrado["serie_bd_alunos"] == serie]

    # Combinar colunas selecionadas
    colunas_selecionadas = col_id + col_vac

    # Filtrar apenas as colunas que existem no dataframe
    colunas_existentes = [
        col for col in colunas_selecionadas if col in df_filtrado.columns
    ]

    if not colunas_existentes:
        return f"Total de registros: 0"

    df_final = df_filtrado[colunas_existentes]

    return f"Total de registros: {len(df_final)}"
