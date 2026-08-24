# backend/app/main.py

from fastapi import FastAPI

from app.api.routes import webhook, payments
from app.engine.flow_router import FlowRouter

#------------------------------------------------------------------------
# Application
#------------------------------------------------------------------------

app = FastAPI(
    title="Warima",
    version="1.0.1"
)

#-------------------------------------------------------------------------
# Flow Router
#-------------------------------------------------------------------------
flow_router = FlowRouter()


#--------------------------------------------------------------------------
# Routes
#--------------------------------------------------------------------------

app.include_router(
    webhook.router,
    prefix="/webhook",
    tags=["Webhook"],
)

app.include_router(
    payments.router,
    prefix="/payments",
    tags=["Payments"],
)


#---------------------------------------------------------------------------
# Health Check
#---------------------------------------------------------------------------

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "warima",
    }
