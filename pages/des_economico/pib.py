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
    __name__, path="/desenvolvimento_economico/pib", name="PIB"
)

################################ DESENVOLVIMENTO ECONÔMICO #################################
# CARREGAR DADOS
all_data = load_data()

mapa_cores = {
    "Osasco (SP)": "#1F77B4",
    "São José dos Campos (SP)": "#AF8DCD",
    "Sorocaba (SP)": "#FF9F4A",
    "São Bernardo do Campo (SP)": "#E05D5E",
    "Ribeirão Preto (SP)": "#61B861",
    "Santo André (SP)": "#A98078",
}

# GRÁFICOS PIB
def get_pib_plots(all_data):

    # GRÁFICO PIB POR CATEGORIA
    df_pib_categorias = (
        all_data["pib_por_categoria"]
        .loc[all_data["pib_por_categoria"]["variavel_dash"] != "Total"]
        .copy()
    )
    fig_pib_categorias = px.bar(
        df_pib_categorias,
        x="ano",
        y="pib_deflacionado",
        color="variavel_dash",
        color_discrete_sequence=[
            "#1666ba",
            "#368ce7",
            "#7ab3ef",
            "#bedaf7",
            "#deecfb",
        ],
        labels={
            "ano": "Ano",
            "pib_deflacionado": "PIB (deflacionado)",
            "variavel_dash": "Categoria",
        },
        template=TEMPLATE,
    )
    # fig_pib_categorias.update_xaxes(tickmode="linear", tickangle=45)
    fig_pib_categorias.update_layout(
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="white",
            bordercolor="lightgray",
        ),
    )

    fig_pib_categorias.update_yaxes(
        showgrid=True,
        gridcolor="rgba(0,0,0,0.08)",
        zeroline=False,
        ticks="outside", 
        automargin=True
    )
    fig_pib_categorias.update_xaxes(
        zeroline=False,
        ticks="outside", 
        tickmode="linear", 
        tickangle=45
    )
    fig_pib_categorias.update_traces(
        cliponaxis=False,
        marker_line_color="black",
        marker_line_width=1,
        hovertemplate="<b>%{fullData.name}</b><br>Ano: %{x}<br>PIB: R$ %{y:,.2f}<extra></extra>",
    )
    fig_pib_categorias.update_layout(
        bargap=0.25,
        showlegend=True,
        margin=dict(l=40, r=40, t=30, b=80),
        plot_bgcolor="white",
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="white",
            bordercolor="lightgray",
        ),
    )
    
    # Adicionar tooltip personalizado que mostra todas as categorias
    anos_unicos = df_pib_categorias['ano'].unique()
    
    # Criar um dicionário com os tooltips por ano
    tooltips_por_ano = {}
    
    for ano in anos_unicos:
        dados_ano = df_pib_categorias[df_pib_categorias['ano'] == ano]
        total_ano = dados_ano['pib_deflacionado'].sum()
        
        # Criar texto do tooltip com todas as categorias
        tooltip_text = f"<b>Ano: {ano}</b><br><br>"
        tooltip_text += "<b>PIB por Categoria:</b><br>"
        
        for _, row in dados_ano.iterrows():
            categoria = row['variavel_dash']
            valor = row['pib_deflacionado']
            percentual = (valor / total_ano) * 100
            
            # Formatar o valor para milhões de reais
            if valor >= 1_000_000:
                valor_formatado = f"R$ {valor/1_000_000:.1f}M"
            elif valor >= 1_000:
                valor_formatado = f"R$ {valor/1_000:.1f}K"
            else:
                valor_formatado = f"R$ {valor:,.0f}"
            
            tooltip_text += f"<b>{categoria}:</b> {valor_formatado} ({percentual:.1f}%)<br>"
        
        # Formatar o total também
        if total_ano >= 1_000_000:
            total_formatado = f"R$ {total_ano/1_000_000:.1f}M"
        elif total_ano >= 1_000:
            total_formatado = f"R$ {total_ano/1_000:.1f}K"
        else:
            total_formatado = f"R$ {total_ano:,.0f}"
        
        tooltip_text += f"<br><b>Total: {total_formatado}</b>"
        tooltips_por_ano[ano] = tooltip_text
    
    # Aplicar o tooltip personalizado para cada trace
    for trace in fig_pib_categorias.data:
        # Criar uma lista de tooltips para este trace
        tooltips_trace = []
        
        for i, x_val in enumerate(trace.x):
            if x_val in tooltips_por_ano:
                tooltips_trace.append(tooltips_por_ano[x_val] + "<extra></extra>")
            else:
                # Fallback para tooltip padrão se não encontrar o ano
                valor = trace.y[i]
                if valor >= 1_000_000:
                    valor_formatado = f"R$ {valor/1_000_000:.1f}M"
                elif valor >= 1_000:
                    valor_formatado = f"R$ {valor/1_000:.1f}K"
                else:
                    valor_formatado = f"R$ {valor:,.0f}"
                tooltips_trace.append(f"<b>{trace.name}</b><br>Ano: {x_val}<br>PIB: {valor_formatado}<extra></extra>")
        
        # Atualizar o hovertemplate do trace
        trace.hovertemplate = tooltips_trace

    # GRÁFICO PIB PER CAPITA
    fig_pib_per_capita = px.line(
        all_data["pib_per_capita"],
        x="ano",
        y="pib_per_capita",
        color="municipio",
        line_shape="spline",
        labels={
            "ano": "Ano",
            "pib_per_capita": "PIB per capita (R$)",
            "municipio": "Município",
        },
        template="none",
        color_discrete_map=mapa_cores,
    )

    fig_pib_per_capita.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis=dict(tickformat=",.0f", gridcolor="lightgray", zeroline=False),
        xaxis=dict(gridcolor="white", zeroline=False),
        legend_title_text="Município",
        legend=dict(
            orientation="h", yanchor="bottom", y=-0.35, xanchor="center", x=0.5
        ),
        hovermode="x unified"
    )

    fig_pib_per_capita.for_each_trace(
        lambda trace: trace.update(
            line=dict(
                width=2.5 if trace.name == "Osasco (SP)" else 1.5,
                dash="solid" if trace.name == "Osasco (SP)" else "dash",
            ),
            marker=dict(size=8 if trace.name == "Osasco (SP)" else 6),
            opacity=1 if trace.name == "Osasco (SP)" else 0.75,
        )
    )
    fig_pib_per_capita.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>Ano: %{x}<br>PIB per capita: R$ %{y:,.2f}<extra></extra>"
    )
    fig_pib_per_capita.update_xaxes(tickmode="linear", tickangle=45)

    # GRÁFICO PARTICIPAÇÃO DO PIB MUNICIPAL NO PIB DE SÃO PAULO
    fig_pib_sp = px.line(
        all_data["pib_participacao_sp"],
        x="ano",
        y="participacao_pib_sp",
        color="municipio",
        line_shape="spline",
        labels={
            "ano": "Ano",
            "participacao_pib_sp": "Participação % PIB de SP",
            "municipio": "Município",
        },
        template="none",
        color_discrete_map=mapa_cores,
    )
    fig_pib_sp.for_each_trace(
        lambda trace: trace.update(
            line=dict(
                width=2 if trace.name == "Osasco (SP)" else 1.5,
                dash="solid" if trace.name == "Osasco (SP)" else "dot",
            ),
            opacity=1 if trace.name == "Osasco (SP)" else 0.7,
        )
    )
    fig_pib_sp.update_xaxes(tickmode="linear", tickangle=45)

    fig_pib_sp.update_layout(
        yaxis_tickformat=".%",
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis=dict(
            tickformat=",.1%", gridcolor="lightgray", zeroline=False, title_standoff=30
        ),
        xaxis=dict(gridcolor="white", zeroline=False),
        legend_title_text="Município",
        legend=dict(
            orientation="h", yanchor="bottom", y=-0.35, xanchor="center", x=0.5
        ),
        hovermode="x unified"
    )
    fig_pib_sp.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>Ano: %{x}<br>Participação: %{y:,.2%}<extra></extra>"
    )

    # ATRIBUIR MARGEM E ANOTAÇÃO DE FONTE A TODOS OS GRÁFICOS
    for fig in [fig_pib_sp, fig_pib_per_capita, fig_pib_categorias]:
        fig.update_layout(
            margin=dict(t=0),
        )
        fig.add_annotation(
            text="Fonte: <a href='https://www.ibge.gov.br/estatisticas/economicas/contas-nacionais/9088-produto-interno-bruto-dos-municipios.html'>IBGE</a>",
            xref="paper",
            yref="paper",
            x=0.0,
            y=-0.2,
            showarrow=False,
            font=dict(size=12),
            xanchor="center",
            clicktoshow=False,
        )
    return fig_pib_sp, fig_pib_per_capita, fig_pib_categorias


fig_pib_sp, fig_pib_per_capita, fig_pib_categorias = get_pib_plots(all_data)

# VALORES PIB PARA CARD LATERAL
pib_corrente = calcular_pib_atual(all_data["pib_por_categoria"])
variacao_pib = calcular_variacao_pib(all_data["pib_por_categoria"])

card_pib_corrente = html.Div(
    [
        html.Div(
            [
                html.H5(
                    "PIB",
                    className="card-title",
                ),
                html.Div(
                    [html.Div(pib_corrente, className="card-value")],
                    className="card-value-container",
                ),
                html.P(
                    f"{all_data['pib_por_categoria']['ano'].max()}",
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

arrow_symbol = "▲" if float(variacao_pib.strip("%").replace(",", ".")) >= 0 else "▼"
arrow_style = {
    "color": (
        "#28a745"
        if float(variacao_pib.strip("%").replace(",", ".")) >= 0
        else "#dc3545"
    ),
    "fontSize": "24px",
    "marginLeft": "8px",
}

card_variacao_pib = html.Div(
    [
        html.Div(
            [
                html.H5("Variação", className="card-title"),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(variacao_pib, className="card-value"),
                                html.Span(arrow_symbol, style=arrow_style),
                            ],
                            style={
                                "display": "flex",
                                "alignItems": "center",
                                "justifyContent": "center",
                            },
                        )
                    ],
                    className="card-value-container",
                ),
                html.P(
                    "2020 - 2021",
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


coluna_cartao_pib_categorias = dbc.Col(
    [
        card_pib_corrente,
        html.Div(style={"height": "20px"}),  # Spacer between cards
        card_variacao_pib,
    ],
    width=2,
    className="cards-container",
)

cartoes_pib_categorias = dbc.Row(
    [
        coluna_cartao_pib_categorias,
        dbc.Col(
            dcc.Graph(
                id="pib-graph",
                figure=fig_pib_categorias,
                config={"displayModeBar": False},
                style={"height": "500px"}
            ),
            width=10,
        ),
    ],
    className="main-content-row",
)

# VALORES PIB PER CAPITA PARA CARD LATERAL
vl_pib_per_capita = (
    all_data["pib_per_capita"]
    .loc[all_data["pib_per_capita"]["ano"] == all_data["pib_per_capita"]["ano"].max()][
        "pib_per_capita"
    ]
    .values[0]
)

vl_pib_per_capita = format_currency(
    vl_pib_per_capita, "BRL", locale="pt_BR", currency_digits=False, format="¤ #,##0"
)

card_pib_per_capita = html.Div(
    [
        html.Div(
            [
                html.H5(
                    "PIB per capita",
                    className="card-title",
                ),
                html.Div(
                    [html.Div(vl_pib_per_capita, className="card-value")],
                    className="card-value-container",
                ),
                html.P(
                    f"{all_data['pib_per_capita']['ano'].max()}",
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

# VALORES POPULAÇÃO PARA CARD LATERAL
vl_populacao = (
    all_data["pib_per_capita"]
    .loc[all_data["pib_per_capita"]["ano"] == all_data["pib_per_capita"]["ano"].max()][
        "populacao"
    ]
    .values[0]
)

vl_populacao = format_decimal(vl_populacao, format="#,##0", locale="pt_BR")

card_populacao = html.Div(
    [
        html.Div(
            [
                html.H5(
                    "População",
                    className="card-title",
                ),
                html.Div(
                    [html.Div(vl_populacao, className="card-value")],
                    className="card-value-container",
                ),
                html.P(
                    f"{all_data['pib_per_capita']['ano'].max()}",
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

coluna_cartao_pib_per_capita = dbc.Col(
    [
        card_pib_per_capita,
        html.Div(style={"height": "20px"}),
        card_populacao,
    ],
    width=2,
    className="cards-container",
)

cartoes_pib_per_capita = dbc.Row(
    [
        coluna_cartao_pib_per_capita,
        dbc.Col(
            dcc.Graph(
                figure=fig_pib_per_capita,
                config={"displayModeBar": False},
                id="pib-per-capita-graph",
            ),
            width=10,
        ),
    ],
    className="main-content-row",
)

# CARTÕES PARTICIPAÇÃO NO PIB SP

vl_participacao = (
    all_data["pib_participacao_sp"]
    .loc[
        all_data["pib_participacao_sp"]["ano"]
        == all_data["pib_participacao_sp"]["ano"].max()
    ]["participacao_pib_sp"]
    .values[0]
)
vl_participacao = format_percent(vl_participacao, locale="pt_BR", format="#.00%")

card_participacao = html.Div(
    [
        html.Div(
            [
                html.H5(
                    "PIB de Osasco / PIB SP",
                    className="card-title",
                ),
                html.Div(
                    [html.Div(vl_participacao, className="card-value")],
                    className="card-value-container",
                ),
                html.P(
                    f"{all_data['pib_participacao_sp']['ano'].max()}",
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
coluna_card_participacao = dbc.Col(
    [card_participacao, html.Div(style={"height": "20px"})],
    width=2,
    className="cards-container",
)

cartoes_participacao = dbc.Row(
    [
        coluna_card_participacao,
        dbc.Col(
            dcc.Graph(
                id="fig-pib-sp",
                figure=fig_pib_sp,
                config={"displayModeBar": False},
            ),
            width=10,
        ),
    ],
    className="main-content-row",
)

# LAYOUT DA PÁGINA
layout = html.Div(
    [
        # PIB CATEGORIAS
        html.Br(),
        html.Div(
            [
                html.H4("PIB (em R$ de 2021)"),
                create_info_popover(
                    "info-pib",
                    "economico_pib_categorias",
                ),
                cartoes_pib_categorias,
            ],
            className="section-container",
            style={"marginBottom": "3rem"},
        ),
        # PIB PER CAPITA
        html.Div(
            [
                html.H4("PIB per capita (em R$ de 2021)"),
                create_info_popover(
                    "info-pib-per-capita",
                    "economico_pib_per_capita",
                ),
                cartoes_pib_per_capita,
            ],
            className="section-container",
            style={"marginBottom": "3rem"},
        ),
        # PARTICIPAÇÃO DO PIB MUNICIPAL NO PIB DE SÃO PAULO
        html.Div(
            [
                html.H4("Participação do PIB municipal no Estado de São Paulo"),
                create_info_popover(
                    "info-pib-sp",
                    "economico_pib_participacao_sp",
                ),
                cartoes_participacao,
            ],
            className="section-container",
            style={"marginBottom": "3rem"},
        ),
    ]
)
