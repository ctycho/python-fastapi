""" FastAPI """

from fastapi import FastAPI

from app import models
from app.database import engine
from app.routes import post, user, auth
from app.config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    """Root"""
    return {"message": "Hello World"}


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
