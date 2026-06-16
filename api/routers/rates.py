from fastapi import APIRouter, HTTPException
from database import get_data, get_latest_value
from analysis import compute_rolling_average
from config import METRICS


router = APIRouter(prefix="/rates", tags=["rates"])


def validate_metric(metric: str):
    if metric not in METRICS:
        raise HTTPException(
            status_code=404,
            detail=f"Invalid metric : {metric}. Available metrics: {', '.join(METRICS)}",
        )


@router.get("/{metric}")
def read_rates(metric: str):

    validate_metric(metric)

    df = get_data(metric)
    if df.empty:
        raise HTTPException(
            status_code=404, detail="No data found for the requested metric"
        )

    return {
        "metric": metric,
        "count": len(df),
        "data": df.to_dict(orient="records"),
    }


@router.get("/{metric}/latest")
def latest_rates(metric: str):

    validate_metric(metric)

    try:
        result = get_latest_value(metric)
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"No data available for metric '{metric}'"
        )

    return {"metric": metric, "latest": result}


@router.get("/{metric}/trend")
def metric_trend(metric: str, window: int = 3):
    validate_metric(metric)
    df = get_data(metric)
    if df.empty:
        raise HTTPException(
            status_code=404, detail="No data found for the requested metric"
        )
    df = compute_rolling_average(df, window)
    return {
        "metric": metric,
        "window": window,
        "data": df.to_dict(orient="records"),
    }
