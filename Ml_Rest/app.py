from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

import dal_users
from router_users import router as user_router
from router_ml import router as ml_router


app = FastAPI(title="Project 4 - REST API + ML + JWT")


@app.on_event("startup")
def startup():
    dal_users.create_table_users()


@app.get("/")
def root():
    html_path = os.path.join(os.path.dirname(__file__), "index.html")

    if os.path.exists(html_path):
        return FileResponse(html_path, media_type="text/html")

    return {"message": "index.html not found"}


app.include_router(user_router)
app.include_router(ml_router)