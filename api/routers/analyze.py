from database import get_latest_value
from analysis import compute_comparison, compute_real_return
from llm.anthropic_provider import AnthropicProvider
from config import METRICS

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/analyze", tags=["analysis"])

provider = AnthropicProvider()


def validate_asset(asset: str):
    if asset not in METRICS:
        raise HTTPException(status_code=404, detail=f"Invalid asset : {asset}")


def get_inflation():
    return get_latest_value("inflation")


@router.get("/real-return")
def real_return(asset: str, amount: float):
    validate_asset(asset)

    try:
        asset_data = get_latest_value(asset)
        inflation_data = get_inflation()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    real = compute_real_return(
        asset_rate=asset_data["value"],
        inflation_rate=inflation_data["value"],
        amount=amount,
    )

    return JSONResponse(
        content={
            "asset": asset,
            "amount": amount,
            "asset_rate": asset_data,
            "inflation_rate": inflation_data,
            "result": real,
        },
        media_type="application/json; charset=utf-8",
    )


@router.get("/compare")
def compare(assets: str, amount: float):
    asset_list = assets.split(",")
    inflation_data = get_inflation()

    rates = {}
    for asset in asset_list:
        validate_asset(asset)
        try:
            asset_data = get_latest_value(asset)
            rates[asset] = asset_data["value"]
        except ValueError:
            continue

    comparison = compute_comparison(rates, inflation_data["value"])

    return JSONResponse(
        content={"results": comparison}, media_type="application/json; charset=utf-8"
    )


@router.get("/analyze")
def analyze(asset: str, amount: float):
    validate_asset(asset)

    try:
        asset_data = get_latest_value(asset)
        inflation_data = get_inflation()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    real = compute_real_return(
        asset_rate=asset_data["value"],
        inflation_rate=inflation_data["value"],
        amount=amount,
    )

    stats = {
        "asset": asset,
        "amount": amount,
        "asset_rate": asset_data["value"],
        "inflation_rate": round(inflation_data["value"], 2),
        "result": real,
    }

    try:
        analysis = provider.generate_analysis(stats)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"LLM service unavailable: {e}")

    return JSONResponse(
        content={"stats": stats, "analysis": analysis},
        media_type="application/json; charset=utf-8",
    )
