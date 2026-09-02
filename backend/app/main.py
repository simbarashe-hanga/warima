# backend/app/main.py

from fastapi import FastAPI

from app.api.routes import webhook, payments

#------------------------------------------------------------------------
# Application
#------------------------------------------------------------------------

app = FastAPI(
    title="Warima",
    version="1.0.1"
)


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
