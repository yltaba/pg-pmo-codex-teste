from dash import dcc, html, register_page, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import re
import unicodedata
import ipeadatapy

from src.utils import (
    create_info_popover,
    get_options_dropdown,
)
from src.config import TEMPLATE
from src.load_data import load_data


register_page(__name__, path="/demografia", name="Demografia")


all_data = load_data()
populacao_densidade = all_data["populacao_densidade"].copy()


# CARREGAR DADOS
def to_snake_case(column_name):
    """
    Converte um nome de coluna para snake_case, removendo acentos e ç.

    Args:
        column_name (str): Nome da coluna original

    Returns:
        str: Nome da coluna em snake_case sem acentos
    """
    # Remove parênteses e seu conteúdo
    column_name = re.sub(r"\s*\([^)]*\)", "", column_name)

    # Remove acentos e normaliza caracteres
    column_name = unicodedata.normalize("NFD", column_name)
    column_name = "".join(c for c in column_name if not unicodedata.combining(c))

    # Converte para minúsculas
    column_name = column_name.lower()

    # Substitui ç por c
    column_name = column_name.replace("ç", "c")

    # Substitui espaços e caracteres especiais por underscore
    column_name = re.sub(r"[^\w\s]", " ", column_name)
    column_name = re.sub(r"\s+", "_", column_name)

    # Remove underscores duplicados e no início/fim
    column_name = re.sub(r"_+", "_", column_name)
    column_name = column_name.strip("_")

    return column_name


def transform_columns_to_snake_case(df):
    """
    Transforma todas as colunas de um DataFrame para snake_case.

    Args:
        df (pandas.DataFrame): DataFrame com as colunas a serem transformadas

    Returns:
        pandas.DataFrame: DataFrame com colunas em snake_case
    """
    # Cria um mapeamento das colunas originais para snake_case
    column_mapping = {col: to_snake_case(col) for col in df.columns}

    # Renomeia as colunas
    df_renamed = df.rename(columns=column_mapping)

    return df_renamed


def extrair_pop_censo_api():
    url_pop_censo = (
        "https://apisidra.ibge.gov.br/values"
        "/t/9514"
        "/p/2022"
        "/v/93"
        "/n6/3534401"
        "/c2/4,5"
        "/c287/93070,93084,93085,93086,93087,93088,93089,93090,93091,93092,93093,93094,93095,93096,93097,93098,49108,49109,60040,60041,6653"
    )
    pop_osasco_censo22 = pd.read_json(url_pop_censo)

    # tratamentos
    pop_osasco_censo22.columns = pop_osasco_censo22.iloc[0]
    pop_osasco_censo22 = pop_osasco_censo22.drop(pop_osasco_censo22.index[0])

    pop_osasco_censo22["Valor"] = pop_osasco_censo22["Valor"].astype(int)

    colunas_a_remover = pop_osasco_censo22.filter(like="(Código)").columns
    pop_osasco_censo22 = pop_osasco_censo22.drop(columns=colunas_a_remover)

    pop_osasco_censo22 = transform_columns_to_snake_case(pop_osasco_censo22)

    return pop_osasco_censo22


def extrair_pop_urbana_rural_censo_api():
    def extrair_serie_pop_urbana_rural(serie):
        pop = ipeadatapy.timeseries(serie).reset_index(drop=True)
        pop.columns = (
            pop.columns.str.lower()
            .str.replace("(", "")
            .str.replace(")", "")
            .str.replace(" ", "_")
        )
        pop = pop[["tercodigo", "year", "value_habitante"]]
        pop["categoria"] = "pop_urbana" if serie == "POPUR" else "pop_rural"
        return pop


    def processar_tratar():
        pop_urbana = extrair_serie_pop_urbana_rural("POPUR")
        pop_rural = extrair_serie_pop_urbana_rural("POPRU")

        munic_selecionados = {
            "3548708": "São Bernardo do Campo",
            "3534401": "Osasco",
            "3552205": "Sorocaba",
            "3543402": "Ribeirão Preto",
            "3547809": "Santo André",
            "3549904": "São José dos Campos",
        }
        pop_urbana["municipio"] = pop_urbana["tercodigo"].map(munic_selecionados)
        pop_rural["municipio"] = pop_rural["tercodigo"].map(munic_selecionados)

        pop_urbana = pop_urbana[pop_urbana["tercodigo"].isin(munic_selecionados.keys())]
        pop_rural = pop_rural[pop_rural["tercodigo"].isin(munic_selecionados.keys())]

        pop = pd.concat([pop_urbana, pop_rural], axis=0)

        pop = pop.pivot(
            index=["tercodigo", "year", "municipio"],
            columns="categoria",
            values="value_habitante",
        ).reset_index()

        pop = pop.query("year > 1960")
        return pop


    def calcular_proporcoes(df):
        df[['pop_rural', 'pop_urbana']] = df[['pop_rural', 'pop_urbana']].fillna(0)
        df['pop_total'] = df['pop_urbana'] + df['pop_rural']
        df['prop_urbana'] = df['pop_urbana'] / df['pop_total']
        df['prop_rural'] = df['pop_rural'] / df['pop_total']
        return df


    pop = processar_tratar()
    pop = calcular_proporcoes(pop)
    return pop


pop_censo = extrair_pop_censo_api()
pop_urbana_rural = extrair_pop_urbana_rural_censo_api()


# GRÁFICOS
mapa_cores = {
    "Osasco": "#1F77B4",
    "São José dos Campos": "#AF8DCD",
    "Sorocaba": "#FF9F4A",
    "São Bernardo do Campo": "#E05D5E",
    "Ribeirão Preto": "#61B861",
    "Santo André": "#A98078",
}

def gerar_grafico_piramide_etaria(pop_censo):

    sexos_unicos = pop_censo["sexo"].unique()
    df_masc = pop_censo[pop_censo["sexo"] == sexos_unicos[0]].copy()
    df_fem = pop_censo[pop_censo["sexo"] == sexos_unicos[1]].copy()

    # Para o lado esquerdo (masculino), valores negativos
    df_masc["valor_negativo"] = -df_masc["valor"]

    fig = go.Figure()

    # Adicionar barras masculinas (lado esquerdo)
    fig.add_trace(
        go.Bar(
            y=df_masc["idade"],
            x=df_masc["valor_negativo"],
            name="Masculino",
            orientation="h",
            marker_color="#368CE7",  # Azul
            hovertemplate="Idade: %{y}<br>População: %{text}<extra></extra>",
            text=df_masc["valor"],
            textposition="none",
        )
    )

    # Adicionar barras femininas (lado direito)
    fig.add_trace(
        go.Bar(
            y=df_fem["idade"],
            x=df_fem["valor"],
            name="Feminino",
            orientation="h",
            marker_color="#073C73",
            hovertemplate="Idade: %{y}<br>População: %{x}<extra></extra>",
        )
    )

    # Configurar o layout
    fig.update_layout(
        height=600,
        barmode="overlay",
        xaxis=dict(
            title="População", tickformat=",", showgrid=True, gridcolor="lightgray"
        ),
        yaxis=dict(
            title="Faixa etária",
            showgrid=True,
            gridcolor="lightgray",
            # Centralizar os ticks entre as barras usando índices
            tickmode="array",
            tickvals=np.arange(len(df_masc)) + 0.5,  # Posicionar entre as barras
            ticktext=df_masc["idade"],  # Manter os rótulos originais
        ),
        plot_bgcolor="white",
        showlegend=True,
        legend=dict(orientation="h", yanchor="top", y=1.1, xanchor="left", x=0),
    )

    # Configurar o eixo X para mostrar valores redondos em milhares
    max_valor = max(pop_censo["valor"])

    # Calcular o valor máximo arredondado para cima em milhares
    max_valor_round = int(np.ceil(max_valor / 1000) * 1000)

    # Criar ticks com valores redondos em milhares
    tick_vals = []
    tick_texts = []

    # Lado negativo (masculino)
    for i in range(0, int(max_valor_round / 1000) + 1, 5):  # De 5 em 5 mil
        tick_vals.append(-i * 1000)
        tick_texts.append(f"{i}k")

    # Lado positivo (feminino) - excluir o 0 que já foi adicionado
    for i in range(5, int(max_valor_round / 1000) + 1, 5):  # De 5 em 5 mil
        tick_vals.append(i * 1000)
        tick_texts.append(f"{i}k")

    # Adicionar o 0 no meio
    tick_vals.append(0)
    tick_texts.append("0")

    # Ordenar os valores
    sorted_pairs = sorted(zip(tick_vals, tick_texts))
    tick_vals, tick_texts = zip(*sorted_pairs)

    fig.update_xaxes(
        tickmode="array",
        tickvals=tick_vals,
        ticktext=tick_texts,
    )

    return fig


def gerar_grafico_populacao():
    fig = px.line(
        populacao_densidade,
        x="year",
        y="value_habitante",
        color="municipio",
        labels={
            "year": "Ano",
            "value_habitante": "População residente",
            "municipio": "Município",
        },
        markers=True,
        template="none",
        line_shape="spline",
        color_discrete_map=mapa_cores,
    )

    fig.for_each_trace(
        lambda trace: trace.update(
            line=dict(
                width=2 if trace.name == "Osasco" else 1.5,
                dash="solid" if trace.name == "Osasco" else "dot",
            ),
            opacity=1 if trace.name == "Osasco" else 0.7,
        )
    )
    fig.update_xaxes(tickformat="%m/%Y")
    fig.update_yaxes(tickformat=",")
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis=dict(gridcolor="lightgray", zeroline=False, title_standoff=30),
        xaxis=dict(gridcolor="white", zeroline=False, title_standoff=30),
        legend_title_text="Município",
        legend=dict(orientation="h", yanchor="bottom", y=-0.6, xanchor="center", x=0.5),
        separators=",.",
        hovermode="x unified",
    )
    fig.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>Mês/Ano: %{x}<br>População residente: %{y:,.0f}<extra></extra>"
    )

    return fig


def gerar_grafico_densidade():
    populacao_densidade_filtro = populacao_densidade.query(
        "densidade_demografica.notna()"
    ).copy()
    fig = px.line(
        populacao_densidade_filtro,
        x="year",
        y="densidade_demografica",
        color="municipio",
        labels={
            "year": "Ano",
            "densidade_demografica": "Densidade demográfica (hab/km²)",
            "municipio": "Município",
        },
        markers=True,
        template="none",
        line_shape="spline",
        color_discrete_map=mapa_cores,
    )

    fig.for_each_trace(
        lambda trace: trace.update(
            line=dict(
                width=2 if trace.name == "Osasco" else 1.5,
                dash="solid" if trace.name == "Osasco" else "dot",
            ),
            opacity=1 if trace.name == "Osasco" else 0.7,
        )
    )
    fig.update_xaxes(tickformat="%m/%Y")
    fig.update_yaxes(tickformat=",")
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis=dict(gridcolor="lightgray", zeroline=False, title_standoff=30),
        xaxis=dict(gridcolor="white", zeroline=False, title_standoff=30),
        legend_title_text="Município",
        legend=dict(orientation="h", yanchor="bottom", y=-0.6, xanchor="center", x=0.5),
        separators=",.",
        hovermode="x unified",
    )
    fig.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>Mês/Ano: %{x}<br>Densidade demográfica: %{y:,.0f}<extra></extra>"
    )

    return fig


def gerar_grafico_populacao_urbana_rural(pop_urbana_rural):

    fig = px.line(
        pop_urbana_rural,
        x="year",
        y="prop_urbana",
        color="municipio",
        labels={
            "year": "Ano",
            "prop_urbana": "Proporção da população urbana",
            "municipio": "Município",
        },
        markers=True,
        template="none",
        line_shape="spline",
        color_discrete_map=mapa_cores,
    )

    fig.for_each_trace(
        lambda trace: trace.update(
            line=dict(
                width=2 if trace.name == "Osasco" else 1.5,
                dash="solid" if trace.name == "Osasco" else "dot",
            ),
            opacity=1 if trace.name == "Osasco" else 0.7,
        )
    )
    fig.update_xaxes(tickformat="%m/%Y")
    fig.update_yaxes(tickformat=",")
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis=dict(gridcolor="lightgray", zeroline=False, title_standoff=30),
        xaxis=dict(gridcolor="white", zeroline=False, title_standoff=30),
        legend_title_text="Município",
        legend=dict(orientation="h", yanchor="bottom", y=-0.6, xanchor="center", x=0.5),
        separators=",.",
        hovermode="x unified",
    )
    fig.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>Mês/Ano: %{x}<br>Proporção da população urbana: %{y:,.0f}<extra></extra>"
    )
    return fig


fig_piramide_etaria = gerar_grafico_piramide_etaria(pop_censo)
fig_populacao = gerar_grafico_populacao()
fig_densidade = gerar_grafico_densidade()
fig_populacao_urbana_rural = gerar_grafico_populacao_urbana_rural(pop_urbana_rural)

layout = dbc.Container(
    [
        html.Br(),
        html.H4("Pirâmide etária da população de Osasco"),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=fig_piramide_etaria), width=12),
            ],
            className="mb-4",
        ),
        html.H4("Evolução populacional"),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=fig_populacao), width=12),
            ],
            className="mb-4",
        ),
        html.H4("Densidade populacional"),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=fig_densidade), width=12),
            ],
            className="mb-4",
        ),
        html.H4("População urbana e rural!"),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=fig_populacao_urbana_rural), width=12),
            ],
            className="mb-4",
        ),
    ]
)
