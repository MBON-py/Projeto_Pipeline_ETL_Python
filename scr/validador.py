from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import pandas as pd

class RegistroGLP(BaseModel):
    regiao_sigla: str = Field(..., min_length=1, max_length=2)
    estado_sigla: str = Field(..., min_length=2, max_length=2)
    municipio: str = Field(..., min_length=1)
    revenda: str = Field(..., min_length=1)
    cnpj_revenda: str = Field(..., regex=r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}")
    nome_rua: str = Field(..., min_length=1)
    numero_rua: Optional[str]
    complemento: Optional[str]
    bairro: str = Field(..., min_length=1)
    cep: str = Field(..., regex=r"\d{5}-\d{3}")
    produto: str = Field(..., min_length=1)
    data_coleta: datetime
    valor_venda: Optional[float]
    valor_compra: Optional[float]
    unidade_medida: str = Field(..., min_length=1)
    bandeira: str = Field(..., min_length=1)

def validar_dados(csv_path: str):
    df = pd.read_csv(csv_path, delimiter=';', engine='python', dtype=str)
    registros_validos = []
    erros = []
    
    for index, row in df.iterrows():
        try:
            registro = RegistroGLP(
                regiao_sigla=row['Regiao - Sigla'],
                estado_sigla=row['Estado - Sigla'],
                municipio=row['Municipio'],
                revenda=row['Revenda'],
                cnpj_revenda=row['CNPJ da Revenda'].strip(),
                nome_rua=row['Nome da Rua'],
                numero_rua=row.get('Numero Rua'),
                complemento=row.get('Complemento'),
                bairro=row['Bairro'],
                cep=row['Cep'],
                produto=row['Produto'],
                data_coleta=datetime.strptime(row['Data da Coleta'], "%d/%m/%Y"),
                valor_venda=float(row['Valor de Venda'].replace(',', '.')) if row['Valor de Venda'] else None,
                valor_compra=float(row['Valor de Compra'].replace(',', '.')) if row['Valor de Compra'] else None,
                unidade_medida=row['Unidade de Medida'],
                bandeira=row['Bandeira']
            )
            registros_validos.append(registro)
        except Exception as e:
            erros.append((index, str(e)))
    
    return registros_validos, erros

# Exemplo de uso
csv_path = "precos-glp-02_2025_edit.csv"
registros, erros = validar_dados(csv_path)

print(f"Registros válidos: {len(registros)}")
print(f"Erros encontrados: {len(erros)}")
for erro in erros:
    print(f"Linha {erro[0]}: {erro[1]}")
