"""
Aplicação FastAPI principal.

Configura e inicializa a aplicação FastAPI com todas as dependências:
- Middlewares
- Tratadores de exceção
- Rotas
- Swagger (condicional ao ambiente)
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from bem_saude.api.configuracoes import configuracoes
from bem_saude.api.rotas.recepcionista_rotas import router as recepcionista_router
from bem_saude.api.rotas.paciente_rotas import router as paciente_router
from bem_saude.infraestrutura.banco_dados.modelos.modelo_base import Base
from bem_saude.infraestrutura.banco_dados.conexao import engine

# Configurar logging antes de criar a aplicação
logging.basicConfig(
    level=configuracoes.LOG_LEVEL,
    format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H-%M-%S"
)

logger = logging.getLogger(__name__)


def criar_aplicacao() -> FastAPI:
    if configuracoes.eh_producao:
        logger.info("Iniciando aplicação em modo PRODUÇÃO (Swagger desabilitado)")
        app = FastAPI(
            docs_url=None,      # Desabilita /docs
            redoc_url=None,     # Desabilita /redoc
            openapi_url=None,   # Desabilita /openapi.json
        )
    else:
        logger.info("Iniciando aplicação em modo DESENVOLVIMENTO (Swagger habilitado)")
        app = FastAPI(
            title="Bem Saúde API",
            version="1.0.0",
            docs_url="/docs",
            redoc_url="/redoc",
            openapi_url="/openapi.json",
        )

    logger.info("Configurando middleware de cors")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:4200",
            "https://bemsaude.com.br"
        ],
        allow_credentials=False,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"]
    )

    logger.info("Configurando middleware de logs")

    logger.info("Configurando tratadores de exceção")

    logger.info("Registrando rotas")
    app.include_router(recepcionista_router)
    app.include_router(paciente_router)

    @app.get("/health", tags=["Sistema"], summary="Health check", description="Verifica se a API está respondendo")
    def health_check():
        return {
            "status": "ok",
            "ambiente": configuracoes.AMBIENTE,
            "swagger_habilitado": configuracoes.swagger_habilitado
        }
    logger.info("Aplicação configurada com sucesso")

    # from bem_saude.infraestrutura.banco_dados.modelos.modelo_base import Base
    # from bem_saude.infraestrutura.banco_dados.conexao import engine   
    Base.metadata.create_all(engine)
    return app

# Criar instância da aplicação
app = criar_aplicacao()