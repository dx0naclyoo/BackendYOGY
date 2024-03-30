import uvicorn

if __name__ == '__main__':
    uvicorn.run(
        "src.backend.app:app",
        reload=True,
    )
