from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer, Boolean, Text
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete
from sqlalchemy.future import select
from fastapi import HTTPException
from sqlalchemy.orm import relationship

from models.database import Base, db


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(128), unique=True, nullable=False)
    full_name = Column(String(128))
    email = Column(String(128), unique=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    disabled = Column(Boolean, default=False)
    created_at = Column(DateTime, index=True, default=datetime.utcnow)
    posts = relationship('Post', backref='user', cascade='all, delete-orphan',
                         primaryjoin="User.id == Post.user_id")

    def __repr__(self):
        return (
            f'<{self.__class__.__name__}('
            f'id={self.id}, '
            f'username={self.username}, '
            f')>'
        )

    @classmethod
    async def create(cls, **kwargs):
        user = cls(**kwargs)
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

    @classmethod
    async def update(cls, id, **kwargs):
        query = (
            sqlalchemy_update(cls).where(cls.id == id).values(**kwargs)
                .execution_options(synchronize_session='fetch')
        )
        await db.execute(query)
        try:
            await db.commit()
        except Exception as e:
            await db.rollback()
            message = e.__cause__
            if message is not None:
                raise HTTPException(status_code=400, detail=message)
            else:
                raise HTTPException(status_code=400, detail='Bad request.')

        users = await db.execute(select(cls).where(cls.id == id))
        (user,) = users.first()
        return user

    @classmethod
    async def get(cls, id):
        query = select(cls).where(cls.id == id)
        users = await db.execute(query)
        (user,) = users.first()
        return user

    @classmethod
    async def delete(cls, id):
        query = sqlalchemy_delete(cls).where(cls.id == id)
        await db.execute(query)
        try:
            await db.commit()
        except Exception as e:
            await db.rollback()
            message = e.__cause__
            if message is not None:
                raise HTTPException(status_code=400, detail=message)
            else:
                raise HTTPException(status_code=400, detail='Bad request.')
        return True


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(256), nullable=False)
    text = Column(Text)
    created_at = Column(DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return (
            f'<{self.__class__.__name__}('
            f'id={self.id}, '
            f'username={self.title}, '
            f')>'
        )
