# FinHealth - Next.js App

A financial health prediction platform for African SMEs, built with Next.js 14, TypeScript, and Tailwind CSS.

## Features

- **Home Page** - Landing page with model performance metrics and insights
- **Survey Page** - Comprehensive financial health questionnaire
- **Results Page** - Visualized survey results with radar charts and recommendations
- **Reports Page** - Gallery of financial insights and trends

## Getting Started

### Prerequisites

- Node.js 18.17 or later
- npm, yarn, or pnpm

### Installation

1. Navigate to the Next.js app directory:
   ```bash
   cd nextjs-app
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
nextjs-app/
├── src/
│   ├── app/
│   │   ├── layout.tsx          # Root layout with Navbar & Footer
│   │   ├── page.tsx            # Home page
│   │   ├── globals.css         # Global styles
│   │   ├── survey/
│   │   │   ├── layout.tsx      # Survey-specific layout
│   │   │   └── page.tsx        # Survey form
│   │   ├── results/
│   │   │   └── page.tsx        # Results display
│   │   └── reports/
│   │       └── page.tsx        # Reports gallery
│   └── components/
│       ├── Navbar.tsx          # Navigation component
│       └── Footer.tsx          # Footer component
├── tailwind.config.ts          # Tailwind configuration
├── package.json
└── tsconfig.json
```

## Navigation

All pages are linked together:
- **Logo/FinHealth** → Home (`/`)
- **Reports** (nav link) → Reports (`/reports`)
- **Take Survey** (button) → Survey (`/survey`)
- Survey submission → Results (`/results`)
- Results "Full Report" → Reports (`/reports`)

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Font**: Space Grotesk
- **Icons**: Material Symbols Outlined

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
