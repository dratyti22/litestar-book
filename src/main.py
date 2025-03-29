import uvicorn

from src.app import get_app # noqa F401

if __name__ == '__main__':
    uvicorn.run(
        "src.main:get_app",
        reload=True,
        factory=True,
    )
