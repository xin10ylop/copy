# Analysis scripts

Requires Python 3 and `lz4` (`pip install lz4`). All data is public: Hyperliquid's builder-fill files and its info API.

| Script | What it does | Output |
|---|---|---|
| `01_aggregate_builder_fills.py` | Downloads every daily builder-fill file for Invo's builder address (`0x557e…3c81`) and aggregates it per day, per user and per coin | `fills_agg.pkl` |
| `02_check_file_coverage.py` | Flags days whose published files are partial (they end before 23:00 UTC) | `coverage.json` |
| `03_kpis_cohorts_cascades.py` | Monthly KPIs from complete days, revenue concentration, cohort retention, and "mimic cascade" detection (20+ users opening the same coin and direction within 10 minutes) | stdout |
| `04_sample_true_pnl.py` | Pulls Hyperliquid `portfolio` all-time PnL (includes liquidations, fees and funding) for 300 random traders and the top 100 by fees paid | `sample_pnl.json` |

Aggregate outputs committed in `data/`:
- `invo_daily_kpis.json`: daily volume, builder fees, unique traders, fills and closed PnL, with a `partial` flag.
- `pnl_sample_summary.json`: results of the PnL samples.

Only aggregates are committed. No per-wallet data is included.

**Caveats:**
- Some published daily files are partial, so those days are lower bounds; `02` flags them.
- Closed PnL from builder fills excludes liquidations, so use `04` for real outcomes.
- To analyse another front-end, change the builder address. The same pipeline works for any Hyperliquid builder.
