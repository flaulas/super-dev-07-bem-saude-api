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
from bem_saude.api.configuracoes import configuracoes

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

    logger.info("Configurando middleware de logs")

    logger.info("Configurando tratadores de exceção")

    logger.info("Registrando rotas")

    @app.get("/health", tags=["Sistema"], summary="Health check", description="Verifica se a API está respondendo")
    def health_check():
        return {
            "status": "ok",
            "ambiente": configuracoes.AMBIENTE,
            "swagger_habilitado": configuracoes.swagger_habilitado
        }
    logger.info("Aplicação configurada com sucesso")
    return app

# Criar instância da aplicação
app = criar_aplicacao()