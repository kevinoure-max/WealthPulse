LIVRET_A_RATES = {
    "livret_a": {
        "2020-02": 0.5,
        "2020-08": 0.5,
        "2021-02": 0.5,
        "2021-08": 0.5,
        "2022-02": 1.0,
        "2022-08": 2.0,
        "2023-02": 3.0,
        "2023-08": 3.0,
        "2024-02": 3.0,
        "2024-08": 3.0,
        "2025-02": 2.4,
        "2025-08": 1.7,
        "2026-02": 1.5,
    }
}


LEP_RATES = {
    "lep": {
        "2020-02": 1.0,
        "2020-08": 1.0,
        "2021-02": 1.0,
        "2021-08": 1.0,
        "2022-02": 2.2,
        "2022-08": 4.6,
        "2023-02": 6.1,
        "2023-08": 6.0,
        "2024-02": 5.0,
        "2024-08": 4.0,
        "2025-02": 3.5,
        "2025-08": 2.7,
        "2026-02": 2.5,
    }
}

SOURCES = {
    "inflation": "https://stats.oecd.org/SDMX-JSON/data/PRICES_CPI/FRA.CPALTT01.GY.M/all",
    "cac_40": "https://query1.finance.yahoo.com/v8/finance/chart/%5EFCHI?interval=1mo&range=2y",
}

METRICS = ["livret_a", "lep", "inflation", "cac_40"]

STATIC_RATES = {
    "livret_a": LIVRET_A_RATES,
    "lep": LEP_RATES,
}
