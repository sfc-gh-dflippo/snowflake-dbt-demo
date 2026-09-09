---
name: snowflake-connection
description: Choose and configure a Snowflake target authenticator. Use when creating or repairing a Snowflake connection, especially Microsoft Entra ID / Azure AD / OIDC SSO, or when `externalbrowser` fails against an OIDC IdP.
license: Proprietary. See License-Skills for complete terms
---

# Snowflake target connection

`scai` opens Snowflake through Snowflake.Data. Pick the authenticator that matches the identity provider. Do **not** guess; ask if the user is unsure.

## When to use which authenticator

| Situation | Authenticator | Notes |
|-----------|---------------|--------|
| Microsoft Entra ID, Azure AD, or any OIDC IdP | `oauth_authorization_code` | Browser PKCE flow. Required for Entra. |
| Snowflake SAML SSO / classic IdP SSO | `externalbrowser` | Do **not** use this for Entra OIDC. |
| Password + MFA | omit / `username_password_mfa` | Existing default. |
| Programmatic access token | `programmatic_access_token` | Headless / CI. |
| Key-pair | `snowflake_jwt` | Headless / CI. |
| Token already in hand (SPCS) | `oauth` | Non-interactive. |
| Service principal | `oauth_client_credentials` | Non-interactive. |

If a connection using `externalbrowser` fails with an OIDC / Entra / AADSTS error, switch it to `oauth_authorization_code`. Do not keep retrying SAML.

Full field reference: `Snowflake.SnowConvertDesktop/Snowflake.SnowConvert.Cli/docs/entra-oidc-oauth.md`.

## Entra / OIDC (`oauth_authorization_code`)

Requires a desktop session (system browser + loopback listener). Refuse it in containers, CI, or headless Linux (`DISPLAY` / `WAYLAND_DISPLAY` unset). Suggest PAT or key-pair instead.

Required `connections.toml` keys:

- `account`, `user` — `user` is required so Snowflake.Data can cache and refresh tokens
- `authenticator = "oauth_authorization_code"`
- `oauth_client_id`, `oauth_client_secret`
- `oauth_scope` — forwarded verbatim; do not trim or reorder
- `oauth_authorization_url` and `oauth_token_request_url` — both HTTPS, set together
- `oauth_redirect_uri` — **required whenever those external endpoints are set**. Fixed absolute loopback URI registered **exactly** in Entra (scheme, host, port, path). Example: `http://127.0.0.1:8080/`

Do not omit `oauth_redirect_uri` for Entra. The connector's random-port `127.0.0.1` callback is not Entra-compatible (`localhost` any-port does not apply to `127.0.0.1`).

Example:

```toml
[entra_oidc]
authenticator = "oauth_authorization_code"
account = "myorg-myaccount"
user = "first.last@example.com"
oauth_client_id = "<app-client-id>"
oauth_client_secret = "<client-secret>"
oauth_scope = "<scope-the-Entra-app-expects>"
oauth_authorization_url = "https://login.microsoftonline.com/<tenant-id>/oauth2/v2.0/authorize"
oauth_token_request_url = "https://login.microsoftonline.com/<tenant-id>/oauth2/v2.0/token"
oauth_redirect_uri = "http://127.0.0.1:8080/"
```

Select it with `scai … --connection entra_oidc` (or the project's `snowflake_connection`).

## Limits the agent must not ignore

- **Data validation and test generation do not support this authenticator.** Their DTO cannot carry client, endpoints, scope, or redirect. Use PAT, key-pair, or password for those jobs (`CNX0037`).
- **Browser single-flight is process-local** and covers SCAI Jobs/Databases native opens only. Do not start overlapping Authorization Code data-migration / SMA opens; cache the first login, then run them one at a time.
- Never log client secrets, authorization codes, tokens, or full authorize URLs.
