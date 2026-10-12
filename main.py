
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

import models
import schemas
from database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User Management REST API",
    description="API to create, view, update, and delete users",
    version="1.0.0"
)


# 1. Create User
@app.post(
    "/users",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.scalar(
        select(models.User).where(models.User.email == user.email)
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    new_user = models.User(**user.model_dump())
    db.add(new_user)

    try:
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )


# 2. Get All Users (with optional filters)
@app.get("/users", response_model=list[schemas.UserResponse])
def get_users(
    city: str | None = None,
    is_active: bool | None = None,
    db: Session = Depends(get_db)
):
    query = select(models.User)

    if city is not None:
        query = query.where(models.User.city == city)

    if is_active is not None:
        query = query.where(models.User.is_active == is_active)

    return db.scalars(query.order_by(models.User.id)).all()


# 3. Get User by ID
@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(models.User, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# 4. Update User
@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(
    user_id: int,
    user_data: schemas.UserUpdate,
    db: Session = Depends(get_db)
):
    user = db.get(models.User, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    duplicate_email = db.scalar(
        select(models.User).where(
            models.User.email == user_data.email,
            models.User.id != user_id
        )
    )

    if duplicate_email:
        raise HTTPException(
            status_code=409,
            detail="Email already belongs to another user"
        )

    for field, value in user_data.model_dump().items():
        setattr(user, field, value)

    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email already belongs to another user"
        )


# 5. Delete User
@app.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(models.User, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)
    db.commit()
    return None
