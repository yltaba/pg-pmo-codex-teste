import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/saude/sobre", name="Sobre", title="Sobre")

layout = dbc.Container([
    # Header section
    dbc.Row([
        dbc.Col([
            html.H1(
                "Informações sobre o painel",
                className="text-center mb-4",
                style={
                    "color": "#2c3e50",
                    "fontWeight": "bold",
                    "marginTop": "2rem"
                }
            ),
            html.Hr(style={"borderColor": "#27ae60", "borderWidth": "3px", "width": "100px", "margin": "0 auto 2rem auto"}),
        ])
    ]),
    
    # Data Overview Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(
                        "Visão geral dos dados",
                        className="card-title mb-3",
                        style={"color": "#2c3e50"}
                    ),
                    html.Div([
                        html.P([
                            html.I(className="fas fa-info-circle me-2", style={"color": "#27ae60"}),
                            "Os dados apresentados são atualizados regularmente e incluem informações de todas as escolas da rede municipal de Osasco."
                        ], className="mb-3"),
                        html.P([
                            html.I(className="fas fa-calendar-alt me-2", style={"color": "#27ae60"}),
                            "Período de dados: 2015 até o ano atual"
                        ], className="mb-3"),
                    ], style={"color": "#7f8c8d"})
                ])
            ], style={
                "border": "none",
                "backgroundColor": "#f8f9fa",
                "marginBottom": "2rem"
            })
        ], width=12)
    ]),
    
    # Data Sources Section
    dbc.Row([
        dbc.Col([
            html.H3(
                "Fontes dos dados",
                className="mb-4",
                style={"color": "#2c3e50"}
            )
        ], width=12)
    ]),
    
    dbc.Row([
        # Data Source 1
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5(
                        "Dados de vacinação",
                        className="card-title",
                        style={"color": "#2c3e50"}
                    ),
                    html.P(
                        "Informações sobre aplicação de vacinas nas escolas municipais de Osasco, "
                        "incluindo tipo de vacina, data de aplicação, escola e dados demográficos dos alunos.",
                        className="card-text",
                        style={"color": "#7f8c8d"}
                    ),
                ])
            ], style={
                "height": "100%",
                "border": "none",
                "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.1)"
            })
        ], width=6, className="mb-3"),
        
        # Data Source 2
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5(
                        "Dados de alunos",
                        className="card-title",
                        style={"color": "#2c3e50"}
                    ),
                    html.P(
                        "Cadastro de alunos da rede municipal de ensino, com informações "
                        "demográficas e escolares para análise da cobertura vacinal.",
                        className="card-text",
                        style={"color": "#7f8c8d"}
                    ),
                ])
            ], style={
                "height": "100%",
                "border": "none",
                "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.1)"
            })
        ], width=6, className="mb-3")
    ]),
    
    # Geographic Data Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5(
                        "Dados geográficos",
                        className="card-title",
                        style={"color": "#2c3e50"}
                    ),
                    html.P(
                        "Shapefiles e arquivos GeoJSON com limites territoriais de Osasco provenientes do IBGE.",
                        "Localização das escolas para visualização em mapas provenientes do sistema de educação municipal.",
                        className="card-text",
                        style={"color": "#7f8c8d"}
                    ),
                ])
            ], style={
                "border": "none",
                "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.1)",
                "marginBottom": "2rem"
            })
        ], width=12)
    ]),
], fluid=True, style={"paddingTop": "2rem", "paddingBottom": "2rem"})