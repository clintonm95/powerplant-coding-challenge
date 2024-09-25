from fastapi import FastAPI
from routers import production_plan_router

app = FastAPI(
    title="Power Distribution API",
    description="API for managing power distribution and power plants",
    version="1.0.0",
)

app.include_router(
    production_plan_router.router,
    prefix="/productionplan",
    tags=["Power Distribution"],
)
