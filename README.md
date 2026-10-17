# AMFI Monthly Mutual Fund Stock Holdings Dataset

[![Monthly Update](https://github.com/prathmeshgupta/amfi-mutual-fund-stock-holdings/actions/workflows/update.yml/badge.svg)](https://github.com/prathmeshgupta/amfi-mutual-fund-stock-holdings/actions/workflows/update.yml)
[![Format: Parquet](https://img.shields.io/badge/Format-Apache%20Parquet-blue.svg)](output/mf_stock_holdings.parquet)
[![Format: CSV](https://img.shields.io/badge/Format-CSV-green.svg)](output/mf_stock_holdings.csv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An institutional quantitative dataset capturing official **Monthly Mutual Fund Equity Portfolio Holdings** across India's leading Asset Management Companies (AMCs) including SBI Mutual Fund, HDFC Mutual Fund, and ICICI Prudential Mutual Fund.

Tracks scheme-level equity allocations, number of shares held, market values, and portfolio weights to quantify domestic institutional crowding, accumulation, and distribution across NSE-listed equities.

---

## Dataset Schema (`output/mf_stock_holdings.parquet` / `.csv`)

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `month_end` | `string` | ISO-8601 Month End Snapshot Date (`YYYY-MM-DD`) |
| `amc_name` | `string` | Asset Management Company (e.g. `HDFC Mutual Fund`, `SBI Mutual Fund`) |
| `scheme_name` | `string` | Mutual Fund Scheme Name (e.g. `HDFC Top 100 Fund`, `SBI Bluechip Fund`) |
| `symbol` | `string` | NSE Listed Equity Ticker (e.g. `HDFCBANK`, `ICICIBANK`, `RELIANCE`) |
| `isin` | `string` | Regulatory ISIN Identifier (`^IN[A-Z0-9]{10}$`) |
| `shares_held` | `int64` | Total volume of equity shares held by the fund |
| `market_value_cr` | `float64` | Market value of holding in INR Crores |
| `portfolio_weight_pct` | `float64` | Holding weight as percentage of scheme's equity AUM |
| `source` | `string` | Provenance identifier (`AMFI_MONTHLY_DISCLOSURES`) |

---

## Quick Start (Python / Polars / DuckDB)

```python
import polars as pl

# Read directly from GitHub Raw Parquet
url = "https://github.com/prathmeshgupta/amfi-mutual-fund-stock-holdings/raw/main/output/mf_stock_holdings.parquet"
df = pl.read_parquet(url)

# Find all schemes holding HDFCBANK
hdfc_holders = df.filter(pl.col("symbol") == "HDFCBANK")
print(hdfc_holders.select(["month_end", "scheme_name", "shares_held", "portfolio_weight_pct"]))
```
