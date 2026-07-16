import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import analysis, auth, library, movies, recommendations, rooms, social
from app.core.config import get_settings
from app.db.base import Base, SessionLocal, engine
from app.db.seed import seed
from app.services.analysis.mood import get_provider

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

APP_VERSION = "1.0.0"


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        seed(db)
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version=APP_VERSION, lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health", tags=["health"])
    def health() -> dict:
        provider = get_provider()
        return {
            "status": "ok",
            "version": APP_VERSION,
            "mood_provider": provider.name,
            "mood_provider_available": provider.available(),
        }

    app.include_router(auth.router)
    app.include_router(auth.users_router)
    app.include_router(movies.router)
    app.include_router(recommendations.router)
    app.include_router(analysis.router)
    app.include_router(rooms.router)
    app.include_router(rooms.ws_router)
    app.include_router(social.router)
    app.include_router(library.router)
    return app


app = create_app()
