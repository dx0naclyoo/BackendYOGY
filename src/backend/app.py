from fastapi import FastAPI
from .settings import settings
from .api import router as api_v1
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware


origins = [
    "http://localhost:5173/",
    "http://127.0.0.1:5173/",
    "https://ugor.netlify.app/auth",
    "https://ugor.netlify.app/"
]

middleware = [
    Middleware(CORSMiddleware, allow_origins=origins)
]

app = FastAPI(
    title="BackendYOGU",
    description="API For YOGY university",
    debug=settings.debug,
    middleware=middleware
)
# docs_url=None, redoc_url=None | Settings for deployment on prod


app.include_router(api_v1)