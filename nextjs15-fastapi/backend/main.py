import os
import base64
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Request
from dotenv import load_dotenv
from supabase import AsyncClient
from supabase.client import AsyncSupabaseAuthClient, create_async_client
from gotrue.types import UserResponse

load_dotenv()


def _get_auth_session_cookie(request: Request) -> str | None:
    print(f"Request cookies: {request.cookies}")
    for cookie_name in request.cookies.keys():
        if cookie_name.startswith("auth_session"):
            return request.cookies.get(cookie_name)
    return None


AuthSessionCookieDep = Annotated[str | None, Depends(_get_auth_session_cookie)]


async def _get_auth_client() -> AsyncSupabaseAuthClient:
    """
    Create a new authentication client for each request.

    Returns:
        AsyncGoTrueClient: A configured instance of AsyncGoTrueClient.

    Note:
        A new client is created for each request to ensure thread safety and
        to avoid sharing state between requests.
    """
    url = os.getenv("SUPABASE_URL")
    anon_key = os.getenv("SUPABASE_ANON_KEY")

    if not url or not anon_key:
        raise ValueError("SUPABASE_URL or SUPABASE_ANON_KEY is not set")

    supabase: AsyncClient = await create_async_client(url, anon_key)

    return supabase.auth


AuthClientDep = Annotated[AsyncSupabaseAuthClient, Depends(_get_auth_client)]


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/auth/me")
async def get_me(
    auth_session: AuthSessionCookieDep, client: AuthClientDep
) -> UserResponse | None:
    if not auth_session:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        user = await client.get_user(auth_session)
    except Exception as e:
        raise e

    return user


@app.get("/auth/me/base64")
async def get_me_base64(
    auth_session: AuthSessionCookieDep, client: AuthClientDep
) -> UserResponse | None:
    if not auth_session:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Remove 'base64-' prefix and add padding if needed
    base64_str = auth_session.replace("base64-", "")
    padding_needed = len(base64_str) % 4
    if padding_needed:
        base64_str += "=" * (4 - padding_needed)

    # Decode base64 to get the actual session token
    try:
        decoded_session = base64.b64decode(base64_str).decode("utf-8")
        user = await client.get_user(decoded_session)
    except Exception as e:
        raise e

    return user


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
