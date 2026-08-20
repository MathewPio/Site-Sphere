from fastapi import FastAPI

app = FastAPI(
    title="sitesphere API",
    description="Backend API for the SiteSphere construction collaboration platform",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message" "Welcome to SiteSphere API"
    }