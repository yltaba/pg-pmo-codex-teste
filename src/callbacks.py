from dash import Input, Output, html, State, no_update
import plotly.express as px
from babel.numbers import format_decimal, format_percent
import dash_bootstrap_components as dbc
import pandas as pd

from src.config import TEMPLATE


def init_callbacks(app, all_data):

    # CALLBACKS DE FILTRO - GRÁFICOS
    @app.callback(
        Output("fig-rais-anual", "figure"), Input("filtro-cnae-rais-saldo", "value")
    )
    def atualizar_grafico_rais_anual(filtro_cnae):
        if filtro_cnae == "Todos":
            df_filtrado = all_data["rais_anual"]
        else:
            df_filtrado = all_data["rais_anual"][
                all_data["rais_anual"]["descricao_secao_cnae"] == filtro_cnae
            ]

        rais_anual_grp = df_filtrado.groupby("ano", as_index=False).agg(
            {"quantidade_vinculos_ativos": "sum"}
        )

        fig = px.area(
            rais_anual_grp,
            x="ano",
            y="quantidade_vinculos_ativos",
            labels={
                "ano": "Ano",
                "quantidade_vinculos_ativos": "Quantidade de vínculos empregatícios ativos",
            },
            markers="o",
            template="plotly_white",
            color_discrete_sequence=["#75BAFF"],
        )
        fig.add_annotation(
            text="Fonte: <a href='https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/estatisticas-trabalho/rais/rais-2024'>RAIS Estabelecimentos</a>",
            xref="paper",
            yref="paper",
            x=0,
            y=-0.2,
            showarrow=False,
            font=dict(size=12),
            clicktoshow=False,
        )
        fig.update_xaxes(tickmode="linear", dtick="M1", tickangle=45)
        fig.update_yaxes(tickformat=",")
        return fig

    @app.callback(
        [
            Output("card-estoque-atual-value", "children"),
            Output("card-variacao-estoque-value", "children"),
            Output("card-variacao-arrow", "children"),
            Output("card-variacao-arrow", "style"),
        ],
        Input("filtro-cnae-rais-saldo", "value"),
    )
    def atualizar_cards_estoque(filtro_cnae):
        if filtro_cnae == "Todos":
            df_filtrado = all_data["rais_anual"]
        else:
            df_filtrado = all_data["rais_anual"][
                all_data["rais_anual"]["descricao_secao_cnae"] == filtro_cnae
            ]

        # Existing calculations
        estoque_atual = (
            df_filtrado.loc[df_filtrado["ano"] == df_filtrado["ano"].max()]
            .agg({"quantidade_vinculos_ativos": "sum"})
            .values[0]
        )
        estoque_atual_formatted = format_decimal(
            estoque_atual, format="#,##0", locale="pt_BR"
        )

        estoque_anterior = (
            df_filtrado.loc[df_filtrado["ano"] == df_filtrado["ano"].max() - 1]
            .agg({"quantidade_vinculos_ativos": "sum"})
            .values[0]
        )
        variacao_estoque = (estoque_atual - estoque_anterior) / estoque_anterior
        variacao_estoque_formatted = format_percent(
            variacao_estoque, format="#,##0.0%", locale="pt_BR"
        )

        arrow_symbol = "▲" if variacao_estoque >= 0 else "▼"
        arrow_style = {
            "color": "#28a745" if variacao_estoque >= 0 else "#dc3545",
            "fontSize": "24px",
            "marginLeft": "8px",
        }

        return (
            estoque_atual_formatted,
            variacao_estoque_formatted,
            arrow_symbol,
            arrow_style,
        )

    @app.callback(
        Output("fig-saldo-anual", "figure"), Input("filtro-cnae-caged-saldo", "value")
    )
    def atualizar_grafico_caged(filtro_cnae):

        if filtro_cnae == "Todos":
            df_filtrado = all_data["caged_saldo_anual"]
        else:
            df_filtrado = all_data["caged_saldo_anual"][
                all_data["caged_saldo_anual"]["cnae_2_descricao_secao"] == filtro_cnae
            ]

        caged_ano = df_filtrado.groupby("ano", as_index=False).agg(
            {"saldo_movimentacao": "sum"}
        )

        fig = px.bar(
            caged_ano,
            x="ano",
            y="saldo_movimentacao",
            template=TEMPLATE,
            labels={
                "ano": "Ano",
                "saldo_movimentacao": "Saldo das movimentações",
            },
            color_discrete_sequence=["#75BAFF"],
        )
        fig.add_annotation(
            text="Fonte: <a href='https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/estatisticas-trabalho/novo-caged/2025/fevereiro/pagina-inicial'>CAGED e NOVO CAGED</a>",
            xref="paper",
            yref="paper",
            x=0,
            y=-0.2,
            showarrow=False,
            font=dict(size=12),
        )
        fig.update_xaxes(tickmode="linear", dtick="M1", tickangle=45)
        fig.update_yaxes(tickformat=",")

        return fig

    # @app.callback(
    #     [
    #         Output("card-saldo-atual-value", "children"),
    #         Output("card-variacao-saldo-value", "children"),
    #         Output("card-variacao-saldo-arrow", "children"),
    #         Output("card-variacao-saldo-arrow", "style"),
    #     ],
    #     Input("filtro-cnae-caged-saldo", "value"),
    # )
    # def atualizar_cards_estoque(filtro_cnae):
    #     if filtro_cnae == "Todos":
    #         df_filtrado = all_data["caged_saldo_anual"]
    #     else:
    #         df_filtrado = all_data["caged_saldo_anual"][
    #             all_data["caged_saldo_anual"]["cnae_2_descricao_secao"] == filtro_cnae
    #         ]
    #     saldo_ano_max = (
    #         df_filtrado.loc[df_filtrado["ano"] == df_filtrado["ano"].max()]
    #         .agg({"saldo_movimentacao": "sum"})
    #         .values[0]
    #     )
    #     saldo_ano_max_formatted = format_decimal(
    #         saldo_ano_max, format="#,##0", locale="pt_BR"
    #     )

    #     saldo_ano_max_var = (
    #         df_filtrado.loc[df_filtrado["ano"] == df_filtrado["ano"].max() - 1]
    #         .agg({"saldo_movimentacao": "sum"})
    #         .values[0]
    #     )

    #     saldo_ano_max_lag1 = (
    #         df_filtrado.loc[df_filtrado["ano"] == df_filtrado["ano"].max() - 2]
    #         .agg({"saldo_movimentacao": "sum"})
    #         .values[0]
    #     )
    #     variacao_mov = (saldo_ano_max_var - saldo_ano_max_lag1) / saldo_ano_max_lag1
    #     variacao_mov_formatted = format_percent(
    #         variacao_mov, format="#,##0%", locale="pt_BR"
    #     )

    #     arrow_symbol = "▲" if variacao_mov >= 0 else "▼"
    #     arrow_style = {
    #         "color": "#28a745" if variacao_mov >= 0 else "#dc3545",
    #         "fontSize": "24px",
    #         "marginLeft": "8px",
    #     }

    #     return (
    #         saldo_ano_max_formatted,
    #         variacao_mov_formatted,
    #         arrow_symbol,
    #         arrow_style,
    #     )

    @app.callback(
        [
            Output("card-saldo-atual-value", "children"),
            Output("card-saldo-atual-arrow", "children"),  # Adicione esta linha
            Output("card-saldo-atual-arrow", "style"),  # Adicione esta linha
            Output("card-variacao-saldo-value", "children"),
            Output("card-variacao-saldo-arrow", "children"),
            Output("card-variacao-saldo-arrow", "style"),
        ],
        Input("filtro-cnae-caged-saldo", "value"),
    )
    def atualizar_cards_estoque(filtro_cnae):
        if filtro_cnae == "Todos":
            df_filtrado = all_data["caged_saldo_anual"]
        else:
            df_filtrado = all_data["caged_saldo_anual"][
                all_data["caged_saldo_anual"]["cnae_2_descricao_secao"] == filtro_cnae
            ]

        # Obter ano atual (ano máximo)
        current_year = df_filtrado["ano"].max()

        # Calcular total do ano atual
        saldo_atual = (
            df_filtrado.loc[df_filtrado["ano"] == current_year]
            .agg({"saldo_movimentacao": "sum"})
            .values[0]
        )
        saldo_atual_formatted = format_decimal(
            saldo_atual, format="#,##0", locale="pt_BR"
        )

        # Arrow saldo atual
        saldo_arrow_symbol = "▲" if saldo_atual >= 0 else "▼"
        saldo_arrow_style = {
            "color": "#28a745" if saldo_atual >= 0 else "#dc3545",
            "fontSize": "24px",
            "marginLeft": "8px",
        }

        # Calcular total do ano anterior
        previous_year = current_year - 1
        saldo_anterior = (
            df_filtrado.loc[df_filtrado["ano"] == previous_year]
            .agg({"saldo_movimentacao": "sum"})
            .values[0]
        )

        # Calcular variação: (atual - anterior) / anterior
        variacao_mov = (saldo_atual - saldo_anterior) / saldo_anterior
        variacao_mov_formatted = format_percent(
            variacao_mov, format="#,##0%", locale="pt_BR"
        )

        # Arrow variação
        variacao_arrow_symbol = "▲" if variacao_mov >= 0 else "▼"
        variacao_arrow_style = {
            "color": "#28a745" if variacao_mov >= 0 else "#dc3545",
            "fontSize": "24px",
            "marginLeft": "8px",
        }

        return (
            saldo_atual_formatted,
            saldo_arrow_symbol,  # Nova arrow para saldo atual
            saldo_arrow_style,  # Estilo da nova arrow
            variacao_mov_formatted,
            variacao_arrow_symbol,
            variacao_arrow_style,
        )

    @app.callback(
        Output("fig-caged-saldo-secao", "figure"),
        Input("filtro-ano-caged-secao", "value"),
    )
    def atualizar_grafico_caged_saldo_secao(filtro_ano):
        if filtro_ano == "Todos":
            df_filtrado = all_data["caged_saldo_secao"]
        else:
            df_filtrado = all_data["caged_saldo_secao"][
                all_data["caged_saldo_secao"]["ano"] == filtro_ano
            ]

        caged_saldo_secao_grp = (
            df_filtrado.groupby("cnae_2_descricao_secao", as_index=False)
            .agg({"saldo_movimentacao": "sum"})
            .sort_values("saldo_movimentacao")
        )

        caged_saldo_secao_grp["cnae_2_descricao_secao"] = caged_saldo_secao_grp[
            "cnae_2_descricao_secao"
        ].str.capitalize()

        fig = px.bar(
            caged_saldo_secao_grp,
            x="saldo_movimentacao",
            y="cnae_2_descricao_secao",
            orientation="h",
            labels={
                "saldo_movimentacao": "Saldo das movimentações",
                "cnae_2_descricao_secao": "Seção da CNAE",
            },
            template=TEMPLATE,
            color_discrete_sequence=["#75BAFF"],
        )
        fig.add_annotation(
            text="Fonte: <a href='https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/estatisticas-trabalho/novo-caged/2025/fevereiro/pagina-inicial'>CAGED e NOVO CAGED</a>",
            xref="paper",
            yref="paper",
            x=0.0,
            y=-0.2,
            showarrow=False,
            font=dict(size=12),
            xanchor="center",
        )
        return fig

    @app.callback(
        Output("fig-caged-saldo-idade", "figure"),
        Input("filtro-ano-caged-idade", "value"),
    )
    def atualizar_grafico_caged_saldo_idade(filtro_ano):
        if filtro_ano == "Todos":
            df_filtrado = all_data["caged_saldo_idade"].copy()
        else:
            df_filtrado = all_data["caged_saldo_idade"][
                all_data["caged_saldo_idade"]["ano"] == filtro_ano
            ].copy()

        faixas = [
            "0-5",
            "6-10",
            "11-15",
            "16-20",
            "21-25",
            "26-30",
            "31-35",
            "36-40",
            "41-45",
            "46-50",
            "51-55",
            "56-60",
            "61-65",
            "66-70",
            "71-75",
            "76-80",
            "81-85",
            "86-90",
            "91-95",
            "96-100",
        ]

        df_filtrado["idade_grupo"] = pd.Categorical(
            df_filtrado["idade_grupo"], categories=faixas, ordered=True
        )

        caged_saldo_idade_grp = df_filtrado.groupby(
            "idade_grupo", as_index=False, observed=True
        ).agg({"saldo_movimentacao": "sum"})

        fig = px.bar(
            caged_saldo_idade_grp,
            x="saldo_movimentacao",
            y="idade_grupo",
            labels={
                "idade_grupo": "Idade",
                "saldo_movimentacao": "Saldo das movimentações",
            },
            orientation="h",
            template=TEMPLATE,
            color_discrete_sequence=["#75BAFF"],
        )
        fig.update_layout(bargap=0.05)
        fig.add_annotation(
            text="Fonte: <a href='https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/estatisticas-trabalho/novo-caged/2025/fevereiro/pagina-inicial'>CAGED e NOVO CAGED</a>",
            xref="paper",
            yref="paper",
            x=0.05,
            y=-0.2,
            showarrow=False,
            font=dict(size=12),
            xanchor="center",
        )
        return fig

    @app.callback(
        Output("fig-caged-salario-medio", "figure"),
        [
            Input("filtro-ano-caged-salario-medio", "value"),
            Input("salario-stat-type", "value"),
        ],
    )
    def atualizar_grafico_caged_media_salario(filtro_cnae, stat_type):
        # Filtrar por CNAE, se aplicável
        df_filtrado = (
            all_data["caged_media_salario"]
            if filtro_cnae == "Todos"
            else all_data["caged_media_salario"][
                all_data["caged_media_salario"]["cnae_2_descricao_secao"] == filtro_cnae
            ]
        )

        # Choose aggregation function based on radio button selection
        agg_func = "mean" if stat_type == "mean" else "median"
        stat_label = "Média" if stat_type == "mean" else "Mediana"

        # Agrupar corretamente
        caged_media_salario_grp = (
            df_filtrado.groupby(["ano", "variable"], as_index=False)
            .agg({"salario_medio": agg_func})
            .sort_values("ano")
        )

        # Criar gráfico de linha
        fig = px.line(
            caged_media_salario_grp,
            y="salario_medio",
            x="ano",
            labels={
                "ano": "Ano",
                "salario_medio": f"{stat_label} Salarial",
                "variable": "Tipo de movimentação",
            },
            color="variable",
            markers=True,
            template=TEMPLATE,
            color_discrete_sequence=["#75BAFF", "#3670AA"],
        )

        # Adicionar anotação da fonte
        fig.add_annotation(
            text="Fonte: <a href='https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/estatisticas-trabalho/novo-caged/2025/fevereiro/pagina-inicial'>CAGED e NOVO CAGED</a>",
            xref="paper",
            yref="paper",
            x=0.0,
            y=-0.2,
            showarrow=False,
            font=dict(size=12),
            xanchor="left",
        )

        return fig

    @app.callback(
        Output("fig-caged-media-idade", "figure"),
        [
            Input("filtro-ano-caged-media-idade", "value"),
            Input("media-idade-stat-type", "value"),
        ],
    )
    def atualizar_grafico_caged_media_idade(filtro_cnae, stat_type):
        # Filtrar por CNAE, se aplicável
        df_filtrado = (
            all_data["caged_media_idade"]
            if filtro_cnae == "Todos"
            else all_data["caged_media_idade"][
                all_data["caged_media_idade"]["cnae_2_descricao_secao"] == filtro_cnae
            ]
        )

        # Choose aggregation function based on radio button selection
        agg_func = "mean" if stat_type == "mean" else "median"
        stat_label = "Média" if stat_type == "mean" else "Mediana"

        # Agrupar corretamente
        caged_media_idade_grp = (
            df_filtrado.groupby(["ano", "variable"], as_index=False)
            .agg({"media_idade": agg_func})  # Fixed the aggregation syntax
            .sort_values("ano")
        )

        # Criar gráfico de linha
        fig = px.line(
            caged_media_idade_grp,
            y="media_idade",
            x="ano",
            labels={
                "ano": "Ano",
                "media_idade": f"{stat_label} de Idade",
                "variable": "Tipo de movimentação",
            },
            color="variable",
            markers=True,
            template=TEMPLATE,
            color_discrete_sequence=["#75BAFF", "#3670AA"],
        )

        # Adicionar anotação da fonte
        fig.add_annotation(
            text="Fonte: <a href='https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/estatisticas-trabalho/novo-caged/2025/fevereiro/pagina-inicial'>CAGED e NOVO CAGED</a>",
            xref="paper",
            yref="paper",
            x=0.0,
            y=-0.2,
            showarrow=False,
            font=dict(size=12),
            xanchor="left",
        )

        return fig

    @app.callback(
        Output("fig-abertura-encerramento", "figure"),
        Input("filtro-des-atividade", "value"),
    )
    def atualizar_grafico_abertura_encerramento_empresas(filtro_atividade):
        if filtro_atividade == "Todos":
            df_filtrado = all_data["abertura_encerramento_empresas_cleaned"]
        else:
            df_filtrado = all_data["abertura_encerramento_empresas_cleaned"][
                all_data["abertura_encerramento_empresas_cleaned"]["des_atividade"]
                == filtro_atividade
            ]

        abertura_encerramento_ano = df_filtrado.groupby("ano", as_index=False).agg(
            {"n_empresas_encerradas": "sum", "n_empresas_abertas": "sum"}
        )
        abertura_encerramento_ano["ano"] = abertura_encerramento_ano["ano"].astype(str)

        fig_abertura_encerramento = px.bar(
            abertura_encerramento_ano,
            x="ano",
            y=["n_empresas_encerradas", "n_empresas_abertas"],
            barmode="group",
            template=TEMPLATE,
            color_discrete_map={
                "n_empresas_encerradas": "#1666ba",
                "n_empresas_abertas": "#52b69a",
            },
            labels={"value": "Número de Empresas", "ano": "Ano", "variable": "Status"},
            text_auto=True,
        )
        fig_abertura_encerramento.update_traces(
            texttemplate="%{y:,.0f}", textposition="outside"
        )
        fig_abertura_encerramento.update_traces(
            name="Empresas encerradas", selector=dict(name="n_empresas_encerradas")
        )
        fig_abertura_encerramento.update_traces(
            name="Empresas abertas", selector=dict(name="n_empresas_abertas")
        )
        fig_abertura_encerramento.update_layout(
            legend=dict(
                orientation="v", yanchor="top", y=0.99, xanchor="center", x=0.13
            ),
            bargap=0.15,
            bargroupgap=0.05,
        )
        fig_abertura_encerramento.update_yaxes(tickformat=",")

        fig_abertura_encerramento.add_shape(
            type="line",
            x0=2 / 3,
            x1=2 / 3,  # 0.666... is between 2024 and 2025
            y0=0,
            y1=1,
            xref="x domain",
            yref="paper",
            line=dict(color="black", width=2, dash="dash"),
        )

        fig_abertura_encerramento.add_annotation(
            x=0.68,  # a bit to the right of the line (in x domain)
            y=1,  # top of the plot (in y domain)
            xref="x domain",
            yref="paper",
            text="*",
            showarrow=False,
            font=dict(size=14, color="gray"),
            align="left",
            xanchor="left",
            yanchor="top",
        )

        fig_abertura_encerramento.add_annotation(
            text="Fonte: <a href='https://sigt.osasco.sp.gov.br/iTRIB2/index.jsp'>SIGT</a>",
            xref="paper",
            yref="paper",
            x=0,
            y=-0.1,
            showarrow=False,
            font=dict(size=12),
        )

        fig_abertura_encerramento.add_annotation(
            text="* A partir de 2025, dados de abertura e encerramento de empresas são inseridos automaticamente desde sistema da Receita Federal.",
            xref="paper",
            yref="paper",
            x=0.35,
            y=-0.25,
            showarrow=False,
            font=dict(size=12),
            xanchor="center",
            clicktoshow=False,
        )

        return fig_abertura_encerramento

    @app.callback(
        [
            Output("card-saldo-empresas-value", "children"),
            Output("card-variacao-saldo-empresas-arrow", "children"),
            Output("card-variacao-saldo-empresas-arrow", "style"),
        ],
        Input("filtro-des-atividade", "value"),
    )
    def atualizar_cards_abertura_empresas(filtro_atividade):
        if filtro_atividade == "Todos":
            df_filtrado = all_data["abertura_encerramento_empresas_cleaned"]
        else:
            df_filtrado = all_data["abertura_encerramento_empresas_cleaned"][
                all_data["abertura_encerramento_empresas_cleaned"]["des_atividade"]
                == filtro_atividade
            ]

        abertura_atual = (
            df_filtrado.loc[df_filtrado["ano"] == df_filtrado["ano"].max()]
            .agg({"n_empresas_abertas": "sum"})
            .values[0]
        )

        encerramento_atual = (
            df_filtrado.loc[df_filtrado["ano"] == df_filtrado["ano"].max()]
            .agg({"n_empresas_encerradas": "sum"})
            .values[0]
        )
        variacao_abertura = abertura_atual - encerramento_atual
        variacao_abertura_formatted = format_decimal(
            variacao_abertura, format="#,##0", locale="pt_BR"
        )

        arrow_symbol = "▲" if variacao_abertura >= 0 else "▼"
        arrow_style = {
            "color": "#28a745" if variacao_abertura >= 0 else "#dc3545",
            "fontSize": "24px",
            "marginLeft": "8px",
        }

        return (
            variacao_abertura_formatted,
            arrow_symbol,
            arrow_style,
        )

    # TRIBUTOS POR SUBCATEGORIA
    @app.callback(
        Output("fig-subcateg-tributo", "figure"), Input("filtro-categ-tributo", "value")
    )
    def atualizar_grafico_subcateg_tributo(categoria):
        if categoria == "Todos":
            df_filtrado = all_data["tb_sigt_receita_categ_tributo"].copy()
        else:
            df_filtrado = all_data["tb_sigt_receita_categ_tributo"][
                all_data["tb_sigt_receita_categ_tributo"]["CATEGORIA_TRIBUTO"]
                == categoria
            ].copy()

        ano_order = ["2023", "2024", "2025"]
        df_filtrado["ANO"] = pd.Categorical(
            df_filtrado["ANO"].astype(str),
            categories=ano_order,
            ordered=True,
        )

        # Process the data
        df_filtrado["TOTAL_RECEITA_MILHOES"] = df_filtrado["TOTAL_RECEITA"] / 1_000_000

        # Create the figure
        fig = px.bar(
            df_filtrado,
            x="TOTAL_RECEITA_MILHOES",
            y="TRIBUTO",
            text="TOTAL_RECEITA_MILHOES",
            color="ANO",
            color_discrete_sequence=["#1f77b4", "#123E5C", "#2ca02c"],
            orientation="h",
            barmode="group",
            template=TEMPLATE,
            labels={
                "TRIBUTO": "Subcategoria Tributária",
                "TOTAL_RECEITA_MILHOES": "Receita (Milhões)",
                "ANO": "Ano",
            },
        )

        fig.update_layout(
            xaxis_tickangle=-45,
            showlegend=True,
            legend_title="Ano",
            bargap=0.5,
            margin=dict(t=20, b=40, l=40, r=20),
        )

        fig.update_traces(
            textposition="outside",
            texttemplate="%{text:.1f}",
            marker_line_color="black",
            marker_line_width=1,
        )

        return fig

    @app.callback(
        Output("fig-rais-tamanho-estabelecimento", "figure"),
        [
            Input("filtro-ano-rais-tamanho-estabelecimento", "value"),
            Input("filtro-cnae-rais-tamanho-estabelecimento", "value"),
        ],
    )
    def atualizar_grafico_rais_tamanho_estabelecimento(filtro_ano, filtro_cnae):
        # Filtro por ano
        if filtro_ano == "Todos":
            df_filtrado = all_data["rais_tamanho_estabelecimento"].copy()
        else:
            df_filtrado = all_data["rais_tamanho_estabelecimento"][
                all_data["rais_tamanho_estabelecimento"]["ano"] == filtro_ano
            ].copy()

        # Filtro por seção CNAE
        if filtro_cnae != "Todos":
            df_filtrado = df_filtrado[
                df_filtrado["descricao_secao_cnae"] == filtro_cnae
            ].copy()

        faixas = [
            "Zero",
            "Ate 4",
            "De 5 a 9",
            "De 10 a 19",
            "De 20 a 49",
            "De 50 a 99",
            "De 100 a 249",
            "De 250 a 499",
            "De 500 a 999",
            "1000 ou mais",
        ]

        df_filtrado["tamanho_estabelecimento"] = pd.Categorical(
            df_filtrado["tamanho_estabelecimento"], categories=faixas, ordered=True
        )

        rais_tamanho_estabelecimento_grp = df_filtrado.groupby(
            "tamanho_estabelecimento", as_index=False, observed=True
        ).agg({"size": "sum"})

        fig = px.bar(
            rais_tamanho_estabelecimento_grp,
            x="size",
            y="tamanho_estabelecimento",
            labels={
                "tamanho_estabelecimento": "Tamanho do estabelecimento",
                "size": "Quantidade de empresas",
            },
            orientation="h",
            template=TEMPLATE,
            color_discrete_sequence=["#75BAFF"],
        )
        fig.update_layout(bargap=0.05)
        fig.add_annotation(
            text="Fonte: <a href='https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/estatisticas-trabalho/rais/rais-2024'>RAIS</a>",
            xref="paper",
            yref="paper",
            x=0.05,
            y=-0.2,
            showarrow=False,
            font=dict(size=12),
            xanchor="center",
        )
        return fig

    try:
        from pages.saude.callbacks import init_saude_callbacks

        init_saude_callbacks(app)
    except ImportError as e:
        print(f"Erro ao importar callbacks de saúde: {e}")
        pass
