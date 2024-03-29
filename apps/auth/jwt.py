from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any

from jose import jwt
from pydantic import ValidationError
from apps.config import settings
from apps.user.deps import get_current_user
from apps.user.models import User
from apps.user.schemas import UserOut
from apps.user.service import UserService
from ..security import create_access_token, create_refresh_token
from .schema import TokenPayload, TokenSchema

auth_router = APIRouter()

@auth_router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = await UserService.authenticate(email = form_data.username, password = form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    return {
        "access_token": create_access_token(user.user_id),
        "refresh_token": create_refresh_token(user.user_id),
    }

@auth_router.get('/', summary="Get User", response_model=UserOut)
async def test_token(user: User = Depends(get_current_user)):
    return user

@auth_router.post('/refresh', summary="Refresh expired access token with refresh token", response_model=TokenSchema)
async def refresh_token(token: str = Body(...)):
    try:
        payload = jwt.decode(token, settings.JWT_REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await UserService.get_user_by_id(token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid token for user",
        )
    return {
        "access_token": create_access_token(user.user_id),
        "refresh_token": create_refresh_token(user.user_id)
    }

