from fastapi import FastAPI

from middlewares.CORSMiddleware import cors_middleware


def add_midlewares(app: FastAPI) -> FastAPI:
    app.add_middleware(cors_middleware(app))
    return app
