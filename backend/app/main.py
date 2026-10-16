from fastapi import FastAPI

app = FastAPI(title="OpsRadar API",version="0.1.0")

@app.get("/health")
def get_health():
    return {"status":"ok"}


