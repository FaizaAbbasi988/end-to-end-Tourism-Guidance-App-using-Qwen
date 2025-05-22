from fastapi import FastAPI
from .app import router as non_login_router
from .login_app import router as login_router  # Import your login router

base_api_url = "/algorithm/api"

def create_app():
    app = FastAPI()
    return app

def register_router(app: FastAPI):
    app.include_router(router=non_login_router, prefix=base_api_url)
    app.include_router(router=login_router, prefix=base_api_url)
