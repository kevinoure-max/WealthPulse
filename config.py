LIVRET_A_RATES = {
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


LEP_RATES = {
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

STATIC_RATES = {
    "livret_a": LIVRET_A_RATES,
    "lep": LEP_RATES,
}

STATIC_SOURCES = {
    "livret_a": "banque_de_france",
    "lep": "banque_de_france",
}

SOURCES = {
    "inflation": "https://api.worldbank.org/v2/country/FR/indicator/FP.CPI.TOTL.ZG?format=json&date=2020:2025&per_page=20",
    "cac40": "https://query1.finance.yahoo.com/v8/finance/chart/%5EFCHI?interval=1mo&range=7y",
}

SOURCE_NAMES = {
    "inflation": "world_bank",
    "cac40": "yahoo_finance",
}


METRICS = ["livret_a", "lep", "inflation", "cac40"]
