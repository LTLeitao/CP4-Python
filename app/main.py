from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controller import router
from app.database import init_db

app = FastAPI(
    title="API da Academia",
    version="1.0.0"
)

init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)