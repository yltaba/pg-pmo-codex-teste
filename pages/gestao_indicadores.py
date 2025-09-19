from dash import html, register_page, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

register_page(__name__, path="/gestao_indicadores", name="Gestão de indicadores")

# Dados dos visuais e indicadores organizados por eixos
DADOS_VISUAIS = {
    "Desenvolvimento Econômico": {
        "PIB": {
            "visuais": [
                {
                    "nome": "PIB (em R$ de 2021)",
                    "tipo": "Gráfico de Barras",
                    "fonte": "IBGE",
                    "status": "Ativo",
                    "descricao": "Evolução do PIB por categoria econômica ao longo dos anos",
                    "metodo_calculo": "Valor adicionado bruto a preços de mercado",
                    "periodicidade_atualizacao": "Anual",
                },
                {
                    "nome": "PIB per capita (em R$ de 2021)",
                    "tipo": "Gráfico de Linha",
                    "fonte": "IBGE",
                    "status": "Ativo",
                    "descricao": "Evolução do PIB per capita de Osasco comparado com outros municípios",
                    "metodo_calculo": "PIB do município dividido pela população residente no mesmo ano",
                    "periodicidade_atualizacao": "Anual",
                },
                {
                    "nome": "Participação do PIB municipal no Estado de São Paulo",
                    "tipo": "Gráfico de Linha",
                    "fonte": "IBGE",
                    "status": "Ativo",
                    "descricao": "Participação percentual de Osasco no PIB do Estado de São Paulo",
                    "metodo_calculo": "PIB do município dividido pelo PIB total do Estado de São Paulo",
                    "periodicidade_atualizacao": "Anual",
                },
            ],
            "indicadores": [
                {
                    "nome": "PIB 2021",
                    "tipo": "Card",
                    "fonte": "IBGE",
                    "status": "Ativo",
                    "descricao": "Valor do PIB em 2021",
                    "metodo_calculo": "Valor adicionado bruto a preços de mercado",
                    "periodicidade_atualizacao": "Anual",
                },
                {
                    "nome": "Variação PIB",
                    "tipo": "Card",
                    "fonte": "IBGE",
                    "status": "Ativo",
                    "descricao": "Variação percentual do PIB entre períodos",
                    "metodo_calculo": "Variação % do PIB do município comparado com o período anterior",
                    "periodicidade_atualizacao": "Anual",
                },
                {
                    "nome": "PIB per capita 2021",
                    "tipo": "Card",
                    "fonte": "IBGE",
                    "status": "Ativo",
                    "descricao": "Valor do PIB per capita em 2021",
                    "metodo_calculo": "PIB do município dividido pela sua população total",
                    "periodicidade_atualizacao": "Anual",
                },
                {
                    "nome": "População em 2021",
                    "tipo": "Card",
                    "fonte": "IBGE",
                    "status": "Ativo",
                    "descricao": "População estimada em 2021",
                    "metodo_calculo": "População residente estimada pelo IBGE",
                    "periodicidade_atualizacao": "Anual",
                },
                {
                    "nome": "PIB de Osasco / PIB SP em 2021",
                    "tipo": "Card",
                    "fonte": "IBGE",
                    "status": "Ativo",
                    "descricao": "Proporção do PIB de Osasco sobre o PIB do Estado de São Paulo em 2021",
                    "metodo_calculo": "PIB do município dividido pelo PIB total do Estado de São Paulo",
                    "periodicidade_atualizacao": "Anual",
                },
            ],
        },
        "Empresas": {
            "visuais": [
                {
                    "nome": "Abertura e encerramento de empresas computadas pelo SIGT.",
                    "tipo": "Gráfico de Barras Agrupadas",
                    "fonte": "SIGT - Prefeitura de Osasco",
                    "status": "Ativo",
                    "descricao": "Evolução da abertura e encerramento de empresas por atividade econômica",
                    "metodo_calculo": "Contagem de eventos de abertura e encerramento de empresas registradas no SIGT",
                    "periodicidade_atualizacao": "Semanal",
                },
                {
                    "nome": "Porte das empresas de Osasco",
                    "tipo": "Gráfico de Barras",
                    "fonte": "RAIS - Ministério do Trabalho",
                    "status": "Ativo",
                    "descricao": "Distribuição de estabelecimentos por tamanho e seção CNAE",
                    "metodo_calculo": "Contagem de estabelecimentos ativos no município, classificados por porte, de acordo com a RAIS Estabelecimentos",
                    "periodicidade_atualizacao": "Semanal",
                },
            ],
            "indicadores": [
                {
                    "nome": "Saldo de Empresas 2025",
                    "tipo": "Card",
                    "fonte": "SIGT - Prefeitura de Osasco",
                    "status": "Ativo",
                    "descricao": "Diferença entre empresas abertas e encerradas",
                    "metodo_calculo": "Subtração entre o número de empresas abertas e o número de empresas encerradas em determinado período",
                    "periodicidade_atualizacao": "Semanal",
                }
            ],
        },
    },
    "Trabalho e Renda": {
        "Emprego Formal": {
            "visuais": [
                {
                    "nome": "Estoque de postos de trabalho por ano",
                    "tipo": "Gráfico de área",
                    "fonte": "RAIS - Ministério do Trabalho",
                    "status": "Ativo",
                    "descricao": "Evolução dos vínculos empregatícios ativos por seção CNAE",
                    "metodo_calculo": "Contagem de vínculos empregatícios ativos, conforme registros da RAIS",
                    "periodicidade_atualizacao": "Anual",
                },
                {
                    "nome": "Saldo de movimentações por ano",
                    "tipo": "Gráfico de linha",
                    "fonte": "CAGED - Ministério do Trabalho",
                    "status": "Ativo",
                    "descricao": "Admissões, desligamentos e saldo de movimentações por seção CNAE",
                    "metodo_calculo": "Total de admissões menos total de desligamentos",
                    "periodicidade_atualizacao": "Mensal",
                },
                {
                    "nome": "Saldo de postos de trabalho por Seção da CNAE",
                    "tipo": "Gráfico de barras",
                    "fonte": "CAGED - Ministério do Trabalho",
                    "status": "Ativo",
                    "descricao": "Distribuição dos empregados por Seção da CNAE",
                    "metodo_calculo": "Total de admissões menos total de desligamentos, agregados por seção da CNAE",
                    "periodicidade_atualizacao": "Mensal",
                },
                {
                    "nome": "Saldo de postos de trabalho por idade",
                    "tipo": "Gráfico de barras",
                    "fonte": "CAGED - Ministério do Trabalho",
                    "status": "Ativo",
                    "descricao": "Saldo de postos de trabalho por idade desde 2007.",
                    "metodo_calculo": "Total de admissões menos total de desligamentos, agregados por faixa etária",
                    "periodicidade_atualizacao": "Mensal",
                },
                {
                    "nome": "Evolução da média/mediana salarial de admissões e demissões",
                    "tipo": "Gráfico de barras",
                    "fonte": "CAGED - Ministério do Trabalho",
                    "status": "Ativo",
                    "descricao": "Evolução da média/mediana salarial de admissões e demissões por seção da CNAE",
                    "metodo_calculo": "Soma dos salários registrados dividida pelo número total de vínculos",
                    "periodicidade_atualizacao": "Mensal",
                },
                {
                    "nome": "Evolução da média/mediana de idade das admissões e demissões",
                    "tipo": "Gráfico de barras",
                    "fonte": "CAGED - Ministério do Trabalho",
                    "status": "Ativo",
                    "descricao": "Evolução da média/mediana de idade das admissões e demissões por seção da CNAE",
                    "metodo_calculo": "Soma das idades registradas dividida pelo número total de vínculos",
                    "periodicidade_atualizacao": "Mensal",
                },
            ],
            "indicadores": [
                {
                    "nome": "Postos de trabalho em 2024",
                    "tipo": "Card",
                    "fonte": "RAIS - Ministério do Trabalho",
                    "status": "Ativo",
                    "descricao": "Total de postos de trabalho em 2024",
                    "metodo_calculo": "Contagem de vínculos empregatícios ativos, conforme registros da RAIS",
                    "periodicidade_atualizacao": "Anual",
                },
                {
                    "nome": "Variação do estoque de postos de trabalho entre 2023 e 2024",
                    "tipo": "Card",
                    "fonte": "RAIS - Ministério do Trabalho",
                    "status": "Ativo",
                    "descricao": "Variação percentual do estoque de postos de trabalho entre 2023 e 2024",
                    "metodo_calculo": "Variação % do estoque de postos de trabalho do município comparado com o período anterior",
                    "periodicidade_atualizacao": "Anual",
                },
                {
                    "nome": "Saldo de movimentações em 2025",
                    "tipo": "Card",
                    "fonte": "CAGED - Ministério do Trabalho",
                    "status": "Ativo",
                    "descricao": "Saldo de admissões menos desligamentos em 2025",
                    "metodo_calculo": "Total de admissões menos total de desligamentos",
                    "periodicidade_atualizacao": "Mensal",
                },
                {
                    "nome": "Variação do saldo de movimentações entre 2024 e 2025",
                    "tipo": "Card",
                    "fonte": "CAGED - Ministério do Trabalho",
                    "status": "Ativo",
                    "descricao": "Variação percentual do saldo de movimentações entre 2024 e 2025",
                    "metodo_calculo": "Variação % do saldo de movimentações do município comparado com o período anterior",
                    "periodicidade_atualizacao": "Mensal",
                },
            ],
        }
    },
    "Desenvolvimento Humano": {
        "Cadastro Único": {
            "visuais": [
                {
                    "nome": "Distribuição acumulada da renda per capita familiar",
                    "tipo": "Gráfico de função de distribuição cumulativa",
                    "fonte": "CadÚnico",
                    "status": "Ativo",
                    "descricao": "Distribuição acumulada da renda per capita familiar",
                    "metodo_calculo": "",
                    "periodicidade_atualizacao": "Mensal",
                },
                {
                    "nome": "Evolução de cadastros no CadÚnico por ano e forma de coleta",
                    "tipo": "Gráfico de barras",
                    "fonte": "CadÚnico",
                    "status": "Ativo",
                    "descricao": "Evolução de cadastros no CadÚnico por ano e forma de coleta",
                    "metodo_calculo": "Contagem dos cadastros registrados no CadÚnico, organizados por ano e por forma de coleta",
                    "periodicidade_atualizacao": "Mensal",
                },
                {
                    "nome": "Pessoas cadastradas no CadÚnico por sexo biológico",
                    "tipo": "Gráfico de rosca",
                    "fonte": "CadÚnico",
                    "status": "Ativo",
                    "descricao": "Pessoas cadastradas no CadÚnico por sexo biológico",
                    "metodo_calculo": "Contagem de pessoas cadastradas no CadÚnico, agrupadas por sexo biológico",
                    "periodicidade_atualizacao": "Mensal",
                },
                {
                    "nome": "Pessoas cadastradas no CadÚnico por parentesco",
                    "tipo": "Gráfico de barras horizontais",
                    "fonte": "CadÚnico",
                    "status": "Ativo",
                    "descricao": "Pessoas cadastradas no CadÚnico por parentesco",
                    "metodo_calculo": "Contagem de pessoas cadastradas no CadÚnico, agrupadas por grau de parentesco.",
                    "periodicidade_atualizacao": "Mensal",
                },
                {
                    "nome": "Visão geral dos bairros de Osasco no CadÚnico",
                    "tipo": "Tabela interativa",
                    "fonte": "CadÚnico",
                    "status": "Ativo",
                    "descricao": "Visão geral dos bairros de Osasco no CadÚnico",
                    "metodo_calculo": "Contagem de pessoas cadastradas no CadÚnico por bairro.",
                    "periodicidade_atualizacao": "Mensal",
                },
            ],
            "indicadores": [
                {
                    "nome": "Famílias cadastradas",
                    "tipo": "Card",
                    "fonte": "CadÚnico",
                    "status": "Ativo",
                    "descricao": "Total de famílias com cadastro ativo e atualizado",
                    "metodo_calculo": "Contagem de famílias cadastradas no CadÚnico",
                    "periodicidade_atualizacao": "Mensal",
                },
                {
                    "nome": "Novas famílias cadastradas (2025)",
                    "tipo": "Card",
                    "fonte": "CadÚnico",
                    "status": "Ativo",
                    "descricao": "Famílias cadastradas em 2025",
                    "metodo_calculo": "Contagem de famílias cadastradas no CadÚnico no ano de 2025",
                    "periodicidade_atualizacao": "Mensal",
                },
                {
                    "nome": "Renda per capita",
                    "tipo": "Card",
                    "fonte": "CadÚnico",
                    "status": "Ativo",
                    "descricao": "Média da renda per capita das famílias cadastradas",
                    "metodo_calculo": "Soma das rendas per capita de todas as famílias cadastradas no CadÚnico, dividida pelo número total de famílias cadastradas",
                    "periodicidade_atualizacao": "Mensal",
                },
                {
                    "nome": "Pessoas por família",
                    "tipo": "Card",
                    "fonte": "CadÚnico",
                    "status": "Ativo",
                    "descricao": "Média de pessoas por família cadastrada",
                    "metodo_calculo": "Soma das pessoas de todas as famílias cadastradas no CadÚnico, dividida pelo número total de famílias cadastradas",
                    "periodicidade_atualizacao": "Mensal",
                },
                {
                    "nome": "Pessoas por domicílio",
                    "tipo": "Card",
                    "fonte": "CadÚnico",
                    "status": "Ativo",
                    "descricao": "Média de pessoas por domicílio",
                    "metodo_calculo": "Soma das pessoas de todas as famílias cadastradas no CadÚnico, dividida pelo número total de domicílios cadastrados",
                    "periodicidade_atualizacao": "Mensal",
                },
                {
                    "nome": "Cômodos por domicílio",
                    "tipo": "Card",
                    "fonte": "CadÚnico",
                    "status": "Ativo",
                    "descricao": "Média de cômodos por domicílio",
                    "metodo_calculo": "Soma dos cômodos de todos os domicílios cadastrados no CadÚnico, dividida pelo número total de domicílios cadastrados",
                    "periodicidade_atualizacao": "Mensal",
                },
                {
                    "nome": "Domicílios sem água canalizada",
                    "tipo": "Card",
                    "fonte": "CadÚnico",
                    "status": "Ativo",
                    "descricao": "Contagem de domicílios sem água canalizada",
                    "metodo_calculo": "Contagem de domicílios sem água canalizada",
                    "periodicidade_atualizacao": "Mensal",
                },
                {
                    "nome": "Domicílios sem rede de esgoto",
                    "tipo": "Card",
                    "fonte": "CadÚnico",
                    "status": "Ativo",
                    "descricao": "Contagem de domicílios sem rede de esgoto",
                    "metodo_calculo": "Contagem de domicílios sem rede de esgoto",
                    "periodicidade_atualizacao": "Mensal",
                },
            ],
        },
        "Bolsa Família": {
            "visuais": [
                {
                    "nome": "Número de famílias beneficiadas pelo PBF",
                    "tipo": "Gráfico de linha",
                    "fonte": "Portal da Transparência - CGU",
                    "status": "Ativo",
                    "descricao": "Evolução do número de famílias beneficiadas pelo PBF",
                    "metodo_calculo": "Contagem de responsáveis familiares (RF) beneficiados pelo PBF no município",
                    "periodicidade_atualizacao": "Mensal",
                },
                {
                    "nome": "Valor total dos repasses do PBF",
                    "tipo": "Gráfico de linha",
                    "fonte": "Portal da Transparência - CGU",
                    "status": "Ativo",
                    "descricao": "Evolução do valor total dos repasses do PBF",
                    "metodo_calculo": "Soma de todos os valores repassados pelo PBF a beneficiários do município no mês de referência",
                    "periodicidade_atualizacao": "Mensal",
                },
                {
                    "nome": "Média do valor dos repasses do PBF",
                    "tipo": "Gráfico de linha",
                    "fonte": "Portal da Transparência - CGU",
                    "status": "Ativo",
                    "descricao": "Evolução da média dos valores dos repasses do PBF",
                    "metodo_calculo": "Soma de todos os valores repassados pelo PBF no município, em reais, dividida pelo número de famílias beneficiadas no mesmo mês",
                    "periodicidade_atualizacao": "Mensal",
                },
            ]
        },
        "Vulnerabilidade Social": {
            "visuais": [
                {
                    "nome": "Proporção de pessoas cadastradas no CadÚnico na população dos distritos",
                    "tipo": "Mapa interativo",
                    "fonte": "OzMundi",
                    "status": "Ativo",
                    "descricao": "Proporção de pessoas cadastradas no CadÚnico na população dos distritos",
                    "metodo_calculo": "",
                    "periodicidade_atualizacao": "Mensal",
                },
                {
                    "nome": "Proporção de pessoas cadastradas no CadÚnico em situação de pobreza na população dos distritos",
                    "tipo": "Mapa interativo",
                    "fonte": "OzMundi",
                    "status": "Ativo",
                    "descricao": "Proporção de pessoas cadastradas no CadÚnico em situação de pobreza na população dos distritos",
                    "metodo_calculo": "",
                    "periodicidade_atualizacao": "Mensal",
                },
                {
                    "nome": "Proporção de pessoas beneficiárias do Bolsa Família na população dos distritos",
                    "tipo": "Mapa interativo",
                    "fonte": "OzMundi",
                    "status": "Ativo",
                    "descricao": "Proporção de pessoas beneficiárias do Bolsa Família na população dos distritos",
                    "metodo_calculo": "",
                    "periodicidade_atualizacao": "Mensal",
                },
                {
                    "nome": "Índice de vulnerabilidade nos diversos distritos do município de Osasco",
                    "tipo": "Mapa interativo",
                    "fonte": "OzMundi",
                    "status": "Ativo",
                    "descricao": "Índice de vulnerabilidade nos diversos distritos do município de Osasco",
                    "metodo_calculo": "",
                    "periodicidade_atualizacao": "Mensal",
                },
                {
                    "nome": "Índice de vulnerabilidade por território de abrangência dos CRAS",
                    "tipo": "Mapa interativo",
                    "fonte": "OzMundi",
                    "status": "Ativo",
                    "descricao": "Índice de vulnerabilidade por território de abrangência dos CRAS",
                    "metodo_calculo": "",
                    "periodicidade_atualizacao": "Mensal",
                },
            ],
        },
    },
    "Saúde": {
        "Mapa de imunização": {
            "visuais": [
                {
                    "nome": "Mapa de imunização",
                    "tipo": "Mapa Interativo",
                    "fonte": "SiSS",
                    "status": "Ativo",
                    "descricao": "Mapa de imunização",
                    "metodo_calculo": "",
                    "periodicidade_atualizacao": "Mensal",
                },
            ],
        },
        "Acompanhamento": {
            "visuais": [
                {
                    "nome": "Acompanhamento de imunizações",
                    "tipo": "Tabela interativa",
                    "fonte": "SiSS",
                    "status": "Ativo",
                    "descricao": "Acompanhamento de imunizações",
                    "metodo_calculo": "",
                    "periodicidade_atualizacao": "Mensal",
                },
                {
                    "nome": "Cobertura vacinal",
                    "tipo": "Card",
                    "fonte": "SiSS",
                    "status": "Ativo",
                    "descricao": "Cobertura vacinal",
                    "metodo_calculo": "",
                    "periodicidade_atualizacao": "Mensal",
                },
            ]
        },
    },
    "Receita Própria": {
        "Tributos": {
            "visuais": [
                {
                    "nome": "Receita total arrecadada por ano",
                    "tipo": "Gráfico de barras",
                    "fonte": "SIGT - Prefeitura de Osasco",
                    "status": "Ativo",
                    "descricao": "Receita total arrecadada por ano",
                    "metodo_calculo": "Soma de todos os valores pagos referentes a IPTU, ISS, ITBI e demais tributos municipais",
                    "periodicidade_atualizacao": "Semanal",
                },
                {
                    "nome": "Receita anual por categoria tributária (2023-2025)",
                    "tipo": "Gráfico de barras",
                    "fonte": "SIGT - Prefeitura de Osasco",
                    "status": "Ativo",
                    "descricao": "Receita tributária por categoria",
                    "metodo_calculo": "Soma de todos os valores pagos referentes a IPTU, ISS, ITBI e demais tributos municipais, organizados por categoria tributária",
                    "periodicidade_atualizacao": "Semanal",
                },
                {
                    "nome": "Receita anual por subcategoria tributária (2023-2025)",
                    "tipo": "Gráfico de barras horizontal",
                    "fonte": "SIGT - Prefeitura de Osasco",
                    "status": "Ativo",
                    "descricao": "Receita tributária por subcategoria",
                    "metodo_calculo": "Soma de todos os valores pagos referentes a IPTU, ISS, ITBI e demais tributos municipais, organizados por subcategoria tributária",
                    "periodicidade_atualizacao": "Semanal",
                },
                {
                    "nome": "Inscrições imobiliárias, valor venal e incidência de tributo por ano",
                    "tipo": "Tabela interativa",
                    "fonte": "SIGT - Prefeitura de Osasco",
                    "status": "Ativo",
                    "descricao": "Inscrições imobiliárias, valor venal e incidência de tributo por ano",
                    "metodo_calculo": "Soma total das inscrições imobiliárias, do valor venal e da incidência tributária, agregadas por ano",
                    "periodicidade_atualizacao": "Semanal",
                },
            ]
        }
    },
    "Desenvolvimento Urbano": {
        "Zoneamento": {
            "visuais": [
                {
                    "nome": "Mapa de Zoneamento",
                    "tipo": "Mapa Interativo",
                    "fonte": "OzMundi",
                    "status": "Ativo",
                    "descricao": "Mapa interativo do zoneamento urbano de Osasco",
                    "metodo_calculo": "",
                    "periodicidade_atualizacao": "Anual",
                }
            ],
        },
        "Loteamento": {
            "visuais": [
                {
                    "nome": "Mapa de Loteamentos",
                    "tipo": "Mapa Interativo",
                    "fonte": "OzMundi",
                    "status": "Ativo",
                    "descricao": "Mapa interativo dos loteamentos aprovados",
                    "metodo_calculo": "",
                    "periodicidade_atualizacao": "Anual",
                }
            ],
        },
    },
}


def criar_tabela_visuais():
    """Cria uma tabela com todos os visuais organizados"""
    dados_tabela = []

    for eixo, sub_eixos in DADOS_VISUAIS.items():
        for sub_eixo, categorias in sub_eixos.items():
            # Adiciona visuais
            if "visuais" in categorias:
                for visual in categorias["visuais"]:
                    dados_tabela.append(
                        {
                            "Eixo": eixo,
                            "Sub-eixo": sub_eixo,
                            "Tipo": "Visual",
                            "Nome": visual["nome"],
                            "Categoria": visual["tipo"],
                            "Fonte": visual["fonte"],
                            "Status": visual["status"],
                            "Periodicidade de atualização": visual["periodicidade_atualizacao"],
                            "Descrição": visual["descricao"],
                            "Método de cálculo": visual["metodo_calculo"],
                        }
                    )

            # Adiciona indicadores
            if "indicadores" in categorias:
                for indicador in categorias["indicadores"]:
                    dados_tabela.append(
                        {
                            "Eixo": eixo,
                            "Sub-eixo": sub_eixo,
                            "Tipo": "Indicador",
                            "Nome": indicador["nome"],
                            "Categoria": indicador["tipo"],
                            "Fonte": indicador["fonte"],
                            "Status": indicador["status"],
                            "Periodicidade de atualização": indicador["periodicidade_atualizacao"],
                            "Descrição": indicador["descricao"],
                            "Método de cálculo": indicador["metodo_calculo"],
                        }
                    )

    return dados_tabela


def criar_resumo_por_eixo():
    """Cria um resumo dos visuais e indicadores por eixo"""
    resumo = {}

    for eixo, sub_eixos in DADOS_VISUAIS.items():
        total_visuais = 0
        total_indicadores = 0
        ativos = 0
        em_desenvolvimento = 0

        for sub_eixo, categorias in sub_eixos.items():
            if "visuais" in categorias:
                total_visuais += len(categorias["visuais"])
                for visual in categorias["visuais"]:
                    if visual["status"] == "Ativo":
                        ativos += 1
                    elif visual["status"] == "Em Desenvolvimento":
                        em_desenvolvimento += 1

            if "indicadores" in categorias:
                total_indicadores += len(categorias["indicadores"])
                for indicador in categorias["indicadores"]:
                    if indicador["status"] == "Ativo":
                        ativos += 1
                    elif indicador["status"] == "Em Desenvolvimento":
                        em_desenvolvimento += 1

        resumo[eixo] = {
            "total_visuais": total_visuais,
            "total_indicadores": total_indicadores,
            "total": total_visuais + total_indicadores,
            "ativos": ativos,
            "em_desenvolvimento": em_desenvolvimento,
        }

    return resumo


# Criar dados para a tabela
dados_tabela = criar_tabela_visuais()
resumo_eixos = criar_resumo_por_eixo()

# Criar tabela
tabela_visuais = dash_table.DataTable(
    id="tabela-visuais",
    columns=[
        {"name": "Eixo", "id": "Eixo", "type": "text"},
        {"name": "Sub-eixo", "id": "Sub-eixo", "type": "text"},
        {"name": "Tipo", "id": "Tipo", "type": "text"},
        {"name": "Nome", "id": "Nome", "type": "text"},
        {"name": "Categoria", "id": "Categoria", "type": "text"},
        {"name": "Fonte", "id": "Fonte", "type": "text"},
        {"name": "Descrição", "id": "Descrição", "type": "text"},
        {"name": "Método de cálculo", "id": "Método de cálculo", "type": "text"},
        {"name": "Periodicidade de atualização", "id": "Periodicidade de atualização", "type": "text"},
        {"name": "Status", "id": "Status", "type": "text"},
    ],
    data=dados_tabela,
    filter_action="native",
    export_format="xlsx",
    export_headers="display",
    page_action="native",
    page_current=0,
    page_size=50,
    style_table={
        "overflowX": "auto",
        "overflowY": "auto",
        "maxHeight": "600px",
        "border": "thin lightgrey solid",
        "borderRadius": "8px",
        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
    },
    style_cell={
        "fontFamily": 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
        "textAlign": "left",
        "padding": "12px 15px",
        "backgroundColor": "white",
        "minWidth": "100px",
        "maxWidth": "300px",
        "overflow": "hidden",
        "textOverflow": "ellipsis",
        "whiteSpace": "normal",
        "height": "auto",
    },
    style_header={
        "backgroundColor": "#f8f9fa",
        "fontWeight": "bold",
        "border": "none",
        "borderBottom": "2px solid #dee2e6",
        "textAlign": "left",
        "padding": "12px 15px",
        "whiteSpace": "normal",
    },
    style_data_conditional=[
        {
            "if": {"column_id": "Status", "filter_query": "{Status} = 'Ativo'"},
            "color": "#28a745",
            "fontWeight": "bold",
        },
        {
            "if": {"column_id": "Status", "filter_query": "{Status} = 'Em Desenvolvimento'"},
            "color": "#fd7e14",
            "fontWeight": "bold",
        },
    ],
    tooltip_header={
        "Eixo": "Eixo principal do desenvolvimento",
        "Sub-eixo": "Subdivisão do eixo principal",
        "Tipo": "Tipo do item (Visual ou Indicador)",
        "Nome": "Nome do visual ou indicador",
        "Categoria": "Tipo de gráfico ou componente",
        "Fonte": "Fonte dos dados",
        "Status": "Status atual (Ativo ou Em Desenvolvimento)",
        "Descrição": "Descrição detalhada do visual/indicador",
        "Periodicidade de atualização": "Periodicidade de atualização dos dados",
        "Método de cálculo": "Método de cálculo dos dados",
    },
    tooltip_delay=0,
    tooltip_duration=-1,
    css=[
        {
            "selector": ".export::after",
            "rule": "content: 'Exportar Excel'; font-size: 12px;",
        },
        {
            "selector": ".export",
            "rule": "font-size: 0;",
        },
    ],
)


def criar_cards_resumo():
    """Cria cards com resumo dos eixos"""
    cards = []

    for eixo, dados in resumo_eixos.items():
        card = dbc.Card(
            dbc.CardBody(
                [
                    html.H5(eixo, className="card-title"),
                    html.Div(
                        [
                            html.P(f"Total: {dados['total']}", className="mb-1"),
                            html.P(
                                f"Visuais: {dados['total_visuais']}", className="mb-1"
                            ),
                            html.P(
                                f"Indicadores: {dados['total_indicadores']}",
                                className="mb-1",
                            ),
                            html.P(f"Ativos: {dados['ativos']}", className="mb-1"),
                            html.P(
                                f"Em desenvolvimento: {dados['em_desenvolvimento']}",
                                className="mb-0",
                            ),
                        ]
                    ),
                ]
            ),
            className="mb-3",
            style={"minHeight": "200px"},
        )
        cards.append(dbc.Col(card, width=4))

    return cards


# Layout da página
layout = html.Div(
    [
        html.Div(
            [
                html.H2("Gestão de indicadores", className="mb-4"),
                # Cards de resumo
                html.H4("Resumo por eixo", className="mb-3"),
                dbc.Row(criar_cards_resumo(), className="mb-3"),
                # Tabela completa
                html.H4("Catálogo completo de visuais e indicadores", className="mb-3"),
                tabela_visuais,
            ]
        )
    ]
)
