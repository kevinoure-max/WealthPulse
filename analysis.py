import pandas as pd


def compute_real_return(
    asset_rate: float, inflation_rate: float, amount: float
) -> dict:
    # Note : asset_rate is the nominal annual rate as published by Banque de France
    # For Livret A et LEP, interest is compound semi-annually, giving a slighly higher effective annual rate.
    # Difference is negligible for rate below 5%
    if inflation_rate is None:
        raise ValueError("Inflation data is not available for this period")

    nominal_return = amount * asset_rate / 100
    inflation_impact = amount * inflation_rate / 100
    real_return = nominal_return - inflation_impact

    # Approximation : real_rate ≈ asset_rate - inflation_rate
    # (The exact Fisher formula could be used instead)
    real_rate = asset_rate - inflation_rate

    return {
        "nominal_return": round(nominal_return, 2),
        "inflation_impact": round(inflation_impact, 2),
        "real_return": round(real_return, 2),
        "real_rate": round(real_rate, 2),
    }


def compute_rolling_average(df: pd.DataFrame, window: int = 3) -> pd.DataFrame:
    df = df.copy()
    df = df.sort_values("date")
    df["rolling_avg"] = df["value"].rolling(window=window).mean()
    df["rolling_avg"] = (
        df["rolling_avg"].astype(object).where(df["rolling_avg"].notna(), None)
    )
    return df


def compute_comparison(rates: dict, inflation_rate: float) -> list:
    result = []
    for asset, rate in rates.items():
        real_rate = round(rate - inflation_rate, 2)
        result.append({"asset": asset, "rate": rate, "real_rate": real_rate})

    return sorted(result, key=lambda item: item["real_rate"], reverse=True)
