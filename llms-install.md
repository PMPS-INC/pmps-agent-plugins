# Installing the PMPS MCP server

PMPS is a remote MCP server. Nothing needs to be downloaded, built or run locally.

1. Add a remote server named `pmps` with the Streamable HTTP transport and the URL `https://api.pmps.ai/mcp`. For Cline, add this to `cline_mcp_settings.json`:

   ```json
   {
     "mcpServers": {
       "pmps": {
         "type": "streamableHttp",
         "url": "https://api.pmps.ai/mcp"
       }
     }
   }
   ```

2. The server uses OAuth with dynamic client registration. When the client opens a browser, the user signs in with a @pmps.ai Google account and approves the agent. Do not ask the user for a client ID or secret.
3. If the client cannot do OAuth, ask the user to create an API key at https://console.pmps.ai/account and add the header `Authorization: Bearer <key>`. Never write the key into a file that is committed to version control.
4. Verify the connection by calling the `get_data_freshness` tool.
