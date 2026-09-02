# Python Data Pipeline Modules

A collection of small, self-contained Python reference scripts covering concurrency, OS utilities, and `pandas` data-reconciliation patterns — built while working through real ERP/data-analyst problems (Sales Order pricing, target calculation, and reconciliation). Every script is directly runnable (`python3 <path>`) and has no external state beyond what it creates itself.

**Flagship script:** [`pandas/05_realization_pct_pipeline.py`](pandas/05_realization_pct_pipeline.py) — a full walkthrough that takes raw Sales Order line items through multi-tier fallback pricing, MRP-tiered target calculation, SO-level aggregation, and a Realization % formula (accounting for commission, freight, and payment terms), ending in a status assignment. It mirrors a real production investigation into Sales Order Realization % discrepancies.

## Requirements

```
pip install -r requirements.txt
```

(Only `pandas` — everything else uses the standard library.)

## Contents

### `threading/` — concurrency fundamentals

| Script | Demonstrates |
|---|---|
| `01_no_threading_baseline.py` | Running two tasks sequentially — a baseline to compare against |
| `02_threading_basics.py` | Running the same two tasks concurrently with `threading.Thread` |
| `03_daemon_threads.py` | Daemon threads getting force-killed when the main program exits |
| `04_thread_safe_gui_updates.py` | The GUI-safe update pattern (background threads push to a queue, only the main thread applies updates) — the pattern behind Tkinter's `mainloop()` |
| `05_race_condition_demo.py` | A race condition on a shared counter — output varies run to run |
| `06_race_condition_with_lock.py` | The same race condition made reproducible, then fixed with `threading.Lock` |

### `utilities/` — standard library utilities

| Script | Demonstrates |
|---|---|
| `01_os_path_basics.py` | `os.path.join`, `os.path.exists`, `os.makedirs`, `os.environ` |
| `02_os_path_advanced.py` | `os.path.basename`/`dirname`/`splitext`/`abspath`, `isfile`/`isdir`, and a timestamped-filename pattern |
| `03_atexit_cleanup.py` | Registering a cleanup function that runs automatically on exit |
| `04_atexit_on_crash.py` | `atexit` cleanup still running after an unhandled exception |
| `05_logging_setup.py` | `logging.basicConfig` with the 5 standard severity levels, writing to a file |

### `pandas/` — data reconciliation patterns

| Script | Demonstrates |
|---|---|
| `01_merge_left_join.py` | A basic `merge(how='left')` join, including unmatched rows becoming `NaN` |
| `02_merge_fallback_pricing.py` | A multi-tier merge fallback: try one price list, then fall back to the next for whatever's still missing |
| `03_groupby_aggregation.py` | Rolling item-level rows up to order-level totals with `groupby` + `sum`, and why `reset_index()` matters |
| `04_apply_custom_business_rules.py` | `DataFrame.apply(axis=1)` to run a custom per-row business rule |
| `05_realization_pct_pipeline.py` | **Flagship** — the full pipeline described above |

## Notes

- A couple of scripts (`threading/04`, `threading/05`) are intentionally non-deterministic — they demonstrate real race conditions and thread interleaving, so their output can vary between runs. That's the point, not a bug.
- `utilities/01_os_path_basics.py` and `utilities/05_logging_setup.py` create local files/folders (`reports/`, `app.log`) when run; both are gitignored.
