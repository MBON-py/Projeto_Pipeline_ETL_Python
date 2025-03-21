import streamlit as st
import pandas as pd
from validador import ValidadorCSV  # Importa a classe de validação

def validar_csv(df):
    """Valida cada linha do CSV usando Pydantic e retorna erros encontrados."""
    erros = []
    dados_validados = []

    # Mapeia as colunas do CSV para as chaves do modelo Pydantic
    colunas_para_mapear = {
        "Regiao - Sigla": "regiao_sigla",
        "Estado - Sigla": "estado_sigla",
        "Municipio": "municipio",
        "Revenda": "revenda",
        "CNPJ da Revenda": "cnpj_revenda",
        "Nome da Rua": "nome_rua",
        "Numero Rua": "numero_rua",
        "Complemento": "complemento",
        "Bairro": "bairro",
        "Cep": "cep",
        "Produto": "produto",
        "Data da Coleta": "data_coleta",
        "Valor de Venda": "valor_venda",
        "Valor de Compra": "valor_compra",
        "Unidade de Medida": "unidade_medida",
        "Bandeira": "bandeira"
    }

    # Renomeia as colunas do DataFrame para corresponder às chaves do modelo
    df.rename(columns=colunas_para_mapear, inplace=True)

    # Remove linhas completamente vazias
    df.dropna(how="all", inplace=True)

    for index, row in df.iterrows():
        try:
            # Verifica se a linha está vazia ou nula
            if row.isnull().all():
                continue  # Ignora linhas completamente vazias

            # Converte os dados para dicionário e valida
            usuario_validado = ValidadorCSV.parse_obj(row.to_dict())
            dados_validados.append(usuario_validado)
        except Exception as e:
            erros.append(f"Linha {index + 1}: {str(e)}")

    return erros

# --- INTERFACE STREAMLIT ---
st.title("📂 Validador de Arquivo CSV")

uploaded_file = st.file_uploader("Carregar arquivo CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Lê o CSV com o separador de ponto e vírgula (;) e codificação utf-8
        df = pd.read_csv(uploaded_file, sep=";", dtype=str, encoding="utf-8")
        st.write("### 🔍 Visualização dos Dados:")
        st.dataframe(df)

        # --- Validação ---
        erros = validar_csv(df)

        if erros:
            st.error("⚠️ Foram encontrados os seguintes erros:")
            for erro in erros:
                st.write(f"- {erro}")
        else:
            st.success("✅ Nenhum erro encontrado! O arquivo está válido.")
            if st.button("💾 Salvar no Banco de Dados"):
                if salvar_no_postgresql(df):
                    st.success("🎉 Dados salvos com sucesso no PostgreSQL!")

    except Exception as e:
        st.error(f"❌ Erro ao processar o arquivo: {e}")