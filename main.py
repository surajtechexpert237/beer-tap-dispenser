import uvicorn
from fastapi import FastAPI

from apps.admin import routes as admin_routes
from apps.common.routes import router as common_routes

app = FastAPI()

app.include_router(common_routes)
"""Admin Routes"""
app.include_router(admin_routes.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
