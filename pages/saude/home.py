from dash import html, register_page, dcc
import dash_bootstrap_components as dbc

# Registrar a página com um path específico
register_page(__name__, path="/saude/home", name="Início - Saúde")


saude_home_layout = dbc.Container([

    dbc.Row([
        dbc.Col([
            html.Div([
                html.H3("PAINEL DE MONITORAMENTO DE IMUNIZAÇÕES",
                        className="text-center mb-3",
                        style={"color": "#34495e"}),
                html.P("Público alvo: alunos da rede pública de Osasco",
                       className="lead text-center mb-4"),
            ], style={"marginBottom": "1.5rem"})
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Hr(style={
                "borderColor": "#3498db",
                "borderWidth": "3px",
                "width": "50%",
                "margin": "0 auto 2rem auto",
            })
        ])
    ]),
    

    dbc.Row([
        # Card 1 - Mapa de Imunização
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-map-marked-alt fa-3x mb-3",
                               style={"color": "#3498db"}),
                        html.H4("Mapa de imunização",
                                className="card-title text-center mb-3",
                                style={"color": "#2c3e50"}),
                        html.P("Visualize a distribuição geográfica das vacinações por escola, "
                               "com filtros por ano, tipo de unidade, modalidade e tipo de vacina.",
                               className="card-text text-center mb-4",
                               style={"color": "#7f8c8d"}),
                    ], className="text-center"),
                    dbc.Button("Acessar Mapa",
                              href="/saude/vacinas",  # Ajustado o path
                              color="primary",
                              size="lg",
                              className="w-100 mt-auto"),
                ], className="d-flex flex-column")
            ], style={
                "height": "100%",
                "border": "none",
                "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                "transition": "transform 0.3s ease-in-out",
            }, className="h-100")
        ], width=6, className="mb-4"),
        
        # Card 2 - Cobertura vacinal
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-database fa-3x mb-3",
                               style={"color": "#27ae60"}),
                        html.H4("Cobertura vacinal",
                                className="card-title text-center mb-3",
                                style={"color": "#2c3e50"}),
                        html.P("Visualize a cobertura vacinal de cada vacina, com filtros por ano, tipo de unidade, modalidade e tipo de vacina.",
                               className="card-text text-center mb-4",
                               style={"color": "#7f8c8d"}),
                    ], className="text-center"),
                    dbc.Button("Acessar Cobertura",
                              href="/saude/cobertura",  # Ajustado o path
                              color="primary",
                              size="lg",
                              className="w-100 mt-auto"),
                ], className="d-flex flex-column")
            ], style={
                "height": "100%",
                "border": "none",
                "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                "transition": "transform 0.3s ease-in-out",
            }, className="h-100")
        ], width=6, className="mb-4"),
    ]),
    
    dbc.Row([
        # Card 3 - Acompanhamento
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-database fa-3x mb-3",
                               style={"color": "#27ae60"}),
                        html.H4("Acompanhamento",
                                className="card-title text-center mb-3",
                                style={"color": "#2c3e50"}),
                        html.P("Tabela de acompanhamento",
                               className="card-text text-center mb-4",
                               style={"color": "#7f8c8d"}),
                    ], className="text-center"),
                    dbc.Button("Acessar acompanhamento",
                              href="/saude/acompanhamento",  # Ajustado o path
                              color="primary",
                              size="lg",
                              className="w-100 mt-auto"),
                ], className="d-flex flex-column")
            ], style={
                "height": "100%",
                "border": "none",
                "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                "transition": "transform 0.3s ease-in-out",
            }, className="h-100")
        ], width=6, className="mb-4"),

        # Card 4 - Sobre os Dados
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-database fa-3x mb-3",
                               style={"color": "#27ae60"}),
                        html.H4("Sobre os dados",
                                className="card-title text-center mb-3",
                                style={"color": "#2c3e50"}),
                        html.P("Conheça as fontes de dados, metodologias e informações técnicas "
                               "utilizadas neste painel de monitoramento.",
                               className="card-text text-center mb-4",
                               style={"color": "#7f8c8d"}),
                    ], className="text-center"),
                    dbc.Button("Ver documentação",
                              href="/saude/sobre",  # Ajustado o path
                              color="info",
                              size="lg",
                              className="w-100 mt-auto"),
                ], className="d-flex flex-column")
            ], style={
                "height": "100%",
                "border": "none",
                "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                "transition": "transform 0.3s ease-in-out",
            }, className="h-100")
        ], width=6, className="mb-4"),
    ])
], fluid=True, style={"paddingTop": "2rem", "paddingBottom": "2rem"})

# Layout padrão da página
layout = saude_home_layout