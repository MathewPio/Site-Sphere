from fastapi import FastAPI

from app.api.auth import router as auth_router

app = FastAPI(
    title="sitesphere API",
    description="Backend API for the SiteSphere construction collaboration platform",
    version="1.0.0",
)

app.include_router(auth_router)

@app.get("/")
def root():
    return {
        "message" "Welcome to SiteSphere API"
    }