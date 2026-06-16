from contextlib import asynccontextmanager
from database import init_db
from api.routers import rates, analyze

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(api: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="WealthPulse API",
    description=(
        "WealthPulse provides access to historical financial metrics "
        "(Livret A, LEP, inflation, CAC 40), computes inflation-adjusted "
        "real returns, compares assets, and generates factual AI-powered analyses."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(rates.router)
app.include_router(analyze.router)
