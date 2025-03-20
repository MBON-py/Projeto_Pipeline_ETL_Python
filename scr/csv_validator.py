import streamlit as st
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import re
from datetime import datetime
from validador import RegistroGLP

def validar_csv(df):
    """Função para validar o CSV e retornar erros encontrados."""
    erros = []
    colunas_necessarias = [
        "Regiao - Sigla", "Estado - Sigla", "Municipio", "Revenda", "CNPJ da Revenda", "Nome da Rua",
        "Numero Rua", "Complemento", "Bairro", "Cep", "Produto", "Data da Coleta", "Valor de Venda",
        "Valor de Compra", "Unidade de Medida", "Bandeira"
    ]
    
    # Verifica se todas as colunas obrigatórias estão presentes
    for coluna in colunas_necessarias:
        if coluna not in df.columns:
            erros.append(f"Coluna obrigatória ausente: {coluna}")
    
    if not erros:
        # Validação dos dados
        for index, row in df.iterrows():
            if not isinstance(row["Regiao - Sigla"], str) or len(row["Regiao - Sigla"]) != 2:
                erros.append(f"Linha {index+1}: Regiao - Sigla inválida ({row['Regiao - Sigla']}).")
            
            if not isinstance(row["Estado - Sigla"], str) or len(row["Estado - Sigla"]) != 2:
                erros.append(f"Linha {index+1}: Estado - Sigla inválido ({row['Estado - Sigla']}).")
            
            if not isinstance(row["Municipio"], str) or row["Municipio"].strip() == "":
                erros.append(f"Linha {index+1}: Municipio não pode estar vazio.")
            
            if not re.match(r'\d{14}$', str(row["CNPJ da Revenda"])):
                erros.append(f"Linha {index+1}: CNPJ inválido ({row['CNPJ da Revenda']}).")
            
            if not re.match(r'\d{8}$', str(row["Cep"])):
                erros.append(f"Linha {index+1}: CEP inválido ({row['Cep']}).")
            
            if not isinstance(row["Produto"], str) or row["Produto"].strip() == "":
                erros.append(f"Linha {index+1}: Produto não pode estar vazio.")
            
            try:
                datetime.strptime(str(row["Data da Coleta"]), "%d/%m/%Y")
            except ValueError:
                erros.append(f"Linha {index+1}: Data da Coleta inválida ({row['Data da Coleta']}).")
            
            if not isinstance(row["Valor de Venda"], (int, float)) or row["Valor de Venda"] <= 0:
                erros.append(f"Linha {index+1}: Valor de Venda inválido ({row['Valor de Venda']}).")
            
            if not isinstance(row["Valor de Compra"], (int, float)) or row["Valor de Compra"] < 0:
                erros.append(f"Linha {index+1}: Valor de Compra inválido ({row['Valor de Compra']}).")
    
    return erros

def salvar_no_postgresql(df):
    """Função para salvar os dados validados no PostgreSQL."""
    try:
        engine = create_engine("postgresql://usuario:senha@localhost:5432/seu_banco")
        df.to_sql("usuarios", engine, if_exists="append", index=False)
        return True
    except Exception as e:
        st.error(f"Erro ao salvar no banco de dados: {e}")
        return False

# Interface Streamlit
st.title("Validador de Arquivo CSV")

uploaded_file = st.file_uploader("Carregar arquivo CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, delimiter=";", encoding="utf-8")
        st.write("### Visualização dos Dados:")
        st.dataframe(df)
        
        # Validação
        erros = validar_csv(df)
        
        if erros:
            st.error("Os seguintes erros foram encontrados:")
            for erro in erros:
                st.write(f"- {erro}")
        else:
            st.success("Nenhum erro encontrado. O arquivo está válido!")
            if st.button("Salvar no Banco de Dados"):
                if salvar_no_postgresql(df):
                    st.success("Dados salvos com sucesso no PostgreSQL!")
    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
