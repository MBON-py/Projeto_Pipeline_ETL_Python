from pydantic import BaseModel, Field, validator
from typing import Optional
import re

class ValidadorCSV(BaseModel):
    regiao_sigla: str = Field(..., min_length=1, max_length=2, description="Sigla da região deve ter entre 1 e 2 caracteres.")
    estado_sigla: Optional[str] = Field(None, min_length=2, max_length=2, regex=r"^[A-Z]{2}$", description="Sigla do estado deve ter 2 letras maiúsculas, mas pode estar em branco.")
    municipio: str
    revenda: str
    cnpj_revenda: str = Field(..., min_length=14, max_length=14, description="CNPJ deve ter 14 dígitos numéricos.")
    nome_rua: str
    numero_rua: str
    complemento: Optional[str] = None
    bairro: str
    cep: str = Field(..., min_length=8, max_length=8, description="CEP deve ter 8 dígitos numéricos.")
    produto: str = Field(..., regex=r"^GLP$", description="Produto deve ser apenas 'GLP'.")
    data_coleta: str = Field(..., regex=r"^\d{2}-\d{2}-\d{4}$", description="Data deve estar no formato dd-mm-aaaa.")
    valor_venda: float = Field(..., gt=0, description="Valor de venda deve ser positivo.")
    valor_compra: Optional[float] = Field(None, ge=0, description="Valor de compra não pode ser negativo.")
    unidade_medida: str
    bandeira: str

    @validator("cnpj_revenda", pre=True)
    def limpar_cnpj(cls, cnpj: str) -> str:
        """Remove caracteres não numéricos do CNPJ e valida o tamanho."""
        cnpj_limpo = re.sub(r"\D", "", cnpj)  # Remove tudo que não for dígito
        if len(cnpj_limpo) != 14:
            raise ValueError("CNPJ deve ter 14 dígitos numéricos.")
        return cnpj_limpo

    @validator("cep", pre=True)
    def limpar_cep(cls, cep: str) -> str:
        """Remove caracteres não numéricos do CEP e valida o tamanho."""
        cep_limpo = re.sub(r"\D", "", cep)  # Remove tudo que não for dígito
        if len(cep_limpo) != 8:
            raise ValueError("CEP deve ter 8 dígitos numéricos.")
        return cep_limpo

    @validator("data_coleta", pre=True)
    def formatar_data(cls, data: str) -> str:
        """Converte a data para o formato dd-mm-aaaa."""
        return data.replace("/", "-")

    @validator("valor_venda", pre=True)
    def tratar_valor_venda(cls, valor: str | float) -> float:
        """Converte o valor_venda para float, substituindo vírgula por ponto."""
        if isinstance(valor, float):
            return valor  # Já é um float, não precisa de conversão
        if isinstance(valor, str):
            valor = valor.replace(",", ".")  # Substitui vírgula por ponto
            try:
                return float(valor)  # Converte para float
            except ValueError:
                raise ValueError("O valor de venda deve ser um número válido.")
        raise ValueError("O valor de venda deve ser um número válido.")

    @validator("valor_compra", pre=True)
    def tratar_valor_compra(cls, valor: str | float) -> Optional[float]:
        """Converte o valor_compra para float, tratando valores vazios ou inválidos."""
        if valor is None or (isinstance(valor, str) and valor.strip() == ""):
            return None  # Retorna None se o valor for vazio ou nulo
        if isinstance(valor, float):
            return valor if valor >= 0 else None  # Retorna None se o valor for negativo
        # Converte a string para float
        try:
            valor_float = float(valor.replace(",", "."))
            return valor_float if valor_float >= 0 else None  # Retorna None se o valor for negativo
        except (ValueError, TypeError):
            return None  # Retorna None se a conversão falhar