from dash import html, register_page, dcc
import dash_bootstrap_components as dbc

# Registrar a página com um path específico
register_page(
    __name__,
    path="/desenvolvimento_humano/home",
    name="Início - Desenvolvimento Humano",
)


des_humano_home_layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "DESENVOLVIMENTO HUMANO",
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
                # Card 1 - Cad Unico
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
                                                    "Cadastro Único para Programas Sociais",
                                                    className="card-title text-center mb-3",
                                                    style={"color": "#2c3e50"},
                                                ),
                                                html.P(
                                                    "O Cadastro Único proporciona uma visão abrangente da parcela mais vulnerável da população brasileira, permitindo que os governos em todos os níveis saibam quem são essas famílias, onde vivem, suas condições de vida e suas necessidades.",
                                                    className="card-text text-center mb-4",
                                                    style={"color": "#7f8c8d"},
                                                ),
                                            ],
                                            className="text-center",
                                        ),
                                        dbc.Button(
                                            "Acessar dados do Cadastro Único",
                                            href="/desenvolvimento_humano/cad_unico",  # Ajustado o path
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
                # Card 2 - Bolsa Familia
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
                                                    "Programa Bolsa Família",
                                                    className="card-title text-center mb-3",
                                                    style={"color": "#2c3e50"},
                                                ),
                                                html.P(
                                                    "O Programa Bolsa Família é um programa de transferência de renda que tem como objetivo reduzir a pobreza e aumentar a renda das famílias mais vulneráveis.",
                                                    className="card-text text-center mb-4",
                                                    style={"color": "#7f8c8d"},
                                                ),
                                            ],
                                            className="text-center",
                                        ),
                                        dbc.Button(
                                            "Acessar dados do Programa Bolsa Família",
                                            href="/desenvolvimento_humano/bolsa_familia",  # Ajustado o path
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
        # Card 3 - Mapas de vulnerabilidade social
        dbc.Row(
            [
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
                                                    "Mapas de vulnerabilidade social",
                                                    className="card-title text-center mb-3",
                                                    style={"color": "#2c3e50"},
                                                ),
                                                html.P(
                                                    "Mapas de vulnerabilidade social do OzMundi.",
                                                    className="card-text text-center mb-4",
                                                    style={"color": "#7f8c8d"},
                                                ),
                                            ],
                                            className="text-center",
                                        ),
                                        dbc.Button(
                                            "Acessar mapas de vulnerabilidade social",
                                            href="/desenvolvimento_humano/vulnerabilidade_social",  # Ajustado o path
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
layout = des_humano_home_layout
