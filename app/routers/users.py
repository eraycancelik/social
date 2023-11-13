from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, utils, database

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    existing_user_email = (
        db.query(models.User).filter(models.User.email == user.email).first()
    )

    if existing_user_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email:{user.email} already exists",
        )
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**dict(user))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/", response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    return users


@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id:{user_id} was not found",
        )
    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id:{user_id} was not found",
        )
    db.delete(user)
    db.commit()
    return {"message": f"User with id:{user_id} was deleted"}
