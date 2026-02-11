"""
Schemas Pydantinc para Recepcionista.

Define os DTOs (Data Transfer Objects) para requisições e respostas relacionadas
a recepcionistas.
"""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from bem_saude.dominio.enums.status_cadastro import StatusCadastro

class RecepcionistaCriarRequest(BaseModel):
    """
    Schema para criação de recepcionista

    Nome é obrigatório
    Status padrão é ATIVO senão informado.

    Validações:
    - nome: mínimo 3 caracteres, máximo 45 caracteres
    """
    nome: str = Field(
        ..., 
        min_length=3, 
        max_length=255, 
        description="Nome completo do recepcionista",
        examples=["Mario dos Santos"]
    )
    status: StatusCadastro = Field(
        default=StatusCadastro.ATIVO,
        description="Status do cadastro",
        examples=["ATIVO"]
    )
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nome": "Mario dos Santos",
                    "status": "ATIVO"
                }
            ]
        }
    }



class RecepcionistaAlterarRequest(BaseModel):
    """
    Schema para alteração de recepcionista

    Nome é obrigatório

    Validações:
    - nome: mínimo 3 caracteres, máximo 45 caracteres
    """
    nome: str = Field(
        ..., 
        min_length=3, 
        max_length=255, 
        description="Nome completo do recepcionista",
        examples=["Mario dos Santos"]
    )
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nome": "Mario dos Santos"
                }
            ]
        }
    }


class RecepcionistaResponse(BaseModel):
    """
    Schema de resposta de recepcionista

    Retornar todos os dados do recepcionista, incluindo campos de auditoria.
    """
    id: UUID = Field(
        ...,
        description="Identificador único do recepcionista (UUID v7)",
        examples=["019c445a-ae15-7bcd-ba0a-cd7b0d0e3f26"]
    ) # uuid v7 generator
    nome: str = Field(
        ..., 
        description="Nome completo do recepcionista",
        examples=["Mario dos Santos"]
    )
    status: StatusCadastro = Field(
        ..., # Campo obrigatório e não tem valor padrão
        description="Status do cadastro",
        examples=["ATIVO"]
    )
    criado_em: datetime = Field(
        ...,
        description="Data e hora de criação do registro",
        examples=["2024-01-30T10:30:00"]
    )
    alterado_em: datetime | None = Field(
        None,
        description="Data e hora da última alteração do registro",
        examples=["2024-01-30T11:45:00"]
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nome": "Mario dos Santos",
                    "status": "ATIVO"
                }
            ]
        }
    }