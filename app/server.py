import uvicorn
from fastapi import FastAPI

from app import version
from app.endpoints.restaurant import router as restaurant_endpoint
from app.endpoints.user import router as user_endpoint
from app.endpoints.vote import router as vote_endpoint


def create_app():
    _app = FastAPI(
        title="Menu Voting API",
        version=version,
        docs_url='/api/docs',
        redoc_url=None,
        openapi_url="/api/openapi.json",
    )

    _app.include_router(prefix="/api", router=user_endpoint)
    _app.include_router(prefix="/api", router=restaurant_endpoint)
    _app.include_router(prefix="/api", router=vote_endpoint)
    return _app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=9001, reload=True)  # nosec
