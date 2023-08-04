import uvicorn
from fastapi import FastAPI

from apps.common.routes import router as common_routes


app = FastAPI()
app.include_router(common_routes)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
