from dash import html
import dash_bootstrap_components as dbc
from babel.numbers import format_currency, format_percent, format_compact_currency
from .tooltips import TOOLTIPS


def get_options_dropdown(all_data, table, column):
    sorted_values = sorted(all_data[table][column].dropna().unique())
    return [{"label": x, "value": x} for x in sorted_values]


def calcular_pib_atual(pib_por_categoria):
    ano_max = pib_por_categoria["ano"].max()
    pib_corrente_int = (
        pib_por_categoria.loc[
            (pib_por_categoria["ano"] == ano_max)
            & (pib_por_categoria["variavel_dash"] == "Total")
        ]["pib_corrente"]
        .values[0]
        .round()
        .astype(int)
    )
    pib_corrente = format_compact_currency(
        pib_corrente_int, "BRL", locale="pt_BR", fraction_digits=2
    )
    return pib_corrente


def calcular_variacao_pib(pib_por_categoria):
    pib_ano = (
        pib_por_categoria.loc[
            (pib_por_categoria["ano"] == pib_por_categoria["ano"].max())
            & (pib_por_categoria["variavel_dash"] == "Total")
        ]["pib_deflacionado"]
        .values[0]
        .round()
        .astype(int)
    )

    pib_ano_anterior = (
        pib_por_categoria.loc[
            (pib_por_categoria["ano"] == pib_por_categoria["ano"].max() - 1)
            & (pib_por_categoria["variavel_dash"] == "Total")
        ]["pib_deflacionado"]
        .values[0]
        .round()
        .astype(int)
    )

    variacao_pib = (pib_ano - pib_ano_anterior) / pib_ano_anterior
    variacao_pib = format_percent(variacao_pib, format="#,##0.0%", locale="pt_BR")

    return variacao_pib


def create_info_popover(id_referencia, texto_ou_chave):
    """
    Cria um popover informativo com ícone de informação.

    Args:
        id_referencia: ID único para o botão
        texto_ou_chave: Texto direto ou chave do dicionário TOOLTIPS
    """
    # Se for uma chave do dicionário, busca o texto correspondente
    if texto_ou_chave in TOOLTIPS:
        texto = TOOLTIPS[texto_ou_chave]
    else:
        texto = texto_ou_chave

    # Processa o texto para criar elementos HTML formatados
    def process_text_to_html(text):
        lines = text.strip().split("\n")
        html_elements = []

        for line in lines:
            if line.strip():
                # Verifica se a linha tem o padrão "Título: conteúdo"
                if ":" in line:
                    parts = line.split(":", 1)
                    title = parts[0].strip()
                    content = parts[1].strip() if len(parts) > 1 else ""

                    if content:
                        html_elements.append(
                            html.Div(
                                [html.Strong(f"{title}:"), html.Span(f" {content}")],
                                style={"marginBottom": "8px"},
                            )
                        )
                    else:
                        html_elements.append(
                            html.Strong(f"{title}:"), style={"marginBottom": "8px"}
                        )
                else:
                    # Linha sem dois pontos
                    html_elements.append(
                        html.Div(line.strip(), style={"marginBottom": "8px"})
                    )
            else:
                # Linha vazia - adiciona espaçamento
                html_elements.append(html.Br())

        return html_elements

    return html.Div(
        [
            dbc.Button(
                html.I(className="material-icons", children="info"),
                id=id_referencia,
                color="link",
                size="sm",
                className="p-0 ms-2",
                style={"color": "#213953"},
            ),
            dbc.Popover(
                dbc.PopoverBody(
                    html.Div(
                        process_text_to_html(texto), style={"whiteSpace": "pre-line"}
                    )
                ),
                target=id_referencia,
                trigger="hover",
                placement="right",
            ),
        ],
        style={"display": "inline-block"},
    )


def create_breadcrumb(pathname):
    """
    Creates a breadcrumb navigation component based on the current pathname.
    """
    if pathname == "/" or pathname == "":
        return None

    # Remove leading slash and replace underscores with spaces
    path_parts = pathname.strip("/").split("/")
    current_page = path_parts[-1].replace("_", " ").title()

    return html.Div(
        dbc.Breadcrumb(
            items=[
                {"label": "Início", "href": "/", "external_link": True},
                {"label": current_page, "active": True},
            ],
            style={
                "backgroundColor": "transparent",
                "padding": "0",
                "marginBottom": "0",
                # "marginRight": "40px",
            },
        ),
        style={
            "display": "flex",
            "alignItems": "center",
            "height": "100%",
            "color": "white",
            # "width": "100%",
            "justifyContent": "flex-start",
        },
    )
