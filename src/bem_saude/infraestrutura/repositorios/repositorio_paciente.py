from datetime import date
from uuid import UUID
from bem_saude.dominio.enums.status_cadastro import StatusCadastro
from bem_saude.infraestrutura.banco_dados.modelos.modelo_paciente import ModeloPaciente

from sqlalchemy.orm import Session


class RepositorioPaciente:
    def __init__(self, sessao: Session):
        self.sessao = sessao

    def criar(self, paciente: ModeloPaciente) -> ModeloPaciente:
        self.sessao.add(paciente)
        self.sessao.commit()
        self.sessao.flush(paciente)
        return paciente

    def listar(self) -> list[ModeloPaciente]:
        modelos = self.sessao.query(ModeloPaciente).order_by(ModeloPaciente.status, ModeloPaciente.nome).all()
        return modelos

    def buscar_por_id(self, id: UUID) -> ModeloPaciente | None:
        modelo = self.sessao.query(ModeloPaciente).filter(ModeloPaciente.id == id).first()
        return modelo

    def editar(self, id: UUID, nome: str, telefone: str, endereco: str, email: str, observacoes: str):
        modelo = self.sessao.query(ModeloPaciente).filter(ModeloPaciente.id == id).first()
        if not modelo:
            return False

        modelo.nome = nome
        modelo.telefone = telefone
        modelo.endereco = endereco
        modelo.email = email
        modelo.observacoes = observacoes
        self.sessao.commit()
        return True

    def remover(self, id: UUID):
        modelo = self.sessao.query(ModeloPaciente).filter(ModeloPaciente.id == id).first()
        if not modelo:
            return False

        modelo.status = StatusCadastro.INATIVO.value
        self.sessao.commit()
        return True

    def ativar(self, id: UUID):
        modelo = self.sessao.query(ModeloPaciente).filter(ModeloPaciente.id == id).first()
        if not modelo:
            return False

        modelo.status = StatusCadastro.ATIVO.value
        self.sessao.commit()
        return True
