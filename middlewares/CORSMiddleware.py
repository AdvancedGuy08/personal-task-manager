from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def cors_middleware(app: FastAPI) -> CORSMiddleware:
    origins = (
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    )

    return CORSMiddleware(
        app,
        allow_credentials=True,
        allow_headers=["*"],
        allow_methods=["*"],
        allow_origins=origins,
    )
