from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import text
from db.session import SessionLocal

router = APIRouter(prefix="/api", tags=["health"])

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    db_status = {"status": "connected", "message": "Database connection successful"}
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
    except Exception as e:
        db_status = {"status": "disconnected", "message": f"Database connection failed: {str(e)}"}
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "error", "api": "healthy", "database": db_status}
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "success",
            "api": {"status": "healthy", "message": "API is running"},
            "database": db_status
        }
    )