"""
Configuração de conexão com o banco de dados.

Gerencia o engine do SQLAlchemy e a factory de sessões.
"""

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from bem_saude.api.configuracoes import configuracoes

logger = logging.getLogger(__name__)

# Engine do SQLAlchemy
# Pool de conexões configurado para uso em produção
# echo=False para não logar SQL (apenas em modo debug)
engine = create_engine(
    configuracoes.DATABASE_URL,
    echo=False,
    pool_pre_ping=True, # Validar conexões antes de usar
    pool_size=5, # Número de conexões no pool
    max_overflow=10 # Conexões extras permitidas
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def obter_sessao() -> Session:
    db = SessionLocal()
    try:
        logger.debug("Sessão de banco de dados criada")
        yield db
    finally:
        db.close() # Sessão fechada automaticamente após o uso
        logger.debug("Sessão de banco de dados fechada")