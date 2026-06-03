# Scripts

Optional maintenance utilities for regenerating Jupyter notebooks from source templates. **Not required** for training or EDA day to day.

| Script | Purpose |
|--------|---------|
| `build_notebooks.py` | Writes `models/financial_prediction_v3.ipynb` and `eda/comprehensive_eda.ipynb` |
| `build_eda_notebook.py` | EDA cell definitions (imported by `build_notebooks.py`) |
| `restructure_v3.py` | One-off helper to organize `financial_prediction_v3.py` module layout |
| `wrap_main_guard.py` | One-off helper for `__main__` guard |

---

## Regenerate notebooks

```bash
cd financial-prediction-model
python scripts/build_notebooks.py
```

Edit `build_eda_notebook.py` or `build_notebooks.py` first if you change notebook structure, then rerun the command above.

---

## Note

Prefer editing and running notebooks directly unless you are batch-updating notebook structure across the project.
