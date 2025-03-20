from pydantic import BaseModel, Field
from typing import Optional, Annotated
from datetime import date
from dateutil.parser import parse

# Definições corretas de validação para Pydantic v2
CNPJ = Annotated[str, Field(pattern=r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}")]
CEP = Annotated[str, Field(pattern=r"\d{5}-\d{3}")]

class RegistroGLP(BaseModel):
    regiao_sigla: str
    estado_sigla: str
    municipio: str
    revenda: str
    cnpj_revenda: CNPJ
    nome_rua: str
    numero_rua: Optional[str] = None
    complemento: Optional[str] = None
    bairro: str
    cep: CEP
    produto: str
    data_coleta: date
    valor_venda: Optional[float] = None
    valor_compra: Optional[float] = None
    unidade_medida: str
    bandeira: str

    @classmethod
    def from_dict(cls, data: dict):
        """ Converte dicionário de strings para os tipos corretos. """
        data["data_coleta"] = parse(data["data_coleta"], dayfirst=True).date()
        if data["valor_venda"]:
            data["valor_venda"] = float(data["valor_venda"].replace(",", "."))
        if data["valor_compra"]:
            data["valor_compra"] = float(data["valor_compra"].replace(",", "."))
        return cls(**data)