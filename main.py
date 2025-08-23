import uvicorn

from app.core.logger import LOGGING_CONFIG


if __name__ == "__main__":
    uvicorn.run(
        app="app.app:app",
        host="localhost",
        port=8000,
        reload=True,
        log_config=LOGGING_CONFIG,
    )
