from fastapi import Depends, FastAPI
from api.public.health import router as health_router
from api.public.users import router as user_router
from core.security import get_current_active_user

app = FastAPI()
app.include_router(health_router)
app.include_router(user_router)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/users/me")
async def read_users_me(current_user = Depends(get_current_active_user)):
    return current_user
