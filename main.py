from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.public.health import router as health_router
from api.public.users import router as user_router
from api.public.auth import router as auth_router
from api.private.categories import router as categories_router
from api.private.customers import router as customer_router
from api.private.products import router as product_router
from core.config import settings

app = FastAPI(
    title="Dropship Tracker API",
    description="API for managing dropshipping operations",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI endpoint
    redoc_url="/redoc",  # ReDoc endpoint
    openapi_url="/openapi.json"  # OpenAPI schema endpoint
)

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
app.include_router(product_router)
app.include_router(categories_router)

# Add private routes
app.include_router(customer_router)
