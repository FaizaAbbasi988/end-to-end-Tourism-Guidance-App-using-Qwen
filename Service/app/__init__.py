from fastapi import FastAPI
from .app import router as non_login_router 

base_api_url = "/algorithm/api"
def create_app():
    app = FastAPI()
    return app

def register_router(app: FastAPI):
    app.include_router(router = non_login_router, prefix = base_api_url)