"""Restructure v3.py: module-level functions, main-only pipeline."""
from pathlib import Path

p = Path(__file__).resolve().parent.parent / "models" / "financial_prediction_v3.py"
text = p.read_text(encoding="utf-8")
lines = text.splitlines(keepends=True)

# Fix dataset paths
text = text.replace(
    "TRAIN_PATH = os.path.join(BASE_PATH, 'Train.csv')",
    "TRAIN_PATH = os.path.join(BASE_PATH, 'datasets', 'Train.csv')",
)
text = text.replace(
    "TEST_PATH = os.path.join(BASE_PATH, 'Test.csv')",
    "TEST_PATH = os.path.join(BASE_PATH, 'datasets', 'Test.csv')",
)
lines = text.splitlines(keepends=True)

# Find function block
start_helpers = next(i for i, l in enumerate(lines) if l.startswith("def map_to_binary"))
end_helpers = next(i for i, l in enumerate(lines) if l.startswith("# APPLY FEATURE ENGINEERING"))
helpers = lines[start_helpers:end_helpers]

# Fix raw_feature_cols inside create_v3_features
helpers_text = "".join(helpers)
helpers_text = helpers_text.replace(
    "features['total_missing_count'] = df[raw_feature_cols].isnull().sum(axis=1)",
    "features['total_missing_count'] = df.isnull().sum(axis=1)",
)
helpers_text = helpers_text.replace(
    "features['missing_pct'] = features['total_missing_count'] / len(raw_feature_cols)",
    "features['missing_pct'] = features['total_missing_count'] / max(len(df.columns), 1)",
)
helpers = helpers_text.splitlines(keepends=True)

# Pipeline: from first banner print through end, excluding helpers
start_pipe = next(i for i, l in enumerate(lines) if "FINANCIAL HEALTH PREDICTION - V3.0" in l)
pipe_parts = lines[start_pipe:start_helpers] + lines[end_helpers:]

header = lines[:start_pipe]
footer_indented = ["    " + l if l.strip() else l for l in pipe_parts]

out = (
    "".join(header)
    + "".join(helpers)
    + "\n\n"
    + "if __name__ == '__main__':\n"
    + "".join(footer_indented)
)
p.write_text(out.replace("if __name__ == '__main__':", 'if __name__ == "__main__":'), encoding="utf-8")
print("Restructured", p)
