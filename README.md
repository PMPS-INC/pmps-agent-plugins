# PMPS agent plugins

Plugins, extensions and registry manifests that connect AI agents to the PMPS MCP server:

```
https://api.pmps.ai/mcp
```

The server gives agents Polymarket and Kalshi market search, live outcome probabilities and the organization's tracked set. Agents sign in with OAuth (Google, @pmps.ai accounts only). No API key or client ID is needed: clients register themselves through dynamic client registration. Manage connected agents at <https://console.pmps.ai/mcp>.

## Install

### Claude Code

```bash
claude plugin marketplace add PMPS-INC/pmps-agent-plugins
claude plugin install pmps@pmps-inc
```

Then run `/mcp`, select `pmps` and choose **Authenticate**.

### Claude (web and desktop)

Settings → Connectors → **Add custom connector**, URL `https://api.pmps.ai/mcp`, leave the OAuth fields empty. On Team and Enterprise plans an owner adds it once under Organization settings → Connectors.

### Codex

```bash
codex plugin marketplace add PMPS-INC/pmps-agent-plugins
```

Restart the app, open the **Plugins** directory, pick the **PMPS** marketplace and install `pmps`. You will be asked to sign in on install.

Without the plugin:

```bash
codex mcp add pmps --url https://api.pmps.ai/mcp
codex mcp login pmps
```

### Cursor

[Install MCP server in Cursor](https://cursor.com/en/install-mcp?name=pmps&config=eyJ1cmwiOiJodHRwczovL2FwaS5wbXBzLmFpL21jcCJ9), or add this repository as a team marketplace (Dashboard → Settings → Plugins → Import, `https://github.com/PMPS-INC/pmps-agent-plugins`) to get the plugin with its skill. Then open Cursor Settings → MCP and click **Connect** next to `pmps`.

### GitHub Copilot CLI

```bash
copilot plugin marketplace add PMPS-INC/pmps-agent-plugins
copilot plugin install pmps@pmps-inc
```

### VS Code (GitHub Copilot)

[Install in VS Code](https://vscode.dev/redirect/mcp/install?name=pmps&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Fapi.pmps.ai%2Fmcp%22%7D), or add to `.vscode/mcp.json`:

```json
{ "servers": { "pmps": { "type": "http", "url": "https://api.pmps.ai/mcp" } } }
```

### Gemini CLI

```bash
gemini extensions install https://github.com/PMPS-INC/pmps-agent-plugins
```

Then run `/mcp auth pmps`.

### Other clients

| Client | Configuration |
| --- | --- |
| Windsurf | `~/.codeium/windsurf/mcp_config.json`: `{ "mcpServers": { "pmps": { "serverUrl": "https://api.pmps.ai/mcp" } } }` |
| Zed | `settings.json`: `{ "context_servers": { "pmps": { "url": "https://api.pmps.ai/mcp" } } }` |
| Goose | `goose configure` → Add Extension → Remote Extension (Streamable HTTP) → `https://api.pmps.ai/mcp` |
| Cline | Follow [llms-install.md](llms-install.md) |
| ChatGPT | Settings → Apps → Create (developer mode), URL `https://api.pmps.ai/mcp`, authentication OAuth |
| No OAuth support | Create an API key at <https://console.pmps.ai/account> and send `Authorization: Bearer <key>` to `https://api.pmps.ai/mcp` |

## Repository layout

| Path | Used by |
| --- | --- |
| `.claude-plugin/marketplace.json` | Claude Code marketplace (also read by Copilot CLI) |
| `.agents/plugins/marketplace.json` | Codex / ChatGPT plugin marketplace |
| `.cursor-plugin/marketplace.json` | Cursor team marketplace |
| `.github/plugin/marketplace.json` | GitHub Copilot CLI marketplace |
| `plugins/pmps/.claude-plugin/plugin.json`, `plugins/pmps/.mcp.json` | Claude Code plugin |
| `plugins/pmps/plugin.json`, `plugins/pmps/mcp.json` | [Agent Plugins](https://agent-plugins.org) package: Codex (with `extensions.com.openai`) and Copilot CLI |
| `plugins/pmps/.cursor-plugin/plugin.json` | Cursor plugin |
| `plugins/pmps/skills/pmps-markets/SKILL.md` | Shared skill for every plugin host |
| `gemini-extension.json`, `GEMINI.md` | Gemini CLI extension (must stay at the repository root) |
| `server.json` | Official MCP Registry entry |
| `llms-install.md`, `assets/logo-400.png` | Cline MCP Marketplace submission |

## Releasing

1. Bump `version` in every manifest (`python scripts/validate.py` fails when they differ).
2. Run `python scripts/validate.py`, and `claude plugin validate .` if Claude Code is installed.
3. Commit and push. Claude Code, Codex, Cursor and Copilot pick up the new version when users update the marketplace.

## Publishing to public directories

Access is limited to @pmps.ai accounts, so the public directories below would list a server that outside users cannot sign in to. Most reviews require a reviewer test account, a privacy policy and a support contact; prepare those first.

- **MCP Registry**: `mcp-publisher login dns --domain pmps.ai --private-key …` (TXT record on `pmps.ai`), then `mcp-publisher publish` from the repository root.
- **Anthropic directory** (Claude and Claude Code): submit the plugin and remote connector through Anthropic's submission form.
- **OpenAI plugin directory** (ChatGPT and Codex): submit through the plugin submission portal, choosing **With MCP**.
- **Cursor Marketplace**: submit the repository at cursor.com/marketplace.
- **Gemini CLI gallery**: add the `gemini-cli-extension` topic to this GitHub repository.
- **Cline MCP Marketplace**: open an issue in `cline/mcp-marketplace` with the repository URL and `assets/logo-400.png`.
