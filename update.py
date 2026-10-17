"""
Automated Monthly Dataset Updater for amfi-mutual-fund-stock-holdings
Can be executed locally or via GitHub Actions.
Zero credentials required.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd
from amfi_mf_holdings.fetcher import MutualFundHoldingsFetcher

OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CSV_FILE = OUTPUT_DIR / "mf_stock_holdings.csv"
PARQUET_FILE = OUTPUT_DIR / "mf_stock_holdings.parquet"


def update():
    print("[1/3] Fetching monthly mutual fund equity stock holdings from AMFI disclosures...")
    fetcher = MutualFundHoldingsFetcher()
    new_df = fetcher.fetch_holdings()
    print(f"      Retrieved {len(new_df)} fund-holding observations.")

    print("[2/3] Merging and saving updated mutual fund holdings dataset...")
    if CSV_FILE.exists():
        existing_df = pd.read_csv(CSV_FILE)
        combined = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        combined = new_df.copy()

    combined = combined.drop_duplicates(subset=["month_end", "scheme_name", "symbol"], keep="last")
    combined = combined.sort_values(by=["month_end", "amc_name", "portfolio_weight_pct"], ascending=[False, True, False])

    combined.to_csv(CSV_FILE, index=False)
    combined.to_parquet(PARQUET_FILE, index=False)
    print(f"      Saved {len(combined)} records to {CSV_FILE.name} and {PARQUET_FILE.name}.")

    print("[3/3] Running automated quality audit...")
    from evaluate_quality import audit_quality
    audit_quality()
    print("Update complete successfully.")


if __name__ == "__main__":
    update()
