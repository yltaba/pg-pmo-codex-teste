from dash import html, register_page, dcc
import dash_bootstrap_components as dbc

# Registrar a página com um path específico
register_page(__name__, path="/desenvolvimento_economico/home", name="Início - Desenvolvimento Econômico")


des_economico_home_layout = dbc.Container([

    dbc.Row([
        dbc.Col([
            html.Div([
                html.H3("DESENVOLVIMENTO ECONÔMICO",
                        className="text-center mb-3",
                        style={"color": "#34495e"}),
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
        # Card 1 - Cad Unico
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-map-marked-alt fa-3x mb-3",
                               style={"color": "#3498db"}),
                        html.H4("PIB",
                                className="card-title text-center mb-3",
                                style={"color": "#2c3e50"}),
                        html.P("Produto Interno Bruto (PIB) da cidade de Osasco.",
                               className="card-text text-center mb-4",
                               style={"color": "#7f8c8d"}),
                    ], className="text-center"),
                    dbc.Button("Acessar dados do PIB",
                              href="/desenvolvimento_economico/pib",  # Ajustado o path
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
        
        # Card 2 - Bolsa Familia
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-database fa-3x mb-3",
                               style={"color": "#27ae60"}),
                        html.H4("Empresas",
                                className="card-title text-center mb-3",
                                style={"color": "#2c3e50"}),
                        html.P("Abertura e encerramento de empresas do SIGT.",
                               className="card-text text-center mb-4",
                               style={"color": "#7f8c8d"}),
                    ], className="text-center"),
                    dbc.Button("Acessar dados das Empresas",
                              href="/desenvolvimento_economico/empresas",  # Ajustado o path
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
], fluid=True, style={"paddingTop": "2rem", "paddingBottom": "2rem"})

# Layout padrão da página
layout = des_economico_home_layout