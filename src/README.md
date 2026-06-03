# Web Application (`src/`)

Next.js front end for FinHealth: survey flow, results, reports, and a demo prediction API.

| Path | Role |
|------|------|
| `app/page.tsx` | Landing page |
| `app/survey/` | Multi-step business survey |
| `app/results/` | Risk category and recommendations |
| `app/reports/` | Research-style reporting views |
| `app/api/health/` | Health check |
| `app/api/predict/` | Demo heuristic prediction (not the Python LightGBM model) |
| `components/` | Navbar, footer, API status |
| `lib/api.ts` | Client API helpers |

---

## Stack

| Layer | Technology |
|-------|------------|
| Framework | Next.js (App Router) |
| UI | React, TypeScript, Tailwind CSS |

---

## Run locally

From repository root:

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

---

## Environment

Set `NEXT_PUBLIC_API_URL` in `.env.local` if connecting to an external inference service. Env files are gitignored — see root [`.gitignore`](../.gitignore).

---

## ML vs demo API

| System | Location |
|--------|----------|
| Production ML (LightGBM v3) | [`financial-prediction-model/`](../financial-prediction-model/README.md) |
| Web demo scorer | `app/api/predict/route.ts` |

Wire the Python model behind an API separately if you want live ML predictions in the UI.
