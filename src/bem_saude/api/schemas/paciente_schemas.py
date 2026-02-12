"""
Schemas Pydantic para Paciente.

Define os DTOs (Data Transfer Objects) para requisições e respostas relacionadas
a pacientes.
"""

from datetime import date
from uuid import UUID
from pydantic import BaseModel, Field, computed_field
from bem_saude.dominio.enums.status_cadastro import StatusCadastro


class PacienteCriarRequest(BaseModel):
    """
    Schema para criação de paciente.

    Validações:
    - nome: mínimo 3 caracteres, máximo 255 caracteres
    - cpf: mínimo 11 caracteres, máximo 14 caracteres
    - telefone: mínimo 10 caracteres, máximo 15 caracteres
    """
    nome: str = Field(
        ...,
        min_length=3,
        max_length=255,
        description="Nome completo do paciente",
        examples=["Maria da Silva"]
    )
    cpf: str = Field(
        ...,
        min_length=11,
        max_length=14,
        description="CPF do paciente",
        examples=["123.456.789-00"]
    )
    telefone: str = Field(
        ...,
        min_length=10,
        max_length=15,
        description="Telefone do paciente",
        examples=["(47) 99999-9999"]
    )
    endereco: str = Field(
        ...,
        max_length=255,
        description="Endereço do paciente",
        examples=["Rua das Flores, 123"]
    )
    email: str = Field(
        ...,
        max_length=255,
        description="E-mail do paciente",
        examples=["maria@email.com"]
    )
    data_nascimento: str = Field(
        ...,
        description="Data de nascimento do paciente (YYYY-MM-DD)",
        examples=["1990-05-15"]
    )
    observacoes: str = Field(
        "",
        description="Observações sobre o paciente",
        examples=["Alérgico a dipirona"]
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nome": "Maria da Silva",
                    "cpf": "123.456.789-00",
                    "telefone": "(47) 99999-9999",
                    "endereco": "Rua das Flores, 123",
                    "email": "maria@email.com",
                    "data_nascimento": "1990-05-15",
                    "observacoes": "Alérgico a dipirona"
                }
            ]
        }
    }


class PacienteEditarRequest(BaseModel):
    """
    Schema para alteração de paciente.

    Validações:
    - nome: mínimo 3 caracteres, máximo 255 caracteres
    - telefone: mínimo 10 caracteres, máximo 15 caracteres
    """
    nome: str = Field(
        ...,
        min_length=3,
        max_length=255,
        description="Nome completo do paciente",
        examples=["Maria da Silva"]
    )
    telefone: str = Field(
        ...,
        min_length=10,
        max_length=15,
        description="Telefone do paciente",
        examples=["(47) 99999-9999"]
    )
    endereco: str = Field(
        ...,
        max_length=255,
        description="Endereço do paciente",
        examples=["Rua das Flores, 123"]
    )
    email: str = Field(
        ...,
        max_length=255,
        description="E-mail do paciente",
        examples=["maria@email.com"]
    )
    observacoes: str = Field(
        "",
        description="Observações sobre o paciente",
        examples=["Alérgico a dipirona"]
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nome": "Maria da Silva",
                    "telefone": "(47) 99999-9999",
                    "endereco": "Rua das Flores, 123",
                    "email": "maria@email.com",
                    "observacoes": "Alérgico a dipirona"
                }
            ]
        }
    }


class PacienteResponse(BaseModel):
    """
    Schema de resposta de paciente para listagem.

    Retorna dados resumidos do paciente.
    Status é retornado como boolean (True = ATIVO, False = INATIVO).
    """
    id: UUID = Field(
        ...,
        description="Identificador único do paciente (UUID v7)",
        examples=["019c445a-ae15-7bcd-ba0a-cd7b0d0e3f26"]
    )
    nome: str = Field(
        ...,
        description="Nome completo do paciente",
        examples=["Maria da Silva"]
    )
    cpf: str = Field(
        ...,
        description="CPF do paciente",
        examples=["123.456.789-00"]
    )
    telefone: str = Field(
        ...,
        description="Telefone do paciente",
        examples=["(47) 99999-9999"]
    )
    status: bool = Field(
        ...,
        description="Status do cadastro (true = ativo, false = inativo)",
        examples=[True]
    )

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": "019c445a-ae15-7bcd-ba0a-cd7b0d0e3f26",
                    "nome": "Maria da Silva",
                    "cpf": "123.456.789-00",
                    "telefone": "(47) 99999-9999",
                    "status": True
                }
            ]
        }
    }


class PacientePesquisaResponse(BaseModel):
    """
    Schema de resposta detalhada de paciente (busca por ID).

    Retorna todos os dados do paciente.
    Status é retornado como boolean (True = ATIVO, False = INATIVO).
    """
    id: UUID = Field(
        ...,
        description="Identificador único do paciente (UUID v7)",
        examples=["019c445a-ae15-7bcd-ba0a-cd7b0d0e3f26"]
    )
    nome: str = Field(
        ...,
        description="Nome completo do paciente",
        examples=["Maria da Silva"]
    )
    cpf: str = Field(
        ...,
        description="CPF do paciente",
        examples=["123.456.789-00"]
    )
    telefone: str = Field(
        ...,
        description="Telefone do paciente",
        examples=["(47) 99999-9999"]
    )
    endereco: str | None = Field(
        None,
        description="Endereço do paciente",
        examples=["Rua das Flores, 123"]
    )
    email: str | None = Field(
        None,
        description="E-mail do paciente",
        examples=["maria@email.com"]
    )
    data_nascimento: date | None = Field(
        None,
        description="Data de nascimento do paciente",
        examples=["1990-05-15"]
    )
    observacoes: str | None = Field(
        None,
        description="Observações sobre o paciente",
        examples=["Alérgico a dipirona"]
    )
    status: bool = Field(
        ...,
        description="Status do cadastro (true = ativo, false = inativo)",
        examples=[True]
    )

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": "019c445a-ae15-7bcd-ba0a-cd7b0d0e3f26",
                    "nome": "Maria da Silva",
                    "cpf": "123.456.789-00",
                    "telefone": "(47) 99999-9999",
                    "endereco": "Rua das Flores, 123",
                    "email": "maria@email.com",
                    "data_nascimento": "1990-05-15",
                    "observacoes": "Alérgico a dipirona",
                    "status": True
                }
            ]
        }
    }
