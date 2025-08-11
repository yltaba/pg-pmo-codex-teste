from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import dash

from src.config import DATA_PATH
from src.load_data import load_data
from src.callbacks import init_callbacks
from flask import request, abort


external_stylesheets = [
    dbc.themes.SANDSTONE,
    "https://fonts.googleapis.com/icon?family=Material+Icons",
]

app = Dash(
    use_pages=True,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
)
app.title = "Painel de Governo PMO"

# DADOS
data_path = DATA_PATH
all_data = load_data()


imagem_cabecalho = html.Img(
    src="/assets/Marca-Osasco-Digital-COLOR-ALTA-02.svg",
    style={
        "width": "350px",
        "height": "auto",
        "display": "block",
        "margin": "10px 20px",  # Remove a margem lateral, mantém só topo e base
        "padding-left": "0",  # Garante que não há padding à esquerda
    },
)

# Main app layout
main_layout = dbc.Container(
    [
        # Breadcrumb navigation
        dcc.Location(id="url", refresh=False),

        # Container fixo para o cabeçalho
        html.Div(
            [
                # Barra azul marinho com breadcrumb
                html.Div(
                    [
                        dbc.Container(
                            id="back-button-container",
                            fluid=True,
                            style={
                                "height": "40px",
                                "display": "flex",
                                "alignItems": "center",
                                "padding": "0",
                                "justifyContent": "space-between",
                                "width": "100%",
                            },
                        )
                    ],
                    style={
                        "backgroundColor": "#3B6B9C",
                        "height": "40px",
                        "marginLeft": "-24px",
                        "marginRight": "-24px",
                        "width": "calc(100% + 48px)",
                    },
                ),
            ],
            style={
                "position": "fixed",  # Fixa o cabeçalho
                "top": 0,  # Alinha ao topo
                "left": 0,  # Alinha à esquerda
                "right": 0,  # Alinha à direita
                "backgroundColor": "white",  # Fundo branco para o cabeçalho
                "zIndex": 1000,  # Garante que fique acima de outros elementos
                "width": "100%",
                "paddingLeft": "24px",  # Adiciona padding para alinhar com o container
                "paddingRight": "24px",
            },
        ),
        # Div para criar espaço para o conteúdo não ficar embaixo do cabeçalho fixo
        html.Div(style={"height": "60px"}),
        # Conteúdo da página
        html.Div(
            dash.page_container,
            style={
                "maxWidth": "1400px",
                "margin": "0 auto",
                "width": "100%",
                "padding": "0 20px",
            },
        ),
    ],
    fluid=True,
    style={
        "overflow-x": "hidden",
        "padding-top": "0",
    },
)

# Layout + autenticação
app.layout = main_layout


@app.callback(Output("back-button-container", "children"), Input("url", "pathname"))
def toggle_navigation(pathname):
    # Breadcrumb informativo em todas as páginas
    breadcrumb_items = []
    
    # Mapeamento de páginas para nomes amigáveis
    page_names = {
        "": "Início",
        "/": "Início",
        "/desenvolvimento_humano": "Desenvolvimento Humano",
        "/desenvolvimento_economico": "Desenvolvimento Econômico", 
        "/desenvolvimento_urbano": "Desenvolvimento Urbano",
        "/trabalho_e_renda": "Trabalho e Renda",
        "/saude": "Saúde",
        "/receita_propria": "Receita Própria",
        "/sobre_dados": "Sobre os Dados",
        "/gestao_indicadores": "Gestão de Indicadores"
    }
    
    # Mapeamento de subpáginas para nomes amigáveis
    subpage_names = {
        "/desenvolvimento_humano/cad_unico": "Cadastro Único",
        "/desenvolvimento_humano/bolsa_familia": "Bolsa Família",
        "/desenvolvimento_humano/vulnerabilidade_social": "Vulnerabilidade Social",
        "/desenvolvimento_humano/home": "Visão Geral",
        "/desenvolvimento_economico/empresas": "Empresas",
        "/desenvolvimento_economico/pib": "PIB",
        "/desenvolvimento_economico/home": "Visão Geral",
        "/desenvolvimento_urbano/zoneamento": "Zoneamento",
        "/desenvolvimento_urbano/loteamento": "Loteamento",
        "/desenvolvimento_urbano/home": "Visão Geral",
        "/saude/vacinas": "Vacinas",
        "/saude/acompanhamento": "Acompanhamento",
        "/saude/cobertura": "Cobertura",
        "/saude/home": "Visão Geral",
        "/saude/sobre": "Sobre"
    }
    
    # Adiciona o item "Início"
    breadcrumb_items.append(
        html.Span(
            "Início",
            style={
                "color": "#ffffff",
                "fontSize": "14px",
                "fontWeight": "500"
            }
        )
    )
    
    # Processa o pathname para criar o breadcrumb
    if pathname and pathname != "/":
        # Verifica se é uma subpágina
        if pathname in subpage_names:
            # É uma subpágina - mostra: Início / Página Principal / Subpágina
            main_page = pathname.split("/")[1]  # Pega a parte principal do path
            main_page_name = page_names.get(f"/{main_page}", main_page.replace("_", " ").title())
            subpage_name = subpage_names[pathname]
            
            # Adiciona página principal
            breadcrumb_items.append(
                html.Span(
                    [
                        html.Span(" / ", style={"color": "#ffffff", "margin": "0 8px", "opacity": "0.8"}),
                        html.Span(main_page_name, style={"color": "#ffffff", "fontSize": "14px", "fontWeight": "500"})
                    ],
                    style={"fontSize": "14px"}
                )
            )
            
            # Adiciona subpágina
            breadcrumb_items.append(
                html.Span(
                    [
                        html.Span(" / ", style={"color": "#ffffff", "margin": "0 8px", "opacity": "0.8"}),
                        html.Span(subpage_name, style={"color": "#ffffff", "fontWeight": "500"})
                    ],
                    style={"fontSize": "14px"}
                )
            )
        else:
            # É uma página principal - mostra: Início / Página Principal
            current_page_name = page_names.get(pathname, pathname.replace("/", "").replace("_", " ").title())
            breadcrumb_items.append(
                html.Span(
                    [
                        html.Span(" / ", style={"color": "#ffffff", "margin": "0 8px", "opacity": "0.8"}),
                        html.Span(current_page_name, style={"color": "#ffffff", "fontWeight": "500"})
                    ],
                    style={"fontSize": "14px"}
                )
            )
    
    # Botão do catálogo (sempre visível)
    catalog_button = html.A(
        "📊 Catálogo de dados",
        href="/gestao_indicadores",
        style={
            "color": "#ffffff",
            "textDecoration": "none",
            "fontSize": "12px",
            "fontWeight": "500",
            "padding": "4px 8px",
            "border": "1px solid #ffffff",
            "borderRadius": "4px",
            "backgroundColor": "transparent",
            "transition": "all 0.2s ease"
        },
        className="catalog-button"
    )
    
    # Layout com botão à esquerda e breadcrumb centralizado
    return html.Div(
        [
            # Botão do catálogo à esquerda
            html.Div(
                catalog_button,
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "height": "100%",
                    "position": "absolute",
                    "left": "20px"
                }
            ),
            # Breadcrumb centralizado
            html.Div(
                breadcrumb_items,
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "height": "32px",
                    "fontSize": "14px",
                    "width": "100%"
                }
            )
        ],
        style={
            "display": "flex",
            "alignItems": "center",
            "height": "100%",
            "width": "100%",
            "position": "relative"
        }
    )


init_callbacks(app, all_data)


# @app.server.before_request
# def check_iframe_access():
#     """Verifica se o acesso é feito através de iframe"""
#     # Permite acesso a assets (CSS, JS, imagens)
#     if request.path.startswith('/assets/'):
#         return
    
#     # Verifica se há referer (indica que veio de outra página)
#     referer = request.headers.get('Referer')
    
#     # Se não há referer, é acesso direto - bloqueia
#     if not referer:
#         abort(403, description="Acesso direto não permitido. Use a aplicação principal.")
    
#     # Se há referer, permite o acesso (vem de iframe)
#     return


server = app.server
if __name__ == "__main__":
    # app.run(host="0.0.0.0")
    app.run(debug=True)