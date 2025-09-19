import pandas as pd
from src.config import DATA_PATH


def load_data():
    return {
        "rais_anual": pd.read_csv(DATA_PATH / "rais_anual.csv", sep=";"),
        "caged_saldo_anual": pd.read_csv(
            DATA_PATH / "caged_saldo_movimentacao_anual.csv", encoding="latin1", sep=";"
        ),
        "caged_saldo_secao": pd.read_csv(
            DATA_PATH / "caged_saldo_secao.csv", sep=";", encoding="latin1"
        ),
        "caged_saldo_idade": pd.read_csv(
            DATA_PATH / "caged_saldo_idade.csv", sep=";", encoding="latin1"
        ),
        "caged_media_idade": pd.read_csv(
            DATA_PATH / "caged_media_idade.csv", sep=";", encoding="latin1"
        ),
        "caged_media_salario": pd.read_csv(
            DATA_PATH / "caged_media_salario.csv", sep=";", encoding="latin1"
        ),
        "pib_por_categoria": pd.read_csv(
            DATA_PATH / "pib_por_categoria.csv", sep=";", encoding="latin1"
        ),
        "pib_participacao_sp": pd.read_csv(
            DATA_PATH / "pib_participacao_sp_munic_selecionados.csv",
            sep=";",
            encoding="latin1",
        ),
        "pib_per_capita": pd.read_csv(
            DATA_PATH / "pib_per_capita_munic_selecionados.csv",
            sep=";",
            encoding="latin1",
        ),
        "pbf_munic_selecionados": pd.read_csv(
            DATA_PATH / "pbf_munic_selecionados.csv", sep=";", encoding="latin1"
        ),
        "abertura_encerramento_empresas_cleaned": pd.read_csv(
            DATA_PATH / "tb_sigt_abertura_encerramento_empresas_cleaned.csv", sep=";"
        ),
        "cod_familiar_fam": pd.read_csv(DATA_PATH / "cod_familiar_fam.csv", sep=";"),
        "cod_familiar_fam_2025": pd.read_csv(
            DATA_PATH / "cod_familiar_fam_2025.csv", sep=";"
        ),
        "renda_per_capita_fam": pd.read_csv(
            DATA_PATH / "renda_per_capita_fam.csv", sep=";"
        ),
        "n_pessoas_fam": pd.read_csv(DATA_PATH / "n_pessoas_fam.csv", sep=";"),
        "escoa_sanitario_fam": pd.read_csv(
            DATA_PATH / "escoa_sanitario_fam.csv", sep=";"
        ),
        "agua_canalizada_fam": pd.read_csv(
            DATA_PATH / "agua_canalizada_fam.csv", sep=";"
        ),
        "qtd_comodos_domic_fam": pd.read_csv(
            DATA_PATH / "qtd_comodos_domic_fam.csv", sep=";"
        ),
        "sabe_ler_escrever_memb": pd.read_csv(
            DATA_PATH / "sabe_ler_escrever_memb.csv", sep=";"
        ),
        "sexo_pessoa": pd.read_csv(DATA_PATH / "sexo_pessoa.csv", sep=";"),
        "forma_coleta": pd.read_csv(DATA_PATH / "forma_coleta.csv", sep=";"),
        "parentesco": pd.read_csv(DATA_PATH / "parentesco.csv", sep=";"),
        "indicadores_bairros": pd.read_csv(
            DATA_PATH / "indicadores_bairros.csv", sep=";"
        ),
        "tb_sigt_receita_categ_tributo": pd.read_csv(
            DATA_PATH / "tb_sigt_receita_categ_tributo.csv", sep=";"
        ),
        "tb_sigt_valor_imovel_tributo": pd.read_csv(
            DATA_PATH / "valor_imovel_tributo.csv", sep=";"
        ),
        "rais_tamanho_estabelecimento": pd.read_csv(
            DATA_PATH / "gold_rais_tamanho_estabelecimento.csv", sep=";"
        ),
        "populacao_densidade": pd.read_csv(
            DATA_PATH / "densidade_pop_munic_selecionados.csv", sep=";", encoding="latin1"
        ),
    }
