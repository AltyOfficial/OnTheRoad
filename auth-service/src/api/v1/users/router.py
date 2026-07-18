from typing import Optional
from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    Header,
    HTTPException,
    status,
)
from starlette.requests import Request

from src.api.v1.users.schemas import (
    AuthTokenResponseSchema,
    RefreshTokenRequestSchema,
    UserCreateRequestSchema,
    UserDetailResponseSchema,
    UserLoginRequestSchema,
)
from src.apps.users.exceptions import (
    InvalidCredentialsError,
    InvalidTokenError,
    SessionNotFoundError,
    UserAlreadyExistsError,
)
from src.apps.users.infra.services import get_user_service, UserService
from src.config.settings import settings
from src.config.settings import logger

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    "/register/",
    description="Register new User",
    response_model=UserDetailResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    payload: UserCreateRequestSchema,
    service: UserService = Depends(get_user_service),
) -> UserDetailResponseSchema:
    """Register new user."""

    try:
        user = await service.register(payload=payload)
    except (UserAlreadyExistsError) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    except Exception as exc:
        logger.error(f"Error registering user: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"server error",
        )

    return UserDetailResponseSchema.model_validate(user)


@router.post(
    "/login/",
    description="Login existing User",
    response_model=AuthTokenResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def login_user(
    payload: UserLoginRequestSchema,
    service: UserService = Depends(get_user_service),
    user_agent: Optional[str] = Header(default=None),
    ip_address: Optional[str] = Header(default=None),
) -> AuthTokenResponseSchema:
    """Login existing user."""

    try:
        tokens = await service.login(payload=payload, user_agent=user_agent, ip_address=ip_address)
    except (InvalidCredentialsError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        )
    except Exception as exc:
        logger.error(f"Error logging in user: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"server error",
        )

    return AuthTokenResponseSchema.model_validate(tokens)


@router.post(
    "/refresh/",
    description="Refresh JWT tokens",
    response_model=AuthTokenResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def refresh_tokens(
    payload: RefreshTokenRequestSchema,
    service: UserService = Depends(get_user_service),
    user_agent: Optional[str] = Header(default=None),
    ip_address: Optional[str] = Header(default=None),
) -> AuthTokenResponseSchema:
    """Refresh JWT tokens."""

    try:
        tokens = await service.refresh(payload=payload, user_agent=user_agent, ip_address=ip_address)
    except (InvalidTokenError, SessionNotFoundError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        )
    except Exception as exc:
        logger.error(f"Error refreshing tokens: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"server error",
        )

    return AuthTokenResponseSchema.model_validate(tokens)


@router.post(
    "/logout/",
    description="Logout User and Invoke Refresh Token",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout(
    payload: RefreshTokenRequestSchema,
    service: UserService = Depends(get_user_service),
) -> None:
    """Logout User."""

    try:
        await service.logout(payload=payload)
    except (InvalidTokenError, SessionNotFoundError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        )
    except Exception as exc:
        logger.error(f"Error refreshing tokens: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"server error",
        )

