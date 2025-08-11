from dash import html, register_page, dcc
import dash_bootstrap_components as dbc

# Registrar a página com um path específico
register_page(
    __name__,
    path="/desenvolvimento_urbano/home",
    name="Início - Desenvolvimento Urbano",
)


des_urbano_home_layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "DESENVOLVIMENTO URBANO",
                                    className="text-center mb-3",
                                    style={"color": "#34495e"},
                                ),
                            ],
                            style={"marginBottom": "1.5rem"},
                        )
                    ]
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Hr(
                            style={
                                "borderColor": "#3498db",
                                "borderWidth": "3px",
                                "width": "50%",
                                "margin": "0 auto 2rem auto",
                            }
                        )
                    ]
                )
            ]
        ),
        dbc.Row(
            [
                # Card 1 - Mapa de Zoneamento
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            [
                                                html.I(
                                                    className="fas fa-map-marked-alt fa-3x mb-3",
                                                    style={"color": "#3498db"},
                                                ),
                                                html.H4(
                                                    "Mapa de zoneamento",
                                                    className="card-title text-center mb-3",
                                                    style={"color": "#2c3e50"},
                                                ),
                                                html.P(
                                                    "Mapa de zoneamento da cidade de Osasco.",
                                                    className="card-text text-center mb-4",
                                                    style={"color": "#7f8c8d"},
                                                ),
                                            ],
                                            className="text-center",
                                        ),
                                        dbc.Button(
                                            "Acessar Mapa de Zoneamento",
                                            href="/desenvolvimento_urbano/zoneamento",  # Ajustado o path
                                            color="primary",
                                            size="lg",
                                            className="w-100 mt-auto",
                                        ),
                                    ],
                                    className="d-flex flex-column",
                                )
                            ],
                            style={
                                "height": "100%",
                                "border": "none",
                                "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                                "transition": "transform 0.3s ease-in-out",
                            },
                            className="h-100",
                        )
                    ],
                    width=6,
                    className="mb-4",
                ),
                # Card 2 - Mapa de Loteamento
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            [
                                                html.I(
                                                    className="fas fa-database fa-3x mb-3",
                                                    style={"color": "#27ae60"},
                                                ),
                                                html.H4(
                                                    "Mapa de loteamento",
                                                    className="card-title text-center mb-3",
                                                    style={"color": "#2c3e50"},
                                                ),
                                                html.P(
                                                    "Mapa de loteamento da cidade de Osasco.",
                                                    className="card-text text-center mb-4",
                                                    style={"color": "#7f8c8d"},
                                                ),
                                            ],
                                            className="text-center",
                                        ),
                                        dbc.Button(
                                            "Acessar Mapa de Loteamento",
                                            href="/desenvolvimento_urbano/loteamento",  # Ajustado o path
                                            color="primary",
                                            size="lg",
                                            className="w-100 mt-auto",
                                        ),
                                    ],
                                    className="d-flex flex-column",
                                )
                            ],
                            style={
                                "height": "100%",
                                "border": "none",
                                "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                                "transition": "transform 0.3s ease-in-out",
                            },
                            className="h-100",
                        )
                    ],
                    width=6,
                    className="mb-4",
                ),
            ]
        ),
    ],
    fluid=True,
    style={"paddingTop": "2rem", "paddingBottom": "2rem"},
)

# Layout padrão da página
layout = des_urbano_home_layout
