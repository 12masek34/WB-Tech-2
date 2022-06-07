import uvicorn

from models.database import AsyncDatabaseSession, get_db
from fastapi import FastAPI
from config import Config


def init_app():
    db = next(get_db())
    app = FastAPI(
        title='Users App',
        description='Handling Our Users',
        version='1',
    )

    @app.on_event('startup')
    async def startup():
        await db.create_all()

    @app.on_event('shutdown')
    async def shutdown():
        await db.close()

    from accounts.views import api
    app.include_router(api, prefix='/api/v1', )
    from blogs.view import api
    app.include_router(api, prefix='/api/v1', )
    return app


app = init_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
