from pathlib import Path

p = Path(__file__).resolve().parent.parent / "models" / "financial_prediction_v3.py"
lines = p.read_text(encoding="utf-8").splitlines(True)
start = next(i for i, l in enumerate(lines) if "FINANCIAL HEALTH PREDICTION - V3.0" in l and l.strip().startswith("print"))
body = lines[start:]
header = lines[:start]
indented = ["    " + l if l.strip() else l for l in body]
p.write_text("".join(header) + "\nif __name__ == \"__main__\":\n" + "".join(indented), encoding="utf-8")
print(f"Wrapped {len(body)} lines")
