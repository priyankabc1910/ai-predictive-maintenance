# AI Predictive Maintenance — Frontend

An industrial reliability console for a predictive maintenance platform. This is the **frontend only**: a fully built, buildable, and running React application driven by mock data, designed so the mock data layer can later be swapped for a real Python/FastAPI + ML backend without touching the UI components.

This project does **not** include a backend, database, authentication, or real ML inference. It renders realistic mock telemetry for 100 machines against dataset FD001 (NASA C-MAPSS convention referenced in the header).

---

## Overview

The console is organized around seven operational views, navigated from a compact icon rail rather than a conventional text sidebar:

| Route            | Page             | Purpose                                                                 |
|-------------------|------------------|--------------------------------------------------------------------------|
| `/`               | Overview         | Fleet reliability hero, RUL trajectories, alerts, fleet grid, risk table, sensor telemetry, activity log |
| `/fleet`          | Fleet            | Full 100-unit machine grid with risk filters, full risk table            |
| `/rul`            | RUL Predictions  | Remaining Useful Life trajectory chart + shortest-RUL ranking             |
| `/anomalies`      | Anomalies        | Anomaly score ranking, active alerts, live sensor panel                  |
| `/maintenance`    | Maintenance      | Work queue grouped by recommended action (Immediate / Schedule / Inspect / Monitor) |
| `/intelligence`   | Intelligence     | Explainable AI: feature attribution and evidence-grounded reasoning       |
| `/reports`        | Reports          | Generated report documents (mock)                                        |

### Visual identity

The design intentionally avoids the generic "sidebar + topbar + stat cards" SaaS dashboard look. It leans into an **industrial command-console** aesthetic:

- **Base palette:** graphite / charcoal / steel (near-black, warm-toned neutrals)
- **Accent:** copper / burnt orange (`--color-copper-500 #c1652f`) — no blue as a primary brand color
- **Secondary:** muted sage green
- **Status colors:** green = healthy, amber = warning/monitoring, red = critical, gray = offline
- **Type:** Inter for UI text, JetBrains Mono for unit IDs, RUL values, timestamps, and other technical identifiers
- Hairline dividers, a subtle background grid motif in the hero, and dense engineering-style layouts (fleet spectrum strip, tile grid, risk table) instead of repeated identical cards

---

## Technology stack

- **React 19** + **TypeScript**
- **Vite** (build tool / dev server)
- **Tailwind CSS v4** (CSS-first `@theme` token system, via `@tailwindcss/vite`)
- **Recharts** — RUL trajectory chart and sensor sparklines
- **Lucide React** — iconography
- **React Router** — client-side routing across the seven views

No backend, database, or authentication libraries are included by design.

---

## Getting started

### Prerequisites

- Node.js 18+ and npm

### Install

```bash
npm install
```

### Run in development

```bash
npm run dev
```

Vite will print a local URL (typically `http://localhost:5173`).

### Build for production

```bash
npm run build
```

Type-checks with `tsc -b` and then produces an optimized bundle in `dist/`.

### Preview the production build locally

```bash
npm run preview
```

### Lint

```bash
npm run lint
```

---

## Mock data

All mock data lives under `src/data/` and is completely separate from components and pages:

| File                        | Contents                                                                 |
|-----------------------------|---------------------------------------------------------------------------|
| `src/data/mockFleetData.ts` | Generates the 100-machine fleet (72 healthy / 20 monitoring / 8 critical), plus five hero units (`UNIT-001`, `UNIT-024`, `UNIT-067`, `UNIT-083`, `UNIT-091`) pinned to the exact values used throughout the UI |
| `src/data/mockRULData.ts`   | Degradation trajectories (predicted RUL vs. operating cycle) for the five hero units |
| `src/data/mockAlerts.ts`    | Active alert records shown in the Alerts rail                             |
| `src/data/mockTelemetry.ts` | Sensor time-series traces for the Sensor Intelligence panel               |
| `src/data/mockActivity.ts`  | System activity / event log entries                                       |

The fleet generator uses a small seeded PRNG (`mulberry32`) so the same 100 machines and distribution appear on every reload, rather than reshuffling randomly.

---

## Component architecture

```
src/
  components/
    layout/        AppShell (page frame), SystemHeader (technical status bar)
    navigation/     NavRail (desktop icon rail), MobileNav (bottom tab bar)
    fleet/          FleetSpectrum (hero), FleetGrid, MachineTile, RiskTable
    rul/            RULTrajectoryChart
    telemetry/      SensorPanel, SensorTrace
    alerts/         AlertRail
    activity/       ActivityTimeline
    ui/             StatusLED, SectionLabel — small shared primitives
  data/             mock data modules (see above)
  types/            telemetry.ts — shared TypeScript interfaces
  pages/            one file per route (Overview, Fleet, RULPredictions,
                     Anomalies, Maintenance, Intelligence, Reports)
  App.tsx           route definitions
  main.tsx          React entry point
  index.css         Tailwind import + industrial design tokens (@theme)
```

Every page composes the same shared components rather than duplicating markup, so a change to (for example) `RiskTable` or `MachineTile` propagates everywhere it's used.

---

## Future ML / API integration

The UI is intentionally decoupled from where its data comes from. The shape every component expects is defined once, in `src/types/telemetry.ts`:

```ts
interface MachineRecord {
  machine_id: string;
  health_score: number;
  rul: number;
  risk_level: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  status: "HEALTHY" | "MONITORING" | "CRITICAL";
  anomaly_score: number;
  trend: "Stable" | "Improving" | "Declining" | "Rapid decline";
  signal: string;
  recommendation: string;
}
```

This mirrors the payload shape described in the project brief (`machine_id, health_score, rul, risk_level, anomaly_score, sensor_values, trend, recommendation`), so it maps directly onto whatever the Python/FastAPI service eventually returns.

To wire up a real backend later:

1. Replace the static exports in `src/data/*.ts` with data-fetching hooks (e.g. `useEffect` + `fetch`, or a library like TanStack Query) that call the FastAPI endpoints.
2. Keep the same exported shapes (`MachineRecord[]`, `RULTrajectory[]`, `AlertRecord[]`, `SensorTrace[]`, `ActivityEvent[]`) so no component code needs to change.
3. Add loading/error states in the pages that consume the data, since mock data is currently always present synchronously.
4. If real-time updates are needed later (WebSockets, polling), that logic belongs in the data layer — the components already re-render on prop/state changes and don't assume anything about how fresh the data is.

Nothing in this repository touches the ML pipeline, notebooks, datasets, or trained models — this is frontend only, as requested.
