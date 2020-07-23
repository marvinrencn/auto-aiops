from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware

from aiops.database import models
from aiops.database.database import engine
from aiops.router import routers

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# CORS处理
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routers.router)

# 程序内启动fastapi
if __name__ == '__main__':
    uvicorn.run(app=app, host="0.0.0.0", port=8000)

