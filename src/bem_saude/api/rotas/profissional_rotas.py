from http import HTTPStatus
from uuid import UUID
from uuid6 import uuid7
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from bem_saude.api.schemas.profissional_schemas import ProfissionalCriarRequest, ProfissionalEditarRequest, ProfissionalPesquisaResponse, ProfissionalResponse
from bem_saude.dominio.enums.status_cadastro import StatusCadastro
from bem_saude.infraestrutura.banco_dados.conexao import obter_sessao
from bem_saude.infraestrutura.banco_dados.modelos.modelo_profissional import ModeloProfissional
from bem_saude.infraestrutura.repositorios.repositorio_profissional import RepositorioProfissional
from bem_saude.api.auth import validar_token

# Router para endpoints de profissionais
# Todas as rotas começam com /profissionais

router = APIRouter(
    prefix="/profissionais",
    tags=["Profissional"],
    dependencies=[Depends(validar_token)]
)


def _converter_status_para_bool(modelo: ModeloProfissional) -> dict:
    """Converte o modelo ORM para dict com status como boolean."""
    return {
        "id": modelo.id,
        "nome": modelo.nome,
        "especialidade": modelo.especialidade,
        "registro": modelo.registro,
        "duracao": modelo.duracao,
        "valor": modelo.valor,
        "dias_semana": modelo.dias_semana,
        "status": modelo.status == StatusCadastro.ATIVO.value,
    }


@router.post(
    "",
    response_model=ProfissionalResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo profissional",
    responses={
        201: {
            "description": "Profissional criado com sucesso",
            "model": ProfissionalResponse
        }
    }
)
def criar_profissional(
    dados: ProfissionalCriarRequest,
    session: Session = Depends(obter_sessao),
) -> ProfissionalResponse:
    profissional = ModeloProfissional(
        id=uuid7(),
        nome=dados.nome,
        especialidade=dados.especialidade,
        registro=dados.registro,
        duracao=dados.duracao,
        valor=dados.valor,
        dias_semana=dados.dias_semana,
        status=StatusCadastro.ATIVO.value,
    )
    repositorio = RepositorioProfissional(sessao=session)
    profissional = repositorio.criar(profissional)
    return _converter_status_para_bool(profissional)


@router.get(
    "",
    response_model=list[ProfissionalResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar profissionais",
    responses={
        200: {
            "description": "Lista de profissionais",
            "model": list[ProfissionalResponse]
        },
    },
)
def listar_profissionais(session: Session = Depends(obter_sessao)):
    """Lista todos os profissionais."""
    repositorio = RepositorioProfissional(sessao=session)
    profissionais = repositorio.listar()
    return [_converter_status_para_bool(p) for p in profissionais]


@router.get(
    "/{id}",
    response_model=ProfissionalPesquisaResponse,
    status_code=status.HTTP_200_OK,
    summary="Buscar profissional filtrando pelo ID",
    description="""
            Busca um profissional específico pelo seu ID (UUID v7).

            Retorna todos os dados do profissional.""",
    responses={
        200: {
            "description": "Profissional encontrado",
            "model": ProfissionalPesquisaResponse
        },
        404: {
            "description": "Profissional não encontrado"
        },
    },
)
def buscar_profissional(id: UUID, session: Session = Depends(obter_sessao)):
    """Busca um profissional por ID."""
    repositorio = RepositorioProfissional(sessao=session)
    profissional = repositorio.buscar_por_id(id)
    if not profissional:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Profissional não encontrado")
    return _converter_status_para_bool(profissional)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Inativar profissional",
    description="Inativar o profissional quando encontrado.",
    responses={
        204: {
            "description": "Profissional inativado",
        },
        404: {
            "description": "Profissional não encontrado"
        },
    },
)
def inativar_profissional(id: UUID, session: Session = Depends(obter_sessao)):
    """Inativa um profissional por ID."""
    repositorio = RepositorioProfissional(sessao=session)
    inativou = repositorio.remover(id)
    if not inativou:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Profissional não encontrado")


@router.put(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Alterar dados do profissional",
    responses={
        204: {
            "description": "Profissional alterado"
        },
        404: {
            "description": "Profissional não encontrado"
        }
    }
)
def alterar_profissional(
    id: UUID,
    dados: ProfissionalEditarRequest,
    session: Session = Depends(obter_sessao),
):
    repositorio = RepositorioProfissional(sessao=session)
    editou = repositorio.editar(
        id,
        nome=dados.nome,
        especialidade=dados.especialidade,
        duracao=dados.duracao,
        valor=dados.valor,
        dias_semana=dados.dias_semana,
    )
    if not editou:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Profissional não encontrado")


@router.put(
    "/{id}/ativar",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Ativar profissional",
    responses={
        204: {
            "description": "Profissional ativado com sucesso"
        },
        404: {
            "description": "Profissional não encontrado"
        }
    }
)
def ativar_profissional(
    id: UUID,
    session: Session = Depends(obter_sessao),
):
    repositorio = RepositorioProfissional(sessao=session)
    ativou = repositorio.ativar(id)
    if not ativou:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Profissional não encontrado")
