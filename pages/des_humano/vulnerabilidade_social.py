from dash import html, register_page, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import dash
from src.utils import create_info_popover

register_page(
    __name__,
    path="/desenvolvimento_humano/vulnerabilidade_social",
    name="Vulnerabilidade Social",
)

# Dados dos mapas
mapas_data = {
    "cadunico_pessoas": {
        "titulo": "Proporção de pessoas cadastradas no CadÚnico na população dos distritos",
        "iframe_src": "https://ozmundi.osasco.sp.gov.br/misc/cadunico_vulnerabilidades_cadastrados_distritos/",
        "info_id": "info-vulnerabilidade_cadunico_pessoas",
        "info_text": "Proporção de pessoas cadastradas no CadÚnico na população dos distritos"
    },
    "cadunico_pobreza": {
        "titulo": "Proporção de pessoas cadastradas no CadÚnico em situação de pobreza na população dos distritos",
        "iframe_src": "https://ozmundi.osasco.sp.gov.br/misc/cadunico_vulnerabilidades_pobreza/",
        "info_id": "info-vulnerabilidade_cadunico_pobreza",
        "info_text": "Proporção de pessoas cadastradas no CadÚnico em situação de pobreza na população dos distritos"
    },
    "bolsafamilia_pessoas": {
        "titulo": "Proporção de pessoas beneficiárias do Bolsa Família na população dos distritos",
        "iframe_src": "https://ozmundi.osasco.sp.gov.br/misc/cadunico_vulnerabilidades_pbf/",
        "info_id": "info-vulnerabilidade_bolsafamilia_pessoas",
        "info_text": "Proporção de pessoas beneficiárias do Bolsa Família na população dos distritos"
    },
    "indice_distritos": {
        "titulo": "Índice de vulnerabilidade nos diversos distritos do município de Osasco",
        "iframe_src": "https://ozmundi.osasco.sp.gov.br/misc/cadunico_vulnerabilidades_distritos/",
        "info_id": "info-vulnerabilidade_indice_distritos",
        "info_text": "Índice de vulnerabilidade nos diversos distritos do município de Osasco"
    },
    "indice_cras": {
        "titulo": "Índice de vulnerabilidade por território de abrangência dos CRAS",
        "iframe_src": "https://ozmundi.osasco.sp.gov.br/misc/indice_de_vulnerabilidade_cras/",
        "info_id": "info-vulnerabilidade_indice_cras",
        "info_text": "Índice de vulnerabilidade por território de abrangência dos CRAS"
    }
}

layout = html.Div(
    [
        html.Br(),

        html.P("Navegue entre os mapas abaixo:", style={"text-align": "center"}),
        
        # Botões de navegação
        html.Div(
            [
                dbc.Button(
                    "CadÚnico - Pessoas cadastradas",
                    id="btn-cadunico_pessoas",
                    color="primary",
                    className="me-2 mb-2",
                    n_clicks=0
                ),
                dbc.Button(
                    "CadÚnico - Situação de pobreza",
                    id="btn-cadunico_pobreza",
                    color="primary",
                    className="me-2 mb-2",
                    n_clicks=0
                ),
                dbc.Button(
                    "Beneficiários Bolsa Família",
                    id="btn-bolsafamilia_pessoas",
                    color="primary",
                    className="me-2 mb-2",
                    n_clicks=0
                ),
                dbc.Button(
                    "Índice de vulnerabilidade - Distritos",
                    id="btn-indice_distritos",
                    color="primary",
                    className="me-2 mb-2",
                    n_clicks=0
                ),
                dbc.Button(
                    "Índice de vulnerabilidade - CRAS",
                    id="btn-indice_cras",
                    color="primary",
                    className="me-2 mb-2",
                    n_clicks=0
                ),
            ],
            className="d-flex flex-wrap justify-content-center",
            style={"marginBottom": "2rem"}
        ),
        
        # Container para o mapa selecionado
        html.Div(
            id="mapa-container",
            style={"minHeight": "1000px"}
        ),
        
        # Store para controlar qual mapa está ativo
        dcc.Store(id="mapa-ativo", data="cadunico_pessoas")
    ]
)

@callback(
    Output("mapa-container", "children"),
    Output("mapa-ativo", "data"),
    [Input(f"btn-{mapa_id}", "n_clicks") for mapa_id in mapas_data.keys()],
    prevent_initial_call=False
)
def atualizar_mapa(*n_clicks):
    # Determinar qual botão foi clicado
    ctx = dash.callback_context
    if not ctx.triggered:
        # Se nenhum botão foi clicado, mostrar o primeiro mapa por padrão
        mapa_id = "cadunico_pessoas"
    else:
        # Extrair o ID do mapa do ID do botão clicado
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        mapa_id = button_id.replace("btn-", "")
    
    # Obter dados do mapa selecionado
    mapa_data = mapas_data[mapa_id]
    
    # Criar o conteúdo do mapa
    mapa_content = html.Div(
        [
            html.H4(
                mapa_data["titulo"],
                id=f"vulnerabilidade_{mapa_id}",
            ),
            html.P(
                [
                    "Fonte: ",
                    html.A(
                        "OzMundi",
                        href="https://ozmundi.osasco.sp.gov.br/forms/login.php",
                        target="_blank",
                    ),
                ]
            ),
            create_info_popover(
                mapa_data["info_id"],
                mapa_data["info_text"],
            ),
            html.Iframe(
                src=mapa_data["iframe_src"],
                style={
                    "width": "100%",
                    "height": "1000px",
                    "border": "none",
                },
            ),
        ],
        className="section-container",
    )
    
    return mapa_content, mapa_id

@callback(
    [Output(f"btn-{mapa_id}", "color") for mapa_id in mapas_data.keys()],
    Input("mapa-ativo", "data")
)
def atualizar_botoes_ativos(mapa_ativo):
    # Retornar cores dos botões baseado no mapa ativo
    cores = []
    for mapa_id in mapas_data.keys():
        if mapa_id == mapa_ativo:
            cores.append("success")  # Botão ativo em verde
        else:
            cores.append("primary")  # Botões inativos em azul
    return cores