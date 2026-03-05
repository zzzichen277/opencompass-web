"""Health check endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def health() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}