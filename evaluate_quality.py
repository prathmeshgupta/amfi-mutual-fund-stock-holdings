import re
import pandas as pd
from pathlib import Path

ISO_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ISIN_REGEX = re.compile(r"^IN[A-Z0-9]{10}$")


def audit_quality():
    print("=" * 65)
    print(" AMFI MUTUAL FUND STOCK HOLDINGS - DATA QUALITY AUDIT")
    print("=" * 65)

    root = Path(__file__).parent
    pq_path = root / "output" / "mf_stock_holdings.parquet"
    csv_path = root / "output" / "mf_stock_holdings.csv"

    assert pq_path.exists(), "mf_stock_holdings.parquet missing"
    assert csv_path.exists(), "mf_stock_holdings.csv missing"

    df_pq = pd.read_parquet(pq_path)
    df_csv = pd.read_csv(csv_path)

    # 1. Parity Check
    assert len(df_pq) == len(df_csv), f"Parity mismatch: Parquet ({len(df_pq)}) != CSV ({len(df_csv)})"
    print(f"Total Holding Records Indexed: {len(df_pq)} [PASS - 100% Parity]")

    # 2. Null Checks
    null_count = df_pq.isnull().sum().sum()
    assert null_count == 0, f"Found {null_count} nulls across table"
    print("Null Values: 0 across all columns [100% COMPLETE]")

    # 3. ISO-8601 Format
    s = df_pq["month_end"].astype(str)
    invalid = s[~s.str.match(ISO_REGEX)]
    assert len(invalid) == 0, f"Non-ISO dates detected: {len(invalid)}"
    print("ISO-8601 Compliance (month_end): 100% PASS")

    # 4. ISIN Format
    invalid_isin = df_pq["isin"][~df_pq["isin"].str.match(ISIN_REGEX)]
    assert len(invalid_isin) == 0, f"Invalid ISINs detected: {len(invalid_isin)}"
    print("Regulatory ISIN Integrity (^IN[A-Z0-9]{10}$): 100% PASS")

    # 5. Domain Invariants
    assert (df_pq["shares_held"] > 0).all(), "Non-positive shares held"
    assert (df_pq["market_value_cr"] > 0).all(), "Non-positive market value"
    assert ((df_pq["portfolio_weight_pct"] > 0) & (df_pq["portfolio_weight_pct"] <= 100)).all(), "Weight out of (0, 100]"
    print("Domain Bounds (Positive shares, values, and portfolio weights): [PASS]")

    # 6. Top Held Stocks Across Schemes
    latest_dt = df_pq["month_end"].max()
    latest_df = df_pq[df_pq["month_end"] == latest_dt]
    agg = latest_df.groupby("symbol")["market_value_cr"].sum().sort_values(ascending=False)
    print(f"\nTop Institutional Stock Holdings across Schemes as of {latest_dt}:")
    for sym, val in agg.head(5).items():
        print(f"  • {sym:<12}: Rs.{val:>9,.1f} Cr across reporting funds")

    print("=" * 65)
    print("ALL AUDIT CHECKS PASSED.")
    print("=" * 65)


if __name__ == "__main__":
    audit_quality()
