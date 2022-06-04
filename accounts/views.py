from datetime import timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter

from accounts.models.models import User
from accounts.models.schema import Token, User as UserSchema, UserSerializer
from accounts.auth import Auth

api = APIRouter(prefix='/users', )


@api.post('/', response_model=UserSchema)
async def read_users_me(new_user: UserSerializer, auth: Auth = Depends()):
    user = UserSerializer(username=new_user.username,
                          email=new_user.email,
                          password1=new_user.password1,
                          password2=new_user.password2)
    hashed_password = auth.get_password_hash(user.password1)
    user = await User.create(username=user.username, email=user.email, hashed_password=hashed_password)
    return UserSchema.from_orm(user)

#
#
# @api.post("/token", response_model=Token)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = await auth.authenticate_user(form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = auth.create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}
#
#
# @api.get("/users/me/", response_model=UserSchema)
# async def read_users_me(current_user: User = Depends(auth.get_current_active_user)):
#     return current_user
