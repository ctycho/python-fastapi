from typing import List

from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app import models, utils
from app.database import get_db
from app.schemas import UserCreate, UserOut

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.get("/", response_model=List[UserOut])
async def get_users(db: Session = Depends(get_db)):
    """Create user"""
    user = db.query(models.User).all()

    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create user"""

    # hash the password
    hashed_password = utils.hash_pwd(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}", response_model=UserOut)
async def get_user(id: int, db: Session = Depends(get_db)):
    """get post by id"""
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id)))
    # row = cursor.fetchone()
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Did not find user with provided id: {id}')
    return user
