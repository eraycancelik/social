from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=["Authantication"])


@router.post("/login", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User with email:{user_credentials.username} was not found",
        )
    if not utils.verify_password(user_credentials.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Incorrect password"
        )

    access_token = oauth2.create_access_token(data={"user_id": user.user_id})

    return {"access_token": access_token, "token_type": "bearer"}
