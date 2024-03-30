from fastapi import FastAPI
from .settings import settings
from .api import router as api_v1

# docs_url=None, redoc_url=None | Settings for deployment on prod
app = FastAPI(title="BackendYOGU", debug=settings.debug)
app.include_router(api_v1)

