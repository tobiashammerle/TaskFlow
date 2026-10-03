from fastapi import APIRouter, Depends

from taskflow.application.login_user import LoginUser
from taskflow.application.register_user import RegisterUser
from taskflow.routers.dependencies import (
    get_login_user_use_case,
    get_register_user_use_case,
)
from taskflow.schemas import LoginRequest, RegisterUserRequest, TokenResponse

router = APIRouter(prefix="/auth")


@router.post("/register", status_code=201)
def register(
    request: RegisterUserRequest,
    register_user: RegisterUser = Depends(get_register_user_use_case),
) -> None:
    register_user.execute(
        email=request.email,
        password=request.password,
    )


@router.post("/login", response_model=TokenResponse)
def login(
    request: LoginRequest, login_user: LoginUser = Depends(get_login_user_use_case)
) -> TokenResponse:
    token = login_user.execute(
        email=request.email,
        password=request.password,
    )
    return TokenResponse(access_token=token, token_type="bearer")
