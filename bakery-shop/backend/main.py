from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager

from products import customer_router, admin_router
from db.pool import pool

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Executed on Startup
    pool.open()
    yield
    # Executed on Shutdown
    pool.close()

class HealthCheck(BaseModel):
    status: str = "ok"

app = FastAPI(lifespan=lifespan)

@app.get(path="/health", response_model=HealthCheck)
def get_health():
    return HealthCheck(status="ok")

app.include_router(customer_router)
app.include_router(admin_router)