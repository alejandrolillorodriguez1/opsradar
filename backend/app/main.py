from fastapi import FastAPI

from app.api.routes.organizations import router as organizations_router

app = FastAPI(title="OpsRadar API", version="0.1.0")

app.include_router(organizations_router, prefix="/api/v1")


@app.get("/health")
def get_health():
    return {"status": "ok"}