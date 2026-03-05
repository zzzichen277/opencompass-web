"""Main API router that includes all sub-routers."""

from fastapi import APIRouter

from app.api.endpoints import health, models, datasets, tasks, results, websocket, templates, auth

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(models.router, prefix="/models", tags=["Models"])
api_router.include_router(datasets.router, prefix="/datasets", tags=["Datasets"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(results.router, prefix="/results", tags=["Results"])
api_router.include_router(templates.router, prefix="/templates", tags=["Templates"])

# WebSocket router (no prefix, handles its own path)
api_router.include_router(websocket.router, tags=["WebSocket"])