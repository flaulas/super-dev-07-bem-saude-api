"""
Modelo ORM para a tabela de pacientes.

Mapeia a entidade Paciente para a tabela 'pacientes' no PostgreSQL.
"""

from sqlalchemy import Column, String, Date, Text
from bem_saude.infraestrutura.banco_dados.modelos.modelo_base import ModeloBase
from sqlalchemy.dialects.postgresql import UUID


class ModeloPaciente(ModeloBase):
    """
    Modelo ORM da tabela 'pacientes'

    Mapeia os campos da entidade de domínio Paciente para colunas
    do banco de dados PostgreSQL.
    """
    __tablename__ = "pacientes"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False
    )
    nome = Column(String(255), nullable=False)
    cpf = Column(String(14), nullable=False, unique=True)
    telefone = Column(String(15), nullable=False)
    endereco = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    data_nascimento = Column(Date, nullable=True)
    observacoes = Column(Text, nullable=True)
    status = Column(String(10), nullable=False)
