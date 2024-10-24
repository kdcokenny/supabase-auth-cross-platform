import base64
import os
from typing import Annotated
from fastapi import Depends, HTTPException, Request
from dotenv import load_dotenv
from supabase import AsyncClient
from supabase.client import create_async_client, AsyncSupabaseAuthClient
from gotrue.types import UserResponse, Session as AuthSession

load_dotenv()


def _decode_auth_session_base64(base64_auth_session: str) -> AuthSession:
    padding_needed = len(base64_auth_session) % 4
    if padding_needed:
        base64_auth_session += "=" * (4 - padding_needed)

    try:
        decoded_session = base64.b64decode(base64_auth_session).decode("utf-8")
        return AuthSession.model_validate_json(decoded_session)
    except Exception as e:
        raise e


def _extract_auth_session_cookie(request: Request) -> str | None:
    session_cookie_arr: list[str] = []
    for cookie_name in request.cookies.keys():
        if cookie_name == "auth_session" or cookie_name.startswith("auth_session."):
            session_cookie_arr.append(request.cookies.get(cookie_name, ""))

    base64_str = "".join(session_cookie_arr).replace("base64-", "")

    return base64_str


AuthSessionCookieDep = Annotated[str | None, Depends(_extract_auth_session_cookie)]


async def _create_auth_client() -> AsyncSupabaseAuthClient:
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


AuthClientDep = Annotated[AsyncSupabaseAuthClient, Depends(_create_auth_client)]


async def retrieve_auth_session(
    auth_session_cookie: AuthSessionCookieDep,
) -> AuthSession | None:
    if not auth_session_cookie:
        return None

    session = _decode_auth_session_base64(auth_session_cookie)

    return session


AuthSessionDep = Annotated[AuthSession | None, Depends(retrieve_auth_session)]


async def fetch_user(
    client: AuthClientDep, auth_session: AuthSessionDep
) -> UserResponse:
    if not auth_session:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = await client.get_user(auth_session.access_token)

    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return user


AuthUserDep = Annotated[UserResponse, Depends(fetch_user)]
