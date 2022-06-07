from fastapi import APIRouter
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,)

from schemas.post_schema import Post as PostSchema

api = APIRouter(prefix='/post', )


@api.post('', response_model=PostSchema, summary='Create new post by authorization user.', tags=['Post'],)
async def create_post(post: PostSchema):
    pass