from dash import html, register_page, dcc, dash_table
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
import plotly.express as px
from babel.numbers import format_decimal, format_currency
from src.utils import create_info_popover
from src.load_data import load_data
from src.config import TEMPLATE

register_page(__name__, path="/desenvolvimento_humano/cad_unico", name="Cadastro Único")

all_data = load_data()

cod_familiar_fam = all_data["cod_familiar_fam"].copy()
cod_familiar_fam_2025 = all_data["cod_familiar_fam_2025"].copy()
renda_per_capita_fam = all_data["renda_per_capita_fam"].copy()
n_pessoas_fam = all_data["n_pessoas_fam"].copy()
escoa_sanitario_fam = all_data["escoa_sanitario_fam"].copy()
agua_canalizada_fam = all_data["agua_canalizada_fam"].copy()
qtd_comodos_domic_fam = all_data["qtd_comodos_domic_fam"].copy()
df_sabe_ler_escrever = all_data["sabe_ler_escrever_memb"].copy()
df_sexo_biologico = all_data["sexo_pessoa"].copy()
df_forma_coleta = all_data["forma_coleta"].copy()
df_parentesco = all_data["parentesco"].copy()


# CARTÕES
n_familias_cadastradas = format_decimal(
    cod_familiar_fam["cod_familiar_fam"].nunique(), format="#,##0", locale="pt_BR"
)
card_n_familias_cadastradas = html.Div(
    [
        html.Div(
            [
                html.H5(
                    "Famílias cadastradas",
                    className="card-title",
                    id="card_familias_cad",
                ),
                html.Div(
                    [html.Div(n_familias_cadastradas, className="card-value")],
                    className="card-value-container",
                ),
                html.P(
                    "Com cadastro ativo e atualizado",
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

n_familias_cadastradas_2025 = format_decimal(
    cod_familiar_fam_2025["cod_familiar_fam"].nunique(),
    format="#,##0",
    locale="pt_BR",
)
card_n_familias_cadastradas_2025 = html.Div(
    [
        html.Div(
            [
                html.H5(
                    "Novas famílias cadastradas",
                    className="card-title",
                    id="card_familias_cad_2025",
                ),
                html.Div(
                    [html.Div(n_familias_cadastradas_2025, className="card-value")],
                    className="card-value-container",
                ),
                html.P(
                    "Em 2025",
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

media_renda_per_capita = format_currency(
    renda_per_capita_fam["vlr_renda_per_capita_fam"].mean(), "BRL", locale="pt_BR"
)
card_media_renda_per_capita = html.Div(
    [
        html.Div(
            [
                html.H5(
                    "Renda per capita",
                    className="card-title",
                    id="card_renda_per_capita",
                ),
                html.Div(
                    [html.Div(media_renda_per_capita, className="card-value")],
                    className="card-value-container",
                ),
                html.P(
                    "Média mensal",
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

media_pessoas_familia = format_decimal(
    n_pessoas_fam["n_pessoas_fam"].mean(),
    format="#,##0.00",
    locale="pt_BR",
)
card_media_pessoas_familia = html.Div(
    [
        html.Div(
            [
                html.H5(
                    "Pessoas por família",
                    className="card-title",
                    id="card_pessoas_familia",
                ),
                html.Div(
                    [html.Div(media_pessoas_familia, className="card-value")],
                    className="card-value-container",
                ),
                html.P(
                    "Média",
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

media_pessoas_domic = format_decimal(
    n_pessoas_fam["qtd_pessoas_domic_fam"].mean(),
    format="#,##0.00",
    locale="pt_BR",
)
card_media_pessoas_domic = html.Div(
    [
        html.Div(
            [
                html.H5(
                    "Pessoas por domicílio",
                    className="card-title",
                    id="card_pessoas_domicilio",
                ),
                html.Div(
                    [html.Div(media_pessoas_domic, className="card-value")],
                    className="card-value-container",
                ),
                html.P(
                    "Média",
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

n_domicilios_sem_rede_esgoto = format_decimal(
    escoa_sanitario_fam.loc[
        escoa_sanitario_fam["desc_cod_escoa_sanitario_domic_fam"]
        == "Rede coletora de esgoto ou pluvial"
    ]["cod_familiar_fam"].nunique(),
    format="#,##0",
    locale="pt_BR",
)

pct_domicilios_sem_rede_esgoto = format_decimal(
    escoa_sanitario_fam.loc[
        escoa_sanitario_fam["desc_cod_escoa_sanitario_domic_fam"]
        != "Rede coletora de esgoto ou pluvial"
    ]["cod_familiar_fam"].nunique()
    / escoa_sanitario_fam["cod_familiar_fam"].nunique(),
    format="#,##0.00%",
    locale="pt_BR",
)

card_n_domicilios_sem_rede_esgoto = html.Div(
    [
        html.Div(
            [
                html.H5(
                    "Domicílios sem rede de esgoto",
                    className="card-title",
                ),
                html.Div(
                    [html.Div(n_domicilios_sem_rede_esgoto, className="card-value")],
                    className="card-value-container",
                ),
                html.P(
                    f"{pct_domicilios_sem_rede_esgoto} do total",
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


n_domicilios_sem_agua_canalizada = format_decimal(
    agua_canalizada_fam.loc[
        agua_canalizada_fam["desc_cod_agua_canalizada_fam"] == "Não"
    ]["cod_familiar_fam"].nunique(),
    format="#,##0",
    locale="pt_BR",
)
pct_domicilios_sem_agua_canalizada = format_decimal(
    agua_canalizada_fam.loc[
        agua_canalizada_fam["desc_cod_agua_canalizada_fam"] == "Não"
    ]["cod_familiar_fam"].nunique()
    / agua_canalizada_fam["cod_familiar_fam"].nunique(),
    format="#,##0.00%",
    locale="pt_BR",
)

card_n_domicilios_sem_agua_canalizada = html.Div(
    [
        html.Div(
            [
                html.H5(
                    "Domicílios sem água canalizada",
                    className="card-title",
                    id="card_agua_canalizada",
                ),
                html.Div(
                    [
                        html.Div(
                            n_domicilios_sem_agua_canalizada, className="card-value"
                        )
                    ],
                    className="card-value-container",
                ),
                html.P(
                    f"{pct_domicilios_sem_agua_canalizada} do total",
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

media_comodos_domic = format_decimal(
    qtd_comodos_domic_fam["qtd_comodos_domic_fam"].mean(),
    format="#,##0.00",
    locale="pt_BR",
)
card_media_comodos_domic = html.Div(
    [
        html.Div(
            [
                html.H5(
                    "Cômodos por domicílio",
                    className="card-title",
                    id="card_comodos_domicilio",
                ),
                html.Div(
                    [html.Div(media_comodos_domic, className="card-value")],
                    className="card-value-container",
                ),
                html.P(
                    "Média",
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


def gerar_grafico_renda_per_capita():
    # grafico renda per capita
    x = renda_per_capita_fam["vlr_renda_per_capita_fam"].dropna()

    # Calcular percentis e média
    p25 = np.percentile(x, 25)
    p50 = np.percentile(x, 50)
    p75 = np.percentile(x, 75)
    media = np.mean(x)

    # Criar ECDF
    fig_renda_per_capita = px.ecdf(x, x="vlr_renda_per_capita_fam")

    # Calcular probabilidades acumuladas para os valores de corte
    prob_extrema_pobreza = np.mean(x <= 218)
    prob_pobreza = np.mean(x <= 660)

    # Adicionar linhas verticais para os limites oficiais
    fig_renda_per_capita.add_vline(
        x=218,
        line_dash="dot",
        line_color="darkred",
        annotation_text=f" Extrema pobreza (< R$ 218): {prob_extrema_pobreza:.1%} das famílias".replace(
            ".", ","
        ),
        annotation_position="top right",
        annotation_font_color="darkred",
        annotation_font_size=12,
    )
    fig_renda_per_capita.add_vline(
        x=660,
        line_dash="dot",
        line_color="darkorange",
        annotation_text=f" Pobreza (< R$ 660): {prob_pobreza:.1%} das famílias".replace(
            ".", ","
        ),
        annotation_position="bottom right",
        annotation_font_color="darkorange",
        annotation_font_size=12,
    )

    # Melhorar visualização do eixo x
    fig_renda_per_capita.update_xaxes(range=[0, 5000], showgrid=False)

    # Layout
    fig_renda_per_capita.update_layout(
        xaxis_title="Renda per capita (R$)",
        yaxis_title="Probabilidade acumulada",
        template="plotly_white",
        separators=",.",
    )

    fig_renda_per_capita.update_traces(hoverinfo="none")
    return fig_renda_per_capita


fig_renda_per_capita = gerar_grafico_renda_per_capita()

# CONSOLIDAÇÃO DOS CARTÕES

cards_cadastro = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    card_n_familias_cadastradas,
                    width=3,
                ),
                dbc.Col(
                    card_n_familias_cadastradas_2025,
                    width=3,
                ),
                dbc.Col(
                    card_media_renda_per_capita,
                    width=3,
                ),
                dbc.Col(
                    card_media_pessoas_familia,
                    width=3,
                ),
            ],
            className="mb-4",
        ),
        html.Br(),
        dbc.Row(
            [
                html.H5("Distribuição acumulada da renda per capita familiar"),
                dcc.Graph(
                    figure=fig_renda_per_capita,
                    id="renda_per_capita",
                    config={
                        "displayModeBar": False,
                        "displaylogo": False,
                        "staticPlot": True,
                    },
                ),
            ]
        ),
    ]
)

cards_domicilio = dbc.Row(
    [
        dbc.Col(
            card_media_pessoas_domic,
            width=3,
        ),
        dbc.Col(
            card_media_comodos_domic,
            width=3,
        ),
        dbc.Col(
            card_n_domicilios_sem_agua_canalizada,
            width=3,
        ),
        dbc.Col(
            card_n_domicilios_sem_rede_esgoto,
            width=3,
        ),
    ],
    className="mb-4",
)


# GRÁFICOS
def gerar_grafico_sexo_biologico():
    sex_colors = {"Masculino": "#368CE7", "Feminino": "#073C73"}
    fig_sexo_biologico = px.pie(
        df_sexo_biologico,
        values="count",
        hole=0.5,
        names="desc_cod_sexo_pessoa",
        template=TEMPLATE,
        labels={
            "desc_cod_sexo_pessoa": "Sexo biológico",
            "count": "Número de pessoas",
        },
    )

    fig_sexo_biologico.update_traces(
        textposition="outside",
        textinfo="percent+label",
        marker=dict(
            colors=[
                sex_colors[name] for name in df_sexo_biologico["desc_cod_sexo_pessoa"]
            ]
        ),
    )
    fig_sexo_biologico.update_layout(
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        separators=",.",
    )
    return fig_sexo_biologico


fig_sexo_biologico = gerar_grafico_sexo_biologico()


# figura de cadastros por ano e forma de coleta
def gerar_grafico_forma_coleta():
    forma_coleta_colors = {
        "Com visita domiciliar": "#073c73",
        "Sem visita domiciliar": "#368ce7",
        "Não informado": "#7ab3ef",
    }

    fig_cadastro_forma_coleta = px.bar(
        df_forma_coleta,
        x="ano_cadastramento",
        y="n_familias",
        color="desc_cod_forma_coleta_fam",
        labels={
            "desc_cod_forma_coleta_fam": "Forma de coleta",
            "ano_cadastramento": "Ano de cadastro",
            "n_familias": "Número de famílias",
        },
        template=TEMPLATE,
        color_discrete_map=forma_coleta_colors,
    )

    fig_cadastro_forma_coleta.update_yaxes(
        showgrid=True,
        gridcolor="rgba(0,0,0,0.08)",
        zeroline=False,
        ticks="outside",
        tickformat=",",
        automargin=True,
    )
    fig_cadastro_forma_coleta.update_xaxes(
        zeroline=False, ticks="outside", tickmode="linear", dtick="M1", tickangle=45
    )
    fig_cadastro_forma_coleta.update_traces(
        cliponaxis=False,
        marker_line_color="black",
        marker_line_width=1,
        hovertemplate="<b>%{fullData.name}</b><br>Ano: %{x}<br>Famílias: %{y:,.0f}<extra></extra>",
    )

    fig_cadastro_forma_coleta.update_layout(
        margin=dict(l=40, r=40, t=30, b=80),
        yaxis=dict(tickformat=",.0f", gridcolor="lightgray", zeroline=False),
        xaxis=dict(tickmode="linear", tickangle=45),
        bargap=0.25,
        plot_bgcolor="white",
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="white",
            bordercolor="lightgray",
        ),
        separators=",.",
    )

    # Adicionar tooltip personalizado que mostra todas as categorias
    anos_unicos = df_forma_coleta["ano_cadastramento"].unique()

    # Criar um dicionário com os tooltips por ano
    tooltips_por_ano = {}

    for ano in anos_unicos:
        dados_ano = df_forma_coleta[df_forma_coleta["ano_cadastramento"] == ano]
        total_ano = dados_ano["n_familias"].sum()

        # Criar texto do tooltip com todas as categorias
        tooltip_text = f"<b>Ano: {ano}</b><br><br>"
        tooltip_text += "<b>Famílias por Forma de Coleta:</b><br>"

        for _, row in dados_ano.iterrows():
            categoria = row["desc_cod_forma_coleta_fam"]
            valor = row["n_familias"]
            percentual = (valor / total_ano) * 100

            # Formatar o valor para milhares quando apropriado
            if valor >= 1_000_000:
                valor_formatado = f"{valor/1_000_000:.1f}M"
            elif valor >= 1_000:
                valor_formatado = f"{valor/1_000:.1f}K"
            else:
                valor_formatado = f"{valor:,.0f}"

            tooltip_text += (
                f"<b>{categoria}:</b> {valor_formatado} ({percentual:.1f}%)<br>"
            )

        # Formatar o total também
        if total_ano >= 1_000_000:
            total_formatado = f"{total_ano/1_000_000:.1f}M"
        elif total_ano >= 1_000:
            total_formatado = f"{total_ano/1_000:.1f}K"
        else:
            total_formatado = f"{total_ano:,.0f}"

        tooltip_text += f"<br><b>Total: {total_formatado} famílias</b>"
        tooltips_por_ano[ano] = tooltip_text

    # Aplicar o tooltip personalizado para cada trace
    for trace in fig_cadastro_forma_coleta.data:
        # Criar uma lista de tooltips para este trace
        tooltips_trace = []

        for i, x_val in enumerate(trace.x):
            if x_val in tooltips_por_ano:
                tooltips_trace.append(tooltips_por_ano[x_val] + "<extra></extra>")
            else:
                # Fallback para tooltip padrão se não encontrar o ano
                valor = trace.y[i]
                if valor >= 1_000_000:
                    valor_formatado = f"{valor/1_000_000:.1f}M"
                elif valor >= 1_000:
                    valor_formatado = f"{valor/1_000:.1f}K"
                else:
                    valor_formatado = f"{valor:,.0f}"
                tooltips_trace.append(
                    f"<b>{trace.name}</b><br>Ano: {x_val}<br>Famílias: {valor_formatado}<extra></extra>"
                )

        # Atualizar o hovertemplate do trace
        trace.hovertemplate = tooltips_trace

    return fig_cadastro_forma_coleta


fig_cadastro_forma_coleta = gerar_grafico_forma_coleta()

row_graficos_cadastro_sexo = dbc.Row(
    [
        dbc.Col(
            [
                html.H4(
                    "Evolução de cadastros no CadÚnico por ano e forma de coleta",
                ),
                create_info_popover(
                    "info-cadastramento-cadunico",
                    "humano_cad_unico_cadastros",
                ),
                dcc.Graph(
                    figure=fig_cadastro_forma_coleta,
                    id="evolucao_cadastros",
                    config={"displayModeBar": False, "responsive": True},
                    style={"width": "100%", "height": "420px"},
                ),
            ],
            width=8,
        ),
        dbc.Col(
            [
                html.H4(
                    "Pessoas cadastradas no CadÚnico por sexo biológico",
                ),
                create_info_popover(
                    "info-cadastramento-cadunico-sexo",
                    "humano_cad_unico_sexo",
                ),
                dcc.Graph(
                    figure=fig_sexo_biologico,
                    id="sexo_biologico",
                    config={"displayModeBar": False, "responsive": True},
                    style={"width": "100%", "height": "420px"},
                ),
            ],
            width=4,
        ),
    ],
    className="g-3 align-items-start",
)


def gerar_grafico_parentesco():
    fig_parentesco = px.bar(
        df_parentesco,
        x="count",
        y="desc_cod_parentesco_rf_pessoa",
        orientation="h",
        template=TEMPLATE,
        color_discrete_sequence=["#75BAFF"],
        labels={
            "desc_cod_parentesco_rf_pessoa": "Parentesco",
            "count": "Número de pessoas",
        },
    )

    fig_parentesco.update_yaxes(
        showgrid=True,
        gridcolor="rgba(0,0,0,0.08)",
        zeroline=False,
        ticks="outside",
        tickformat=",",
        automargin=True,
    )

    fig_parentesco.update_xaxes(
        zeroline=False,
        tickformat=",",
    )
    fig_parentesco.update_traces(
        text=df_parentesco["count"],
        texttemplate="%{x:,.0f}",
        textposition="outside",
        cliponaxis=False,
        marker_line_color="black",
        marker_line_width=1,
        hovertemplate="<b>%{y}</b><br>Total: %{x:,.0f}<extra></extra>",
    )
    fig_parentesco.update_layout(
        bargap=0.25,
        showlegend=False,
        margin=dict(l=40, r=40, t=30, b=80),
        plot_bgcolor="white",
        separators=",.",
    )

    return fig_parentesco


fig_parentesco = gerar_grafico_parentesco()


indicadores_bairros = all_data["indicadores_bairros"].copy()
column_names = {
    "bairro": "Bairro",
    "cod_familiar_fam": "Nº de Famílias",
    "vlr_renda_per_capita_fam": "Média de Renda per Capita",
    "qtd_pessoas_domic_fam": "Média de Pessoas por Domicílio",
    "qtd_comodos_domic_fam": "Média de Cômodos por Domicílio",
    "qtd_familias_domic_fam": "Média de Famílias por Domicílio",
    "val_desp_energia_fam": "Média de Despesa de Energia",
    "val_desp_agua_esgoto_fam": "Média de Despesa de Água/Esgoto",
    "val_desp_alimentacao_fam": "Média de Despesa de Alimentação",
}
indicadores_bairros = indicadores_bairros.rename(columns=column_names)


table = dash_table.DataTable(
    id="interactive-table",
    columns=[
        {
            "name": col,
            "id": col,
            "type": "numeric" if col != "Bairro" else "text",
            "filter_options": {
                "case": "insensitive",
                "placeholder_text": "Filtrar dados...",
                "logic": "contains",
            },
            "format": (
                {
                    "locale": {"decimal": ",", "group": "."},
                    "specifier": (
                        ",.2f" if "Despesa" in col or "Renda" in col else ",.1f"
                    ),
                }
                if col != "Bairro"
                else None
            ),
        }
        for col in indicadores_bairros.columns
    ],
    data=indicadores_bairros.to_dict("records"),
    filter_action="native",
    sort_action="native",
    sort_mode="multi",
    fixed_rows={"headers": True},
    style_table={
        "overflowX": "auto",
        "overflowY": "auto",
        "maxHeight": "500px",
        "border": "thin lightgrey solid",
        "borderRadius": "8px",
        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
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
    style_data_conditional=[
        {
            "if": {"row_index": "odd"},
            "backgroundColor": "#fcfcfc",
        },
        {
            "if": {"state": "selected"},
            "backgroundColor": "#e6f3ff",
            "border": "1px solid #0d6efd",
        },
        {
            "if": {"state": "active"},
            "backgroundColor": "#e6f3ff",
            "border": "1px solid #0d6efd",
        },
    ],
    style_filter={
        "backgroundColor": "#f8f9fa",
        "padding": "8px 15px",
    },
    tooltip_delay=0,
    tooltip_duration=None,
    editable=False,
    row_selectable=False,
    row_deletable=False,
    css=[
        {
            "selector": ".dash-table-tooltip",
            "rule": "background-color: white; font-family: system-ui; padding: 8px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);",
        }
    ],
)
table_container = html.Div([table], className="p-4 bg-white rounded shadow-sm")

# DEFINIÇÃO DO VISUAL DA PÁGINA
layout = html.Div(
    [
        html.Br(),
        html.H3("Cadastro Único para Programas Sociais"),
        create_info_popover(
            "info-cadastro-unico",
            "humano_apresentacao_cad_unico",
        ),
        html.Br(),
        # LINHA CARDS COM INFORMAÇÕES GERAIS
        html.Div(
            [
                html.H4("Famílias"),
                html.Br(),
                cards_cadastro,
            ],
            className="section-container",
            style={"marginBottom": "3rem"},
        ),
        # INFORMAÇÕES GERAIS - DOMICILIOS
        html.Div(
            [
                html.H4("Domicílios"),
                html.Br(),
                cards_domicilio,
            ],
            className="section-container",
            style={"marginBottom": "3rem"},
        ),
        # GRÁFICO DE ALFABETIZADOS E DISTRIBUIÇÃO POR SEXO DOS CADASTROS
        html.Div(
            [row_graficos_cadastro_sexo],
            className="section-container",
            style={"marginBottom": "3rem"},
        ),
        # GRÁFICO DE PARENTESCO DAS PESSOAS CADASTRADAS
        html.Div(
            [
                html.H4(
                    "Pessoas cadastradas no CadÚnico por parentesco",
                ),
                create_info_popover(
                    "info-cadastro-unico-parentesco",
                    "humano_cad_unico_parentesco",
                ),
                dcc.Graph(figure=fig_parentesco, id="graf_parentesco"),
            ],
            className="section-container",
            style={"marginBottom": "3rem"},
        ),
        # TABELA COM VISÃO GERAL DOS BAIRROS DE OSASCO
        html.Div(
            [
                html.H4(
                    "Visão geral dos bairros de Osasco no CadÚnico", id="tabela_bairros"
                ),
                create_info_popover(
                    "info-cadastro-unico-bairros",
                    "humano_cad_unico_bairros",
                ),
                table_container,
            ],
            className="section-container",
            style={"marginBottom": "3rem"},
        ),
    ]
)
