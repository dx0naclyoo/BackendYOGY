from fastapi import FastAPI
from .settings import settings
from .api import router as api_v1
from fastapi.middleware.cors import CORSMiddleware

# docs_url=None, redoc_url=None | Settings for deployment on prod
app = FastAPI(title="BackendYOGU", debug=settings.debug)
app.include_router(api_v1)


origins = [
    "http://localhost:5173/",
    "http://127.0.0.1:5173/",
    "https://localhost:5173/",
    "https://127.0.0.1:5173/",
    "10.217.154.102:0/",
    "http://10.217.154.102:0/",
    "https://10.217.154.102:0/",
    "10.217.154.9:0/",
    "http://10.217.154.9:0/",
    ""
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
