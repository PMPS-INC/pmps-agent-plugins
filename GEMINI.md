# PMPS prediction markets

The `pmps` MCP server (https://api.pmps.ai/mcp) exposes Polymarket and Kalshi data. Sign in with a @pmps.ai Google account when the browser opens (`/mcp auth pmps`).

- Discover with `search_markets` (events) or `search_outcomes` (contracts); pass `platform` + `market_id` to list every outcome of an event. Page with `next_cursor`, keeping other arguments unchanged.
- Get current odds with `get_prices` using outcome `id` values from search results (Polymarket Gamma market ID or Kalshi ticker), not event, condition or token IDs.
- `track_outcomes` / `untrack_outcomes` change a set shared by the whole organization (max 1,000). Change it only when the user asks.
- Probabilities are normalized observations (0–1), not executable quotes. Search results are a snapshot; quote `get_prices` for current numbers and check `get_data_freshness` when timing matters.
- When comparing platforms, match outcomes by rules and end dates, not only titles.
