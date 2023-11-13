from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy import func
from fastapi.encoders import jsonable_encoder
router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    responses={404: {"description": "Not found"}}
)


#@router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    #     models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)

    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()

    # posts = db.execute(
    #     'select posts.*, COUNT(votes.post_id) as votes from posts LEFT JOIN votes ON posts.id=votes.post_id  group by posts.id')
    # results = []
    # for post in posts:
    #     results.append(dict(post))
    # print(results)
    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.post_id, isouter=True).group_by(models.Post.post_id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.get("/{post_id}", response_model=schemas.PostOut)
def get_posts(post_id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.post_id, isouter=True).group_by(models.Post.post_id).filter(
        models.Post.post_id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id:{post_id} was not found",
        )
    # if post.owner_id != current_user.user_id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail=f"User with id:{current_user.user_id} is not authorized to get this post",
    #     )
    return post


# Her Post işleminde status_code=201 ile 201 kodu döndürülür.
# response_model=schemas.Post ile response un içeriğini "Product"ın içeriği şekilde döndürür.
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_product(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    
    new_post = models.Post(owner_id=current_user.user_id,**dict(post))
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{post_id}")
def delete_product(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post = (
        db.query(models.Post)
        .filter(models.Post.post_id == post_id)
        .first()
    )
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id:{post_id} was not found",
        )
    if post.owner_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User with id:{current_user.user_id} is not authorized to delete this post",
        )
    db.delete(post)
    db.commit()
    return {"data": "Product deleted successfully"}


@router.put("/{post_id}", response_model=schemas.Post)
def update_product(
    post_id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(
        models.Post.post_id == post_id
    )
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id:{post_id} was not found",
        )
    if post.owner_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User with id:{current_user.user_id} is not authorized to update this post",
        )
    post_query.update(dict(updated_post), synchronize_session=False)
    db.commit()
    db.refresh(post)
    return post
