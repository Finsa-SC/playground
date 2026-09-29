from fastapi import FastAPI
from pydantic import BaseModel

class HealthCheck(BaseModel):
    status: str = "ok"

app = FastAPI()

@app.get(path="/health", response_model=HealthCheck)
def get_health():
    return HealthCheck(status="ok")