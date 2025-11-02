from fastapi import FastAPI

app = FastAPI(title="Anom Platform API")

# later:
# from anom.modules.business_def import api as business_api
# app.include_router(business_api.router, prefix="/businesses")
