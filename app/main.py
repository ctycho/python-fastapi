""" FastAPI """

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from app import models
# from app.database import engine
from app.routes import post, user, auth, vote

"""
creates database by pydantic, but we use alembic instead now
"""
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root"""
    return {"message": "Hello World"}


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(vote.router)
