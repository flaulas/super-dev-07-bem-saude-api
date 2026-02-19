"""
Módulo de autenticação com Auth0.

Valida tokens JWT emitidos pelo Auth0 usando JWKS (JSON Web Key Set).
Fornece a dependência `validar_token` para proteger rotas da API.
"""

import logging
from typing import Any

import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from bem_saude.api.configuracoes import configuracoes

logger = logging.getLogger(__name__)

security = HTTPBearer()

_jwks_cache: dict[str, Any] | None = None


def _obter_jwks() -> dict[str, Any]:
    """
    Busca as chaves públicas (JWKS) do Auth0.
    Faz cache em memória para evitar requisições repetidas.
    """
    global _jwks_cache
    if _jwks_cache is not None:
        return _jwks_cache

    jwks_url = f"https://{configuracoes.AUTH0_DOMAIN}/.well-known/jwks.json"
    logger.info(f"Buscando JWKS em {jwks_url}")

    response = httpx.get(jwks_url, timeout=10)
    response.raise_for_status()
    _jwks_cache = response.json()
    return _jwks_cache


def validar_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict[str, Any]:
    """
    Dependência FastAPI que valida o token JWT do Auth0.

    Retorna o payload decodificado do token se válido.
    Lança HTTPException 401 se o token for inválido ou expirado.
    """
    token = credentials.credentials

    try:
        jwks = _obter_jwks()

        # Extrair o header do token para encontrar a chave correta
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")

        # Encontrar a chave pública correspondente
        rsa_key: dict[str, str] = {}
        for key in jwks.get("keys", []):
            if key["kid"] == kid:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
                break

        if not rsa_key:
            logger.warning("Chave pública não encontrada no JWKS")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: chave não encontrada",
            )

        # Decodificar e validar o token
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience=configuracoes.AUTH0_AUDIENCE,
            issuer=f"https://{configuracoes.AUTH0_DOMAIN}/",
        )

        return payload

    except JWTError as e:
        logger.warning(f"Erro ao validar token JWT: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
        )
    except httpx.HTTPError as e:
        logger.error(f"Erro ao buscar JWKS: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Erro ao validar autenticação",
        )
