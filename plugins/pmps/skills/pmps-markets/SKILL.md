---
name: pmps-markets
description: Find, compare and track Polymarket and Kalshi prediction markets with the PMPS MCP tools. Use when the user asks about prediction-market odds, event probabilities, Polymarket or Kalshi contracts, or the PMPS tracked set.
---

# PMPS prediction markets

The `pmps` MCP server (https://api.pmps.ai/mcp) exposes Polymarket and Kalshi data. The first call opens a browser for Google sign-in with a @pmps.ai account.

## Workflow

1. **Discover** with `search_markets` (events with outcome previews) or `search_outcomes` (individual contracts). Filter by `query`, `platform`, `categories`, `popular`, `volume_min`, `probability_min`/`probability_max` and `end_after`/`end_before`; sort by `volume`, `end_date` or `probability`. Page with `next_cursor`, keeping the other arguments unchanged.
2. **Drill into an event** with `search_outcomes` and `platform` + `market_id` to list every outcome.
3. **Get current odds** with `get_prices` and outcome IDs (the `id` of outcomes from search results: a Polymarket Gamma market ID or a Kalshi market ticker). Do not pass event IDs, condition IDs or token IDs.
4. **Check freshness** with `get_data_freshness` when timing matters.

## Tracking

- `track_outcomes` and `untrack_outcomes` change a set shared by the **whole organization** (max 1,000 outcomes). Only change it when the user asks, and say what you added or removed.
- `list_tracked_outcomes` shows the set. Tracked outcomes refresh about every minute.

## Reporting

- Probabilities are normalized observations from 0 to 1, not executable quotes. Present them as percentages and name the platform.
- Search results are a discovery snapshot; quote odds from `get_prices` when the user needs current numbers.
- When comparing Polymarket and Kalshi, match outcomes by their rules and end dates, not only by title, and point out differences in resolution criteria.
