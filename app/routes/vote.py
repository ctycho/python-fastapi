from typing import List

from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app import models, oauth2
from app.database import get_db
from app.schemas import Vote


router = APIRouter(
    prefix='/vote',
    tags=['Vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: Vote, db: Session = Depends(get_db),
         current_user: models.User = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                      detail='provided post does not exists')

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                             models.Vote.user_id == current_user.id)

    row = vote_query.first()
    if vote.dir == 1:
        if row:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'user {current_user.id} has already voted on post {vote.post_id}')
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {'message': 'vote sucessfully added'}
    else:
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='vote is not found')
    
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {'message': 'vote was deleted'}
