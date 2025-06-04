from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.public.health import router as health_router
from api.public.users import router as user_router
from api.public.auth import router as auth_router
from core.security import get_current_active_user
from core.config import settings

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(user_router)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

