from fastapi import FastAPI
from app.api.routes import webhook

app = FastAPI()

app.include_router(
    webhook.router,
    prefix="/webhook",
    tags=["Webhook"]
)

app.include_router(payments.router, prefix="/payments", tags=[Payments])
