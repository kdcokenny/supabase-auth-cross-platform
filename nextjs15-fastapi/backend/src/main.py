from fastapi import FastAPI
from gotrue.types import UserResponse
from fastapi.middleware.cors import CORSMiddleware
from .dependencies import AuthUserDep


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/auth/me")
async def get_me(user: AuthUserDep) -> UserResponse:
    return user
