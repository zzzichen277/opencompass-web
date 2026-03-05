"""Authentication endpoints for login."""

from datetime import datetime, timedelta
from typing import Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

router = APIRouter()


# Simple in-memory token store (for demo purposes)
TOKEN_STORE = {}


class LoginRequest(BaseModel):
    """Login request model."""
    userName: str
    password: str


class LoginToken(BaseModel):
    """Login token response."""
    token: str
    refreshToken: str


class UserInfo(BaseModel):
    """User info response."""
    userId: str
    userName: str
    roles: list[str]
    buttons: list[str]


# Default users for demo
DEFAULT_USERS = {
    "admin": {
        "password": "admin123",
        "userId": "1",
        "userName": "Admin",
        "roles": ["R_SUPER"],
        "buttons": ["b1", "b2", "b3"]
    },
    "user": {
        "password": "user123",
        "userId": "2",
        "userName": "User",
        "roles": ["R_USER"],
        "buttons": ["b1"]
    }
}


@router.post("/login", response_model=LoginToken)
async def login(request: LoginRequest) -> LoginToken:
    """User login endpoint."""
    user = DEFAULT_USERS.get(request.userName)

    if not user or user["password"] != request.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Generate tokens
    token = str(uuid.uuid4())
    refresh_token = str(uuid.uuid4())

    # Store tokens
    TOKEN_STORE[token] = {
        "userId": user["userId"],
        "userName": user["userName"],
        "roles": user["roles"],
        "buttons": user["buttons"],
        "refreshToken": refresh_token,
        "expiresAt": datetime.utcnow() + timedelta(hours=24)
    }

    return LoginToken(token=token, refreshToken=refresh_token)


@router.get("/getUserInfo", response_model=UserInfo)
async def get_user_info(token: Optional[str] = None) -> UserInfo:
    """Get current user info."""
    # Try to get token from query or header
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token_data = TOKEN_STORE.get(token)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Check expiration
    if datetime.utcnow() > token_data["expiresAt"]:
        del TOKEN_STORE[token]
        raise HTTPException(status_code=401, detail="Token expired")

    return UserInfo(
        userId=token_data["userId"],
        userName=token_data["userName"],
        roles=token_data["roles"],
        buttons=token_data["buttons"]
    )


@router.post("/refreshToken", response_model=LoginToken)
async def refresh_token(refresh_token: str) -> LoginToken:
    """Refresh access token."""
    # Find token by refresh token
    for token, data in TOKEN_STORE.items():
        if data.get("refreshToken") == refresh_token:
            # Generate new tokens
            new_token = str(uuid.uuid4())
            new_refresh = str(uuid.uuid4())

            # Update store
            TOKEN_STORE[new_token] = {
                **data,
                "refreshToken": new_refresh,
                "expiresAt": datetime.utcnow() + timedelta(hours=24)
            }

            # Remove old token
            del TOKEN_STORE[token]

            return LoginToken(token=new_token, refreshToken=new_refresh)

    raise HTTPException(status_code=401, detail="Invalid refresh token")