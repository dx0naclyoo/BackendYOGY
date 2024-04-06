from typing import Callable

from fastapi import FastAPI, APIRouter
from fastapi.routing import APIRoute
from starlette.requests import Request
from starlette.responses import Response

from .settings import settings
from .api import router as api_v1
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(
    title="BackendYOGU",
    description="API For YOGY university",
    debug=settings.debug,

)
# docs_url=None, redoc_url=None | Settings for deployment on prod
app.include_router(api_v1)

origins = ["*"]


# Handle CORS
class CORSHandler(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def preflight_handler(request: Request):
            if request.method == 'OPTIONS':
                response = Response()
                response.headers['Access-Control-Allow-Origin'] = '*'
                response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, OPTIONS'
                response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
            else:
                response = await original_route_handler(request)

        return preflight_handler


router = APIRouter(route_class=CORSHandler)

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
