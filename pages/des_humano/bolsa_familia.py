from dash import html, register_page, dcc, dash_table
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
import plotly.express as px
from babel.numbers import format_decimal, format_currency
from src.utils import create_info_popover
from src.load_data import load_data
from src.config import TEMPLATE

register_page(__name__, path="/desenvolvimento_humano/bolsa_familia", name="Bolsa Família")

all_data = load_data()

# Programa Bolsa Família
pbf = all_data["pbf_munic_selecionados"].copy()


def get_pbf_plots(pbf):

    # GRÁFICO NÚMERO DE FAVORECIDOS
    fig_n_favorecidos = px.line(
        pbf,
        x="mes_referencia",
        y="n_favorecidos",
        color="nome_municipio",
        line_shape="spline",
        labels={
            "mes_referencia": "Mês",
            "n_favorecidos": "Contagem de famílias beneficiadas",
            "nome_municipio": "Município",
        },
        template="none",
    )
    fig_n_favorecidos.for_each_trace(
        lambda trace: trace.update(
            line=dict(
                width=2 if trace.name == "Osasco (SP)" else 1.5,
                dash="solid" if trace.name == "Osasco (SP)" else "dot",
            ),
            opacity=1 if trace.name == "Osasco (SP)" else 0.7,
        )
    )
    fig_n_favorecidos.update_xaxes(tickformat="%m/%Y")
    fig_n_favorecidos.update_yaxes(tickformat=",")
    fig_n_favorecidos.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis=dict(gridcolor="lightgray", zeroline=False, title_standoff=30),
        xaxis=dict(gridcolor="white", zeroline=False, title_standoff=30),
        legend_title_text="Município",
        legend=dict(orientation="h", yanchor="bottom", y=-0.6, xanchor="center", x=0.5),
        margin=dict(b=120),
        separators=",.",
        hovermode="x unified"
    )
    fig_n_favorecidos.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>Mês/Ano: %{x}<br>Número de favorecidos PBF: %{y:,.0f}<extra></extra>"
    )

    # GRÁFICO TOTAL DE REPASSES
    fig_total_repasses = px.line(
        pbf,
        x="mes_referencia",
        y="total_repasses",
        color="nome_municipio",
        line_shape="spline",
        labels={
            "mes_referencia": "Mês",
            "total_repasses": "Valor total de repasses PBF em reais",
            "nome_municipio": "Município",
        },
        template="none",
    )
    fig_total_repasses.for_each_trace(
        lambda trace: trace.update(
            line=dict(
                width=2 if trace.name == "Osasco (SP)" else 1.5,
                dash="solid" if trace.name == "Osasco (SP)" else "dot",
            ),
            opacity=1 if trace.name == "Osasco (SP)" else 0.7,
        )
    )
    fig_total_repasses.update_xaxes(tickformat="%m/%Y")
    fig_total_repasses.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis=dict(gridcolor="lightgray", zeroline=False, title_standoff=30),
        xaxis=dict(gridcolor="white", zeroline=False, title_standoff=30),
        legend_title_text="Município",
        legend=dict(orientation="h", yanchor="bottom", y=-0.6, xanchor="center", x=0.5),
        margin=dict(b=120),
        hovermode="x unified"
    )
    fig_total_repasses.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>Mês/Ano: %{x}<br>Valor total de repasses PBF: %{y:,.0f}<extra></extra>"
    )

    # GRÁFICO MÉDIA DE REPASSES
    fig_media_repasses = px.line(
        pbf,
        x="mes_referencia",
        y="media_repasses",
        color="nome_municipio",
        line_shape="spline",
        labels={
            "mes_referencia": "Mês",
            "media_repasses": "Média do valor dos repasses PBF em reais",
            "nome_municipio": "Município",
        },
        template="none",
    )
    fig_media_repasses.for_each_trace(
        lambda trace: trace.update(
            line=dict(
                width=2 if trace.name == "Osasco (SP)" else 1.5,
                dash="solid" if trace.name == "Osasco (SP)" else "dot",
            ),
            opacity=1 if trace.name == "Osasco (SP)" else 0.7,
        )
    )
    fig_media_repasses.update_xaxes(tickformat="%m/%Y")
    fig_media_repasses.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis=dict(gridcolor="lightgray", zeroline=False, title_standoff=30),
        xaxis=dict(gridcolor="white", zeroline=False, title_standoff=30),
        legend_title_text="Município",
        legend=dict(orientation="h", yanchor="bottom", y=-0.6, xanchor="center", x=0.5),
        margin=dict(b=120),
        hovermode="x unified"
    )
    fig_media_repasses.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>Mês/Ano: %{x}<br>Média do valor dos repasses PBF: %{y:,.0f}<extra></extra>"
    )

    for fig in [fig_n_favorecidos, fig_total_repasses, fig_media_repasses]:

        fig.add_annotation(
            text="Fonte: <a href='https://portaldatransparencia.gov.br/download-de-dados/novo-bolsa-familia'>Portal da Transparência: CGU</a>",
            xref="paper",
            yref="paper",
            x=0.0,
            y=-0.35,
            showarrow=False,
            font=dict(size=12),
            # xanchor="center",
            clicktoshow=False,
        )

    return fig_n_favorecidos, fig_total_repasses, fig_media_repasses


fig_n_favorecidos, fig_total_repasses, fig_media_repasses = get_pbf_plots(pbf)

# DEFINIÇÃO DO VISUAL DA PÁGINA
layout = html.Div(
    [
        html.Br(),
        html.Div(
            [
                html.H3("Programa Bolsa Família (PBF)"),
                html.Br(),
                html.Div(
                    [
                        html.H4(
                            "Número de famílias beneficiadas pelo PBF",
                        ),
                        create_info_popover(
                            "info-pbf-familias",
                            "humano_favorecidos_pbf",
                        ),
                        dcc.Graph(
                            figure=fig_n_favorecidos, id="graf_familias_bolsa_familia"
                        ),
                    ],
                    className="section-container",
                    style={"marginBottom": "3rem"},
                ),
                html.Div(
                    [
                        html.H4(
                            "Valor total dos repasses do PBF",
                        ),
                        create_info_popover(
                            "info-pbf-repasses",
                            "humano_repasses_pbf",
                        ),
                        dcc.Graph(
                            figure=fig_total_repasses, id="graf_repasses_bolsa_familia"
                        ),
                    ],
                    className="section-container",
                    style={"marginBottom": "3rem"},
                ),
                html.Div(
                    [
                        html.H4(
                            "Média do valor dos repasses do PBF",
                        ),
                        create_info_popover(
                            "info-pbf-media-repasses",
                            "humano_media_repasses_pbf",
                        ),
                        dcc.Graph(figure=fig_media_repasses, id="graf_valor_repasses"),
                    ],
                    className="section-container",
                    style={"marginBottom": "3rem"},
                ),
            ]
        ),
    ]
)