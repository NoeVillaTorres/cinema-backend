from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.titles import router as titles_router
from routes.genres import router as genres_router
from routes.auth import router as auth_router


app = FastAPI(
    title="Cinema Catalog API",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://cinematrixxxx.netlify.app",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(titles_router)
app.include_router(genres_router)
app.include_router(auth_router) 