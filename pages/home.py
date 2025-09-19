from dash import html, register_page
import dash_bootstrap_components as dbc
from src.config import footer

register_page(__name__, path="/", name="Painel de Governo PMO")


# função para criar os botões de navegação
def create_nav_button(icon, text, color, href, preview=False):
    """
    Cria um botão de navegação com estilo consistente.

    Args:
        icon (str): Nome do ícone do Material Icon
        text (str): Texto do botão
        color (str): Cor do ícone (hexadecimal)
        href (str): Destino do link
        preview (bool): Se True, adiciona '(preview)' ao texto do botão

    Returns:
        dbc.Col: Um botão de navegação estilizado
    """
    texto_botao = f"{text} (preview)" if preview else text

    return dbc.Col(
        dbc.CardLink(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div(
                            [
                                html.Span(
                                    # configuração do ícone do botão
                                    icon,
                                    className="material-icons me-3",
                                    style={"fontSize": "2rem", "color": color},
                                ),
                                html.Span(
                                    # configuração do texto do botão
                                    texto_botao,
                                    style={
                                        "fontSize": "1rem",
                                        "textAlign": "center",
                                        "flex": "1",  # Adiciona flex: 1 para ocupar o espaço restante
                                    },
                                ),
                            ],
                            style={
                                # configuração do estilo do ícone e do texto do botão
                                "display": "flex",
                                "alignItems": "center",
                                "justifyContent": "center",  # Centraliza horizontalmente
                                "color": "#213953",
                                "textDecoration": "none",
                                "minHeight": "50px",
                                "width": "100%",
                            },
                        ),
                    ]
                ),
                style={
                    # configuração do estilo do botão
                    "backgroundColor": "white",
                    "borderRadius": "10px",
                    "boxShadow": "0px 4px 12px rgba(0, 0, 0, 0.1)",
                    "transition": "transform 0.2s ease-in-out",
                    "cursor": "pointer",
                },
                className="mb-3 hover-card",
            ),
            href=href, # referencia da pagina a ser redirecionada
            style={
                # configuração do estilo do link do botão
                "textDecoration": "none",
            },
        ),
        width=4, # configuração da largura do botão
    )


# Define configuração dos botões de navegação
NAV_BUTTONS = [
    {
        "icon": "trending_up",
        "text": "Desenvolvimento Econômico",
        "color": "#99d98c",
        "href": "/desenvolvimento_economico",
    },
    {
        "icon": "work",
        "text": "Trabalho e Renda",
        "color": "#34a0a4",
        "href": "/trabalho_e_renda",
    },
    {
        "icon": "location_city",
        "text": "Desenvolvimento Urbano",
        "color": "#168aad",
        "href": "/desenvolvimento_urbano",
    },
    {
        "icon": "group",
        "text": "Desenvolvimento Humano",
        "color": "#1e6091",
        "href": "/desenvolvimento_humano",
    },
    {
        "icon": "currency_exchange",
        "text": "Gestão da Receita Própria",
        "color": "#184e77",
        "href": "/gestao_receita_propria",
        "preview": True,
    },
    {
        "icon": "local_hospital",
        "text": "Saúde",
        "color": "#e74c3c",
        "href": "/saude",
        "preview": True,
    },
    {
        "icon": "account_box",
        "text": "Demografia",
        "color": "#1e6091",
        "href": "/demografia",
        "preview": True,
    }
]

# Cria a linha de botões de navegação
nav_buttons = dbc.Row(
    # aplica a função create_nav_button para cada configuração de botão definida em NAV_BUTTONS
    [create_nav_button(**button_config) for button_config in NAV_BUTTONS],
    className="mt-3",
    justify="center",
)


# Componente de cabeçalho da página
def create_page_header():
    """Cria o cabeçalho da página com título e texto de navegação."""
    return html.Div([
        # título do painel
        html.H3(
            "Bem-vindo ao Painel de Governo da Prefeitura de Osasco!",
            style={"color": "#213953", "fontWeight": "bold"},
            className="text-center mb-4",
        ),
        # texto de navegação
        dbc.Container([
            html.P(
                "Navegue pelas páginas abaixo:",
                className="text-center",
                style={"color": "#213953", "fontSize": "16px"},
            ),
        ]),
    ])

# Botão do catálogo
catalog_button = dbc.Container([
    html.Div([
        html.A(
            "📊 Ver catálogo completo de visuais e indicadores",
            href="/gestao_indicadores",
            className="btn btn-outline-primary btn-sm",
            style={"textDecoration": "none"}
        )
    ], className="text-center mt-4")
], style={"maxWidth": "750px"})

# Definir o layout da página
layout = html.Div(
    [
        html.Div(
            [
                # cabeçalho da página
                create_page_header(),
                # botões de navegação
                dbc.Container(nav_buttons, style={"maxWidth": "750px"}),
                # botão do catálogo (agora abaixo dos botões de navegação)
                catalog_button,
            ],
            style={
                "display": "flex",
                "flexDirection": "column",
                "justifyContent": "center",
                "minHeight": "80vh"
            },
        ),
        # rodapé da página
        html.Div(
            footer,
            style={
                "position": "fixed",
                "bottom": 0,
                "width": "100%",
                "left": 0,
            },
        ),
    ],
)