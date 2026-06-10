import pandas as pd
import requests
from datetime import datetime
from config import SOURCES, STATIC_SOURCES, STATIC_RATES, SOURCE_NAMES


def get_url(metric: str):
    if metric not in SOURCES:
        raise ValueError(
            f"Error : {metric} cannot be found. Available metrics : {', '.join(SOURCES)}"
        )
    return SOURCES[metric]


def fetch_url(url: str, metric: str) -> dict:
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Failed to fetch data for '{metric}': {e}")
    return response.json()


def fetch_static_rates(metric: str) -> pd.DataFrame:
    if metric not in STATIC_RATES:
        raise ValueError(
            f"Error: {metric} cannot be found. Available metrics : {', '.join(STATIC_RATES)}"
        )

    data = STATIC_RATES[metric]

    df = pd.DataFrame(list(data.items()), columns=["date", "value"])
    df["metric"] = metric
    df["source"] = STATIC_SOURCES[metric]
    df["date"] = pd.to_datetime(df["date"]).dt.date

    return df


def fetch_inflation(metric: str) -> pd.DataFrame:

    url = get_url(metric)
    data = fetch_url(url, metric)

    observations = data[1]

    records = [
        {"date": obs["date"], "value": obs["value"]}
        for obs in observations
        if obs["value"] is not None
    ]
    df = pd.DataFrame(records)

    df = df.dropna(subset=["value"])
    df["metric"] = metric
    df["source"] = SOURCE_NAMES[metric]
    df["date"] = pd.to_datetime(df["date"]).dt.date

    return df


def fetch_cac40(metric: str) -> pd.DataFrame:

    url = get_url(metric)
    data = fetch_url(url, metric)

    result = data["chart"]["result"][0]
    timestamps = result["timestamp"]
    prices = result["indicators"]["quote"][0]["close"]

    rows = []
    for ts, price in zip(timestamps, prices):
        date = datetime.fromtimestamp(ts).date()
        rows.append((date, price))

    df = pd.DataFrame(rows, columns=["date", "value"])
    df = df[
        df["date"].between(
            pd.Timestamp("2020-01-01").date(), pd.Timestamp("2025-12-12").date()
        )
    ]
    df["metric"] = metric
    df["source"] = SOURCE_NAMES[metric]
    df = df.dropna(subset=["value"])

    return df
