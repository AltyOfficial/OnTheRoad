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
    UserCreateRequestSchema,
    UserDetailResponseSchema,
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
    description="Регистрация нового пользователя",
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
