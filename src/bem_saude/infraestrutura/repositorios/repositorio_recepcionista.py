from uuid import UUID
from bem_saude.dominio.enums.status_cadastro import StatusCadastro
from bem_saude.infraestrutura.banco_dados.modelos.modelo_recepcionista import ModeloRecepcionista
from sqlalchemy import asc, desc, func

from sqlalchemy.orm import Session

class RepositorioRecepcionista:
    def __init__(self, sessao: Session):
        self.sessao = sessao
    
    def criar(self, recepcionista: ModeloRecepcionista) -> ModeloRecepcionista:
        self.sessao.add(recepcionista)
        self.sessao.commit()
        self.sessao.flush(recepcionista)

        return recepcionista

    def listar(self) -> list[ModeloRecepcionista]:
        modelos = self.sessao.query(ModeloRecepcionista).order_by(ModeloRecepcionista.status, ModeloRecepcionista.nome).all()
        return modelos

    def remover(self, id: UUID):
        modelo = self.sessao.query(ModeloRecepcionista).filter(ModeloRecepcionista.id == id).first()
        if not modelo:
            return False
        
        modelo.status = "INATIVO"
        self.sessao.commit()
        return True
    
    def buscar_por_id(self, id: UUID) -> ModeloRecepcionista | None:
        modelo = self.sessao.query(ModeloRecepcionista).filter(ModeloRecepcionista.id == id).first()
        return modelo
    
    def editar(self, id: UUID, nome: str):
        modelo = self.sessao.query(ModeloRecepcionista).filter(ModeloRecepcionista.id == id).first()
        if not modelo:
            return False
        
        modelo.nome = nome
        self.sessao.commit()
        return True

    
    def ativar(self, id: UUID):
        modelo = self.sessao.query(ModeloRecepcionista).filter(ModeloRecepcionista.id == id).first()
        if not modelo:
            return False
        
        modelo.status = StatusCadastro.ATIVO.value
        self.sessao.commit()
        return True
