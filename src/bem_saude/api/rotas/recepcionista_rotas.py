from http import HTTPStatus
from uuid import UUID
from uuid6 import uuid7
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from bem_saude.api.schemas.recepcionista_schemas import RecepcionistaAlterarRequest, RecepcionistaCriarRequest, RecepcionistaResponse
from bem_saude.infraestrutura.banco_dados.conexao import obter_sessao
from bem_saude.infraestrutura.banco_dados.modelos.modelo_recepcionista import ModeloRecepcionista
from bem_saude.infraestrutura.repositorios.repositorio_recepcionista import RepositorioRecepcionista

# Router para endpoints de recepcionistas
# Todas as rotas começam com /recepcionistas

router = APIRouter(
    prefix="/recepcionistas",
    tags=["Recepcionista"]
)
@router.post(
    "", 
    response_model=RecepcionistaResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo recepcionista",
    responses={
        201: {
            "description": "Recepcionista criado com sucesso",
            "model": RecepcionistaResponse
        }
    }
)
def criar_recepcionista(
    dados: RecepcionistaCriarRequest,
    session: Session = Depends(obter_sessao),
) -> RecepcionistaResponse:
    recepcionista = ModeloRecepcionista(
        id=uuid7(),
        nome=dados.nome,
        status=dados.status,
    )
    repositorio = RepositorioRecepcionista(sessao=session)
    recepcionista = repositorio.criar(recepcionista)
    return recepcionista


@router.get(
    "",
    response_model=list[RecepcionistaResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar recepcionistas",
    responses={
        200: {
            "description": "Lista de recepcionistas",
            "model": list[RecepcionistaResponse]
        },
    },
)
def lista_recepcionistas(session: Session = Depends(obter_sessao)):
    """Lista todos os recepcionistas"""
    repositorio = RepositorioRecepcionista(sessao=session)
    recepcionistas = repositorio.listar()
    return recepcionistas


@router.get(
    "/{id}",
    response_model=RecepcionistaResponse,
    status_code=status.HTTP_200_OK,
    summary="Buscar recepcionista filtrando pelo ID",
    description="""
            Busca um recepcionista específico pelo seu ID  (UUID v7).
            
            Retorna todos os dados do recepcionista, incluido campos de auditoria.""",
    responses={
        200: {
            "description": "Recepcionista encontrado",
            "model": RecepcionistaResponse
        },
    },
)
def busca_recepionista(id: UUID, session: Session = Depends(obter_sessao)):
    """Busca um recepcionista por ID."""
    repositorio = RepositorioRecepcionista(sessao=session)
    recepcionista = repositorio.buscar_por_id(id)
    if not recepcionista:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Recepcionista não encontrado")
    return recepcionista


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Inativar recepcionista",
    description="Inativar o recepcionista quando encontrado.",
    responses={
        204: {
            "description": "Recepcionista inativado",
        },
    },
)
def inativar_recepionista(id: UUID, session: Session = Depends(obter_sessao)):
    """Inativa um recepcionista por ID."""
    repositorio = RepositorioRecepcionista(sessao=session)
    inativou = repositorio.remover(id)
    if not inativou:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Recepcionista não encontrado")
    


@router.put(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Alterar dados do recepcionista",
    responses={
        204: {
            "description": "Recepcionista alterado"
        },
        404: {
            "description": "Recepcionista não encontrado"
        }
    }
)
def alterar_recepcionista(
    id: UUID, 
    dados: RecepcionistaAlterarRequest, 
    session: Session = Depends(obter_sessao),
):
    repositorio = RepositorioRecepcionista(sessao=session)
    inativou = repositorio.editar(id, dados.nome)
    if not inativou:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Recepcionista não encontrado")

@router.put(
    "/{id}/ativar",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Ativar recepcionista",
    responses={
        204: {
            "description": "Recepcionista ativado com sucesso"
        },
        404: {
            "description": "Recepcionista não encontrado"
        }
    }
)
def ativar_recepcionista(
    id: UUID, 
    session: Session = Depends(obter_sessao),
):
    repositorio = RepositorioRecepcionista(sessao=session)
    inativou = repositorio.ativar(id)
    if not inativou:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Recepcionista não encontrado")