# Driver Bootstrap (Oracle / Teradata)

Canonical flow for resolving a NuGet `.NET` driver before any operation that talks to Oracle or Teradata. The first such operation is typically the MCP `configure` tool call (which runs `scai connection test` internally), or a direct `scai code extract` if connection setup is already done.

**Use this any time a `.nupkg` driver is required.** Consumer skills (`oracle-connection`, `teradata-connection`, `extract-code-units`) should link here instead of duplicating the flow.

## Dialect parameters

Resolve these once for the dialect you are working with, then substitute them into the steps below.

| Parameter | Oracle | Teradata |
|-----------|--------|----------|
| `<dialect>` | `oracle` | `teradata` |
| `<package>` | `Oracle.ManagedDataAccess.Core` | `Teradata.Client.Provider` |
| `<driver_file>` | `Oracle.ManagedDataAccess.Core.nupkg` | `Teradata.Client.Provider.nupkg` |
| `<cache_dir>` | `~/.snowflake/scai/drivers/oracle/` | `~/.snowflake/scai/drivers/teradata/` |
| `<nuget_url>` | `https://www.nuget.org/api/v2/package/Oracle.ManagedDataAccess.Core` | `https://www.nuget.org/api/v2/package/Teradata.Client.Provider` |

## Naming guard

**Never call this a JDBC driver.** It is a `.NET` driver shipped as a NuGet package. When talking to the user, refer to it as "the Oracle driver" / "the Teradata driver" or "the NuGet package".

## Flow

### 1a. Check the cache

SCAI caches the driver at `<cache_dir>` and reuses it machine-wide. If a `.nupkg` or `.dll` is present, the driver is already resolved and no further bootstrap is needed — skip directly to **1e**.

```bash
# macOS / Linux
ls <cache_dir>*.nupkg <cache_dir>*.dll 2>/dev/null
```

```powershell
# Windows PowerShell — <cache_dir> uses %USERPROFILE%\.snowflake\... with backslashes
Get-ChildItem -Path "<cache_dir>" -Filter *.nupkg,*.dll -ErrorAction SilentlyContinue
```

If nothing is listed, continue to 1b.

### 1b. Cache miss — ask how to provide the driver

If the cache is empty, ask the user how to provide the driver. Use a structured question prompt (e.g. `ask_user_question`) — **do not** narrate the decision in prose first ("Per the bootstrap flow, I need to ask…", "The driver is not cached, so I have to ask before downloading…"). Just ask.

**Question text:**

> The <dialect> driver (`<driver_file>`) is required but isn't cached on this machine. How would you like to provide it?
>
> 1. **I already have it** — I'll give you the absolute path to the `.nupkg` (or `.dll`).
> 2. **Download it for me** — fetch it from NuGet (`<nuget_url>`).

Take **Branch A** (1c) on answer 1, **Branch B** (1d) on answer 2.

**User-facing language rules** (apply to every prompt and status message in this flow):

- Never mention "the bootstrap flow", "the skill", "1a/1b/1c/1d", "the reference doc", "Branch A/B", or any other internal label. Those exist for the agent, not the user.
- Don't pre-announce that you're going to ask a question — just ask it.
- Don't justify the question with permission-policy language ("I need your consent before downloading"). The question itself implies that.
- After the user answers, don't echo back the procedural label ("Got it, going down Branch B"). Just do the next thing.

### 1c. Branch A — user-provided path

1. Take the absolute path from the user.
2. Validate the file exists:

   ```bash
   ls <PATH_TO_NUPKG_OR_DLL>
   ```

3. Record the path. The first call that uses the driver (typically the consuming skill's `configure(... driver_path=<PATH>)` in 1e) will copy it into `<cache_dir>` so subsequent calls can omit the path.

### 1d. Branch B — download the driver

Run the appropriate command (do not just describe it — execute it):

```bash
# macOS / Linux
curl -L -o <driver_file> <nuget_url>
```

```powershell
# Windows PowerShell
curl.exe -L -o <driver_file> <nuget_url>
```

Note the full path to the resulting `.nupkg`. The first call that uses the driver will copy it into `<cache_dir>`.

### 1e. First driver-using invocation

The consuming skill is responsible for the actual call. For `oracle-connection` / `teradata-connection`, this is the `configure` MCP tool call that triggers the connection test:

- **After Branch A / B (driver not yet cached):**

  ```
  configure(source_connection=<CONNECTION_NAME>, driver_path=<PATH_TO_NUPKG>)
  ```

  The MCP server invokes `scai connection test --driver-path <PATH>` internally, which copies the driver into `<cache_dir>`.

- **After 1a hit (driver already cached):**

  ```
  configure(source_connection=<CONNECTION_NAME>)
  ```

For other consumers (e.g., `scai code extract` invoked directly outside the configure flow), include `--driver-path <PATH>` on the first such command after Branch A or B.

Once the cache is populated, every subsequent operation for `<dialect>` — even in other projects — can omit the path.

## Failure modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `Driver not found` | `driver_path` was omitted on first use, or the cached file is corrupt | Re-resolve through 1a–1e, passing `driver_path` on the first invocation |
| `curl: (22) … 404` | NuGet feed temporarily unreachable | Retry, or fall back to Branch A with a manually downloaded copy |
| Path provided in Branch A is wrong | Typo / file moved | Re-validate with `ls <PATH>` and re-prompt |

## CHECKPOINT

Before continuing in the consuming skill, confirm:

- [ ] Driver is resolved via 1a (cached), 1c (user path), or 1d (downloaded)
- [ ] If 1c or 1d, the next driver-using call will include `driver_path=<PATH>` (or `--driver-path` for direct scai commands)
- [ ] The user has not been asked to do anything they did not opt into (no silent downloads)
