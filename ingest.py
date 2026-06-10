from ingestion import fetch_static_rates, fetch_inflation, fetch_cac40
from database import init_db, save_data
from config import METRICS


FETCHERS = {
    "livret_a": fetch_static_rates,
    "lep": fetch_static_rates,
    "inflation": fetch_inflation,
    "cac40": fetch_cac40,
}


def run_ingestion():
    init_db()

    for metric in METRICS:
        print(f"Fetching {metric}..")
        df = FETCHERS[metric](metric)
        print(f" {len(df)} rows fetched. Saving..")
        save_data(df)
        print(f" {metric} saved.")
    print("Ingestion completed")


if __name__ == "__main__":
    run_ingestion()
