from datetime import date
from http import HTTPStatus
from uuid import UUID
from uuid6 import uuid7
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from bem_saude.api.schemas.paciente_schemas import PacienteCriarRequest, PacienteEditarRequest, PacientePesquisaResponse, PacienteResponse
from bem_saude.dominio.enums.status_cadastro import StatusCadastro
from bem_saude.infraestrutura.banco_dados.conexao import obter_sessao
from bem_saude.infraestrutura.banco_dados.modelos.modelo_paciente import ModeloPaciente
from bem_saude.infraestrutura.repositorios.repositorio_paciente import RepositorioPaciente

# Router para endpoints de pacientes
# Todas as rotas começam com /pacientes

router = APIRouter(
    prefix="/pacientes",
    tags=["Paciente"]
)


def _converter_status_para_bool(modelo: ModeloPaciente) -> dict:
    """Converte o modelo ORM para dict com status como boolean."""
    return {
        "id": modelo.id,
        "nome": modelo.nome,
        "cpf": modelo.cpf,
        "telefone": modelo.telefone,
        "endereco": modelo.endereco,
        "email": modelo.email,
        "data_nascimento": modelo.data_nascimento,
        "observacoes": modelo.observacoes,
        "status": modelo.status == StatusCadastro.ATIVO.value,
    }


@router.post(
    "",
    response_model=PacienteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo paciente",
    responses={
        201: {
            "description": "Paciente criado com sucesso",
            "model": PacienteResponse
        }
    }
)
def criar_paciente(
    dados: PacienteCriarRequest,
    session: Session = Depends(obter_sessao),
) -> PacienteResponse:
    data_nasc = None
    if dados.data_nascimento:
        data_nasc = date.fromisoformat(dados.data_nascimento)

    paciente = ModeloPaciente(
        id=uuid7(),
        nome=dados.nome,
        cpf=dados.cpf,
        telefone=dados.telefone,
        endereco=dados.endereco,
        email=dados.email,
        data_nascimento=data_nasc,
        observacoes=dados.observacoes,
        status=StatusCadastro.ATIVO.value,
    )
    repositorio = RepositorioPaciente(sessao=session)
    paciente = repositorio.criar(paciente)
    return _converter_status_para_bool(paciente)


@router.get(
    "",
    response_model=list[PacienteResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar pacientes",
    responses={
        200: {
            "description": "Lista de pacientes",
            "model": list[PacienteResponse]
        },
    },
)
def listar_pacientes(session: Session = Depends(obter_sessao)):
    """Lista todos os pacientes."""
    repositorio = RepositorioPaciente(sessao=session)
    pacientes = repositorio.listar()
    return [_converter_status_para_bool(p) for p in pacientes]


@router.get(
    "/{id}",
    response_model=PacientePesquisaResponse,
    status_code=status.HTTP_200_OK,
    summary="Buscar paciente filtrando pelo ID",
    description="""
            Busca um paciente específico pelo seu ID (UUID v7).

            Retorna todos os dados do paciente.""",
    responses={
        200: {
            "description": "Paciente encontrado",
            "model": PacientePesquisaResponse
        },
        404: {
            "description": "Paciente não encontrado"
        },
    },
)
def buscar_paciente(id: UUID, session: Session = Depends(obter_sessao)):
    """Busca um paciente por ID."""
    repositorio = RepositorioPaciente(sessao=session)
    paciente = repositorio.buscar_por_id(id)
    if not paciente:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Paciente não encontrado")
    return _converter_status_para_bool(paciente)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Inativar paciente",
    description="Inativar o paciente quando encontrado.",
    responses={
        204: {
            "description": "Paciente inativado",
        },
        404: {
            "description": "Paciente não encontrado"
        },
    },
)
def inativar_paciente(id: UUID, session: Session = Depends(obter_sessao)):
    """Inativa um paciente por ID."""
    repositorio = RepositorioPaciente(sessao=session)
    inativou = repositorio.remover(id)
    if not inativou:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Paciente não encontrado")


@router.put(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Alterar dados do paciente",
    responses={
        204: {
            "description": "Paciente alterado"
        },
        404: {
            "description": "Paciente não encontrado"
        }
    }
)
def alterar_paciente(
    id: UUID,
    dados: PacienteEditarRequest,
    session: Session = Depends(obter_sessao),
):
    repositorio = RepositorioPaciente(sessao=session)
    editou = repositorio.editar(
        id,
        nome=dados.nome,
        telefone=dados.telefone,
        endereco=dados.endereco,
        email=dados.email,
        observacoes=dados.observacoes,
    )
    if not editou:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Paciente não encontrado")


@router.put(
    "/{id}/ativar",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Ativar paciente",
    responses={
        204: {
            "description": "Paciente ativado com sucesso"
        },
        404: {
            "description": "Paciente não encontrado"
        }
    }
)
def ativar_paciente(
    id: UUID,
    session: Session = Depends(obter_sessao),
):
    repositorio = RepositorioPaciente(sessao=session)
    ativou = repositorio.ativar(id)
    if not ativou:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Paciente não encontrado")
