from fastapi import FastAPI

from app.features.users.router import router as users_router

app = FastAPI(title="Lorica API", docs_url="/")

app.include_router(users_router)
