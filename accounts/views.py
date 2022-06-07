from datetime import timedelta

from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter

from schemas.user_schema import Token, User as UserSchema, UserSerializer
from accounts.auth import get_password_hash, authenticate_user, create_access_token, get_current_active_user
from services.CRUD_user import create_user, get_user
from config import Config
from models.database import AsyncDatabaseSession, get_db

api = APIRouter(prefix='/users', )


@api.post('/registration', response_model=UserSchema, summary='Registration new user.', tags=['Users'],
          status_code=status.HTTP_201_CREATED)
async def read_users_me(new_user: UserSerializer, db: AsyncDatabaseSession = Depends(get_db)):
    user = UserSerializer(username=new_user.username,
                          email=new_user.email,
                          password1=new_user.password1,
                          password2=new_user.password2)
    hashed_password = get_password_hash(user.password1)
    user = await create_user(db, username=user.username, email=user.email, hashed_password=hashed_password)
    return UserSchema.from_orm(user)


#
@api.post('/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
                                 db: AsyncDatabaseSession = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username, 'scopes': form_data.scopes},
        expires_delta=access_token_expires,
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@api.get('/me/', response_model=UserSchema, summary='Check user authorization.', tags=['Users'],
         status_code=status.HTTP_200_OK)
async def read_users_me(current_user: UserSchema = Security(get_current_active_user)):
    return current_user
