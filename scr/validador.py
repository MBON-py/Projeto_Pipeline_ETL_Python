from pydantic import BaseModel, Field, ValidationError
from typing import Optional
import re


class ValidadorCSV(BaseModel):
    regiao_sigla: str = Field(..., min_length=2, max_length=2, pattern=r"^[A-Z]{2}$", description="Sigla da região deve ter 2 letras maiúsculas.")
    estado_sigla: Optional[str] = Field(None, min_length=2, max_length=2, regex=r"^[A-Z]{2}$", description="Sigla do estado deve ter 2 letras maiúsculas, mas pode estar em branco.")
    municipio: str
    revenda: str
    cnpj_revenda: str = Field(..., min_length=14, max_length=18, description="CNPJ deve ter 14 dígitos numéricos, podendo conter pontuação.")
    nome_rua: str
    numero_rua: str
    complemento: Optional[str] = None
    bairro: str
    cep: str = Field(..., min_length=8, max_length=8, regex=r"^\d{8}$", description="CEP deve ter 8 dígitos numéricos.")
    produto: str = Field(..., regex=r"^GLP$", description="Produto deve ser apenas 'GLP'.")
    data_coleta: str = Field(..., regex=r"^\d{2}-\d{2}-\d{4}$", description="Data deve estar no formato dd-mm-yyyy.")
    valor_venda: float = Field(..., gt=0, description="Valor de venda deve ser positivo.")
    valor_compra: Optional[float] = Field(None, ge=0, description="Valor de compra não pode ser negativo.")
    unidade_medida: str
    bandeira: str

    @classmethod
    def limpar_cnpj(cls, cnpj: str) -> str:
        """Remove caracteres não numéricos do CNPJ."""
        return re.sub(r"\D", "", cnpj)

    @classmethod
    def limpar_valor(cls, valor: str) -> Optional[float]:
        """Converte uma string de valor para float, tratando valores vazios ou inválidos."""
        if not valor or valor.strip() == "":
            return None
        return float(valor.replace(",", "."))

    @classmethod
    def validar_linha(cls, linha: dict):
        """Valida uma linha de dados e retorna o objeto validado ou os erros encontrados."""
        try:
            # Limpa e formata os campos necessários
            linha["cnpj_revenda"] = cls.limpar_cnpj(linha.get("cnpj_revenda", ""))
            linha["valor_venda"] = cls.limpar_valor(linha.get("valor_venda", "0"))
            linha["valor_compra"] = cls.limpar_valor(linha.get("valor_compra", ""))

            # Remove campos vazios ou nulos que são opcionais
            if linha["valor_compra"] is None:
                linha.pop("valor_compra", None)

            return cls(**linha), None
        except ValidationError as e:
            return None, e.errors()


# Exemplo de uso
dados_exemplo = {
    "regiao_sigla": "NE",
    "estado_sigla": "PE",
    "municipio": "Recife",
    "revenda": "Posto ABC",
    "cnpj_revenda": "12.345.678/0001-99",
    "nome_rua": "Av. Boa Viagem",
    "numero_rua": "123",
    "complemento": "",
    "bairro": "Centro",
    "cep": "50060070",
    "produto": "GLP",
    "data_coleta": "20-03-2025",
    "valor_venda": "185,15",
    "valor_compra": "",  # Campo opcional vazio
    "unidade_medida": "Litro",
    "bandeira": "Petrobras"
}

validado, erros = ValidadorCSV.validar_linha(dados_exemplo)
if erros:
    print("Erros encontrados:", erros)
else:
    print("Dados validados com sucesso:", validado.dict())