from fastapi import HTTPException
from sqlalchemy.future import select
from starlette import status

from models.database import AsyncDatabaseSession
from models.models import User
from schemas.user_schema import UserInDB as UserInDBSchema


async def create_user(db: AsyncDatabaseSession, **kwargs):
    user = User(**kwargs)
    db.add(user)
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        message = str(e.__cause__)
        if message is not None:
            raise HTTPException(status_code=400, detail=message)
        else:
            raise HTTPException(status_code=400, detail='Bad request.')
    return user


async def get_user(db: AsyncDatabaseSession, username: str) -> UserInDBSchema:
    query = select(User).where(User.username == username)
    users = await db.execute(query)
    user = users.first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Username not found.',
        )
    (user,) = user
    return UserInDBSchema.from_orm(user)
