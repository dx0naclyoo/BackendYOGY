import uvicorn

from src.backend.settings import settings

if __name__ == '__main__':
    uvicorn.run(
        "src.backend.app:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )
