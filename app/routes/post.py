from typing import List

from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func

from app import models, oauth2
from app.database import get_db
from app.schemas import PostCreate, Post, PostOut


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get("/", response_model=List[PostOut])
async def get_posts(db: Session = Depends(get_db),
                    _: str = Depends(oauth2.get_current_user)):
    """Get all posts"""
    # cursor.execute("SELECT * FROM posts")
    # records = cursor.fetchall()

    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains('search')
    #     ).limit(5).offset(1).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True
        ).group_by(models.Post.id).all()

    return posts


@router.get("/my", response_model=List[Post])
async def get_my_posts(db: Session = Depends(get_db),
                    current_user: models.User = Depends(oauth2.get_current_user)):
    """Get my posts"""
    # cursor.execute("SELECT * FROM posts")
    # records = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_post(post: PostCreate, db: Session = Depends(get_db),
                      current_user: models.User = Depends(oauth2.get_current_user)):
    """Create post"""
    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
    #                (post.title, post.content, post.published))
    
    # row = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=PostOut)
async def get_post(id: int, db: Session = Depends(get_db),
                   _: str = Depends(oauth2.get_current_user)):
    """get post by id"""
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id)))
    # row = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True
        ).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Did not find post with provided id: {id}')
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db),
                      current_user: models.User = Depends(oauth2.get_current_user)):
    """delete post by id"""
    # cursor.execute("DELETE FROM posts WHERE id = %s returning *", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Did not find')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Unauthorized request')
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=Post)
async def update_post(id: int, post: PostCreate, db: Session = Depends(get_db),
                      current_user: models.User = Depends(oauth2.get_current_user)):
    """delete post by id"""
    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s returning *",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    row = post_query.first()
    
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Did not find')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Unauthorized request')

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    
    return post_query.first()