from dash import dcc, html, register_page, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from src.utils import (
    create_info_popover,
    get_options_dropdown,
)
from src.config import TEMPLATE
from src.load_data import load_data


register_page(
    __name__, path="/gestao_receita_propria", name="Gestão da Receita Própria"
)

# CARREGAR DADOS
all_data = load_data()
tb_sigt_receita_categ_tributo = all_data["tb_sigt_receita_categ_tributo"].copy()
tb_sigt_valor_imovel_tributo = all_data["tb_sigt_valor_imovel_tributo"].copy()


def processar_base_receita_categ_tributo(tb_sigt_receita_categ_tributo):

    tb_sigt_receita_categ_tributo["TOTAL_RECEITA_MILHOES"] = (
        tb_sigt_receita_categ_tributo["TOTAL_RECEITA"] / 1_000_000
    )

    tb_sigt_receita_categ_tributo = tb_sigt_receita_categ_tributo.drop(
        columns=["TOTAL_RECEITA"]
    )

    ano_order = ["2023", "2024", "2025"]
    tb_sigt_receita_categ_tributo["ANO"] = pd.Categorical(
        tb_sigt_receita_categ_tributo["ANO"].astype(str),
        categories=ano_order,
        ordered=True,
    )

    return tb_sigt_receita_categ_tributo


def gerar_gold_receita_tributo_categoria(tb_sigt_receita_categ_tributo):

    arr_mvw_receita_categ_tributo = processar_base_receita_categ_tributo(
        tb_sigt_receita_categ_tributo
    )

    df_ano = (
        arr_mvw_receita_categ_tributo.groupby(
            ["ANO", "CATEGORIA_TRIBUTO"], as_index=False, observed=True
        )
        .agg({"TOTAL_RECEITA_MILHOES": "sum"})
        .round(2)
        .sort_values(by=["TOTAL_RECEITA_MILHOES"], ascending=True)
    )

    df_ano["TOTAL_ANO"] = df_ano.groupby(["ANO"], observed=True)[
        "TOTAL_RECEITA_MILHOES"
    ].transform("sum")
    df_ano["PERCENTUAL"] = (df_ano["TOTAL_RECEITA_MILHOES"] / df_ano["TOTAL_ANO"]) * 100

    category_order = (
        df_ano.groupby("CATEGORIA_TRIBUTO")["TOTAL_RECEITA_MILHOES"]
        .sum()
        .sort_values(ascending=False)
        .index
    )

    df_ano["CATEGORIA_TRIBUTO"] = pd.Categorical(
        df_ano["CATEGORIA_TRIBUTO"], categories=category_order, ordered=True
    )

    df_ano = df_ano.drop(columns=["TOTAL_ANO"]).sort_values(
        ["CATEGORIA_TRIBUTO", "ANO"]
    )

    return df_ano


def gerar_gold_receita_tributo_subcategoria(IMPOSTO, tb_sigt_receita_categ_tributo):

    receita_categ_tributo = processar_base_receita_categ_tributo(
        tb_sigt_receita_categ_tributo
    )

    receita_categ_tributo_select = receita_categ_tributo.loc[
        receita_categ_tributo["CATEGORIA_TRIBUTO"] == IMPOSTO
    ].copy()

    return receita_categ_tributo_select


receita_categ_tributo = gerar_gold_receita_tributo_categoria(
    tb_sigt_receita_categ_tributo
)
receita_categ_tributo = receita_categ_tributo.sort_values(
    by=["ANO", "TOTAL_RECEITA_MILHOES"], ascending=True
)
fig_categ_tributo = px.bar(
    receita_categ_tributo,
    y="CATEGORIA_TRIBUTO",
    x="TOTAL_RECEITA_MILHOES",
    color="ANO",
    color_discrete_sequence=["#1f77b4", "#123E5C", "#2ca02c"],
    barmode="group",
    labels={
        "CATEGORIA_TRIBUTO": "Categoria Tributária",
        "TOTAL_RECEITA_MILHOES": "Receita (Milhões)",
        "ANO": "Ano",
    },
    hover_data={"PERCENTUAL"},
    template=TEMPLATE,
    orientation="h",
)
fig_categ_tributo.update_traces(
    hovertemplate="<b>%{y}</b><br>Ano: %{fullData.name}<br>Receita: %{x:,.2f} mi<br>Percentual: %{customdata[0]:.2f}%",
    marker_line_color="black",
    marker_line_width=1,
    width=0.2,
)
fig_categ_tributo.update_layout(
    xaxis_tickangle=-45,
    showlegend=True,
    legend_title="Ano",
    bargap=0.5,
    margin=dict(t=20, b=40, l=40, r=20),
)


receita_categ_tributo_total = receita_categ_tributo.groupby(
    "ANO", as_index=False, observed=True
).agg({"TOTAL_RECEITA_MILHOES": "sum"})
receita_categ_tributo_total["TOTAL_RECEITA_MILHOES"] = receita_categ_tributo_total[
    "TOTAL_RECEITA_MILHOES"
].round(2)

fig_ano_tributo = px.bar(
    receita_categ_tributo_total,
    x="ANO",
    y="TOTAL_RECEITA_MILHOES",
    text="TOTAL_RECEITA_MILHOES",
    template=TEMPLATE,
    labels={
        "ANO": "Ano",
        "TOTAL_RECEITA_MILHOES": "Receita (Milhões R$)",
    },
    color="ANO",  # Cores diferentes por ano
    color_discrete_sequence=["#1f77b4", "#123E5C", "#2ca02c"],
)
# Rótulo fora da barra e com formato ajustado
fig_ano_tributo.update_traces(
    textposition="outside",
    texttemplate="%{text:.1f}",
    marker_line_color="black",
    marker_line_width=1,
    width=0.5,
)
# Ajustes de layout
fig_ano_tributo.update_layout(
    margin=dict(t=20, b=40, l=40, r=20),
    showlegend=False,
)


coluna_receita_categ_tributo = dbc.Row(
    [
        dbc.Col(
            [
                html.H4("Receita total arrecadada por ano"),
                create_info_popover(
                    "info-receita-anual",
                    "receita_total",
                ),
                dcc.Graph(figure=fig_ano_tributo, config={"displayModeBar": False}),
            ],
            width=4,
        ),
        dbc.Col(
            [
                html.H4("Receita anual por categoria tributária (2023-2025)"),
                create_info_popover(
                    "info-receita-categ-tributo",
                    "receita_categ_tributo",
                ),
                dcc.Graph(figure=fig_categ_tributo),
            ],
            width=8,
        ),
    ]
)


opcoes_categ_tributo = get_options_dropdown(
    all_data, "tb_sigt_receita_categ_tributo", "CATEGORIA_TRIBUTO"
)
dropdown_categ_tributo = dcc.Dropdown(
    id="filtro-categ-tributo",
    options=[{"label": "Todos", "value": "Todos"}] + opcoes_categ_tributo,
    value="IPTU ORIGEM",
    clearable=False,
    className="mb-3",
)


def criar_tabela_valor_imovel_tributo_avancada():
    """
    Cria uma tabela avançada com heatmap usando dados reais ou simulados
    """
    dados_tabela = all_data["tb_sigt_valor_imovel_tributo"].copy()

    # Configurar colunas com formatação adequada
    columns = [
        {
            "name": "Ano",
            "id": "ano_exercicio",
            "type": "numeric",
            "format": {"specifier": "d"},
        },
        {
            "name": "Nº de Inscrições",
            "id": "num_inscricoes",
            "type": "numeric",
            "format": {"locale": {"decimal": ",", "group": "."}, "specifier": ",.0f"},
        },
        {
            "name": "Valor venal total (Milhões R$)",
            "id": "valor_venal_total_milhao",
            "type": "numeric",
            "format": {"locale": {"decimal": ",", "group": "."}, "specifier": ",.0f"},
        },
        {
            "name": "Incidência tributo (Milhões R$)",
            "id": "incidencia_tributo_milhao",
            "type": "numeric",
            "format": {"locale": {"decimal": ",", "group": "."}, "specifier": ",.0f"},
        },
        {
            "name": "Valor venal médio (R$)",
            "id": "valor_venal_medio",
            "type": "numeric",
            "format": {"locale": {"decimal": ",", "group": "."}, "specifier": ",.0f"},
        },
        {
            "name": "Incidência média do tributo (R$)",
            "id": "incidencia_tributo_medio",
            "type": "numeric",
            "format": {"locale": {"decimal": ",", "group": "."}, "specifier": ",.0f"},
        },
    ]

    tabela = dash_table.DataTable(
        id="tabela-valor-imovel-tributo-avancada",
        columns=columns,
        data=dados_tabela.to_dict("records"),
        # Estilos da tabela
        style_table={
            "overflowX": "auto",
            "border": "2px solid #dee2e6",
            "borderRadius": "10px",
            "boxShadow": "0 6px 12px rgba(0, 0, 0, 0.15)",
            "backgroundColor": "white",
            "margin": "20px 0",
        },
        # Estilos do cabeçalho
        style_header={
            "backgroundColor": "#0B3B7F",
            "color": "white",
            "fontWeight": "bold",
            "textAlign": "center",
            "padding": "15px 10px",
            "border": "none",
            "fontSize": "14px",
            "textTransform": "uppercase",
            "letterSpacing": "0.5px",
        },
        # Estilos das células
        style_cell={
            "textAlign": "center",
            "padding": "12px 10px",
            "fontSize": "13px",
            "fontFamily": 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            "border": "1px solid #dee2e6",
            "minWidth": "130px",
            "maxWidth": "220px",
            "whiteSpace": "normal",
            "height": "auto",
            "backgroundColor": "white",
        },
        # Estilos para linhas alternadas
        style_data={"border": "1px solid #dee2e6", "backgroundColor": "white"},
        # Configurações adicionais
        filter_action="none",
        sort_action="native",
        sort_mode="single",
        page_action="none",
        fixed_rows={"headers": True},
        # Tooltips informativos
        tooltip_delay=0,
        tooltip_duration=None,
        tooltip_header={
            "ano_exercicio": "Ano do exercício fiscal",
            "num_inscricoes": "Número total de inscrições cadastrais",
            "valor_venal_total_milhao": "Valor venal total em milhões de reais",
            "incidencia_tributo_milhao": "Incidência tributária total em milhões de reais",
            "valor_venal_medio": "Valor venal médio por inscrição",
            "incidencia_tributo_medio": "Incidência tributária média por inscrição",
        },
        # Interatividade
        editable=False,
        row_selectable=False,
        row_deletable=False,
        # CSS personalizado
        css=[
            {
                "selector": ".dash-table-tooltip",
                "rule": "background-color: white; font-family: system-ui; padding: 10px; border-radius: 6px; box-shadow: 0 4px 8px rgba(0,0,0,0.15); border: 1px solid #dee2e6;",
            }
        ],
    )

    return tabela


tabela_valor_imovel_avancada = criar_tabela_valor_imovel_tributo_avancada()

layout = html.Div(
    [
        html.Br(),
        coluna_receita_categ_tributo,
        html.Br(),
        html.H4("Receita anual por subcategoria tributária (2023-2025)"),
        create_info_popover(
            "info-receita-subcateg-tributo",
            "receita_subcateg_tributo",
        ),
        dropdown_categ_tributo,
        dcc.Graph(id="fig-subcateg-tributo"),
        html.H4("Inscrições imobiliárias, valor venal e incidência de tributo por ano"),
        create_info_popover(
            "info-valor-imovel-tributo",
            "receita_valor_imovel",
        ),
        html.Div(
            [tabela_valor_imovel_avancada],
        ),
        html.Br(),
    ]
)
