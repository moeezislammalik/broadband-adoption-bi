# Executive dashboard wireframe

De-identified layout (professional dark theme). No employer branding.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  BROADBAND ADOPTION EXECUTIVE PORTAL          As of: Mar 2026              │
├──────────────┬──────────────────────────────────────────────────────────────┤
│  SLICERS     │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│  State       │  │ Adoption │ │Penetration│ │  Gap %   │ │ YoY Δ pp │        │
│  Region      │  │  78.4%   │ │  85.1%   │ │  6.7%    │ │  +2.3 ▲  │        │
│  Income      │  └──────────┘ └──────────┘ └──────────┘ └──────────┘        │
│  Market Type │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│  Technology  │  │New Starts│ │Downgrades│ │Lift Ratio│ │ Avg MRC  │        │
│  Provider    │  └──────────┘ └──────────┘ └──────────┘ └──────────┘        │
│  Year/Quarter│  [State] [Income] [Urban/Rural] [Technology] [Trend]         │
│              │  ┌────────────────────┬─────────────────────────────────┐  │
│              │  │ State | Adoption % │  █████████████  Horizontal bars  │  │
│              │  │ Texas | 82.1       │  ████████████                     │  │
│              │  │ ...                │                                   │  │
│              │  └────────────────────┴─────────────────────────────────┘  │
└──────────────┴──────────────────────────────────────────────────────────────┘
```

See [`powerbi/report/executive-dashboard-spec.md`](../powerbi/report/executive-dashboard-spec.md) for build details.
