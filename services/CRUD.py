from fastapi import HTTPException
from models.database import db
from models.models import User


class CRUDUser:
    def __init__(self):
        self._db = db

    async def create(self, **kwargs):
        user = User(**kwargs)
        self._db.add(user)
        try:
            await self._db.commit()
        except Exception as e:
            await self._db.rollback()
            message = str(e.__cause__)
            if message is not None:
                raise HTTPException(status_code=400, detail=message)
            else:
                raise HTTPException(status_code=400, detail='Bad request.')
        return user
