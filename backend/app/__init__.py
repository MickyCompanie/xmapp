from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import Config

from app.person.model import Person  
from app.user.model import User
from app.wish.model import Wish   
from app.gift.model import Gift 

from app.auth.router import auth_router
from app.user.router import user_router
from app.wish.router import wish_router


app = FastAPI(
    title='xmapp api',
    description='an api made to make christmas even more magical',
    version=Config.VERSION
)

url = f'/{Config.PREFIX}{Config.VERSION}'


app.include_router(auth_router, prefix=f"{url}/auth", tags=["auth"])
app.include_router(user_router, prefix=f"{url}/user", tags=["user"])
app.include_router(wish_router, prefix=f"{url}/wish", tags=["wish"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/')
def read_root():
    return {"message": "Welcome to the xmapp api!"}