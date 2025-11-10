# Publishing Skills MCP Server to GitHub Package Registry

This guide explains how the automated publishing works and how to manually publish if needed.

## Automated Publishing (Recommended)

The Skills MCP Server is automatically published to GitHub Package Registry via GitHub Actions.

**Workflow Triggers:**
- ✅ **Push to main** with changes in `skills-mcp-server/` → Runs tests only
- ✅ **Pull requests** with changes in `skills-mcp-server/` → Runs tests only
- ✅ **Git tags** matching `skills-mcp-server-v*` → Runs tests + publishes
- ✅ **GitHub releases** → Runs tests + publishes
- ✅ **Manual workflow dispatch** → Runs tests + publishes with custom version

### Publishing via Git Tag (Recommended)

1. **Update version in package.json:**
   ```bash
   cd skills-mcp-server
   npm version 1.0.1  # or patch/minor/major
   ```

2. **Create and push a git tag:**
   ```bash
   git add skills-mcp-server/package.json
   git commit -m "Bump skills-mcp-server to v1.0.1"
   git tag skills-mcp-server-v1.0.1
   git push origin main --tags
   ```

3. **Automated workflow runs:**
   - Tests are executed (34 tests)
   - Server is built
   - Package is published to GitHub Package Registry
   - Available at: `@sfc-gh-dflippo/skills-mcp-server@1.0.1`

### Publishing via GitHub Release

1. **Create a new release on GitHub:**
   - Go to: https://github.com/sfc-gh-dflippo/snowflake-dbt-demo/releases/new
   - Tag: `skills-mcp-server-v1.0.0` (must match this pattern)
   - Title: `Skills MCP Server v1.0.0`
   - Description: Release notes and changes
   - Click "Publish release"

2. **Workflow triggers automatically** and publishes the package.

### Manual Publishing via Workflow Dispatch

You can also trigger publishing manually with a custom version:

1. Go to: https://github.com/sfc-gh-dflippo/snowflake-dbt-demo/actions
2. Select "Publish Skills MCP Server" workflow
3. Click "Run workflow"
4. Enter version number (e.g., `1.0.1`)
5. Click "Run workflow"

## Manual Publishing (Alternative)

If you need to publish manually from your local machine:

### Prerequisites

1. **Create GitHub Personal Access Token:**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token" → "Generate new token (classic)"
   - Select scopes: `write:packages`, `read:packages`
   - Copy the token

2. **Configure npm authentication:**
   ```bash
   npm login --scope=@sfc-gh-dflippo --registry=https://npm.pkg.github.com
   # Username: your-github-username
   # Password: your-personal-access-token
   # Email: your-email@example.com
   ```

### Publishing Steps

```bash
cd skills-mcp-server

# Run tests
npm test

# Build
npm run build

# Update version (if needed)
npm version patch  # or minor/major

# Publish
npm publish
```

## For Users: Installing from GitHub Package Registry

Users need to configure npm to authenticate with GitHub Package Registry.

### One-Time Setup

Create or update `~/.npmrc`:

```bash
@sfc-gh-dflippo:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=YOUR_GITHUB_TOKEN
```

**Note:** Users need a GitHub account and personal access token with `read:packages` scope.

### Public Alternative (Future)

For easier public access without authentication, consider publishing to public npm registry:

```bash
npm publish --access public --registry=https://registry.npmjs.org
```

This would allow users to install without GitHub authentication.

## Version Management

The version number in `package.json` should follow semantic versioning:

- **Patch** (`2.0.x`): Bug fixes, minor updates
- **Minor** (`2.x.0`): New features, backward compatible
- **Major** (`x.0.0`): Breaking changes

Update version before publishing:
```bash
npm version patch  # 1.0.0 → 1.0.1
npm version minor  # 1.0.1 → 1.1.0
npm version major  # 1.1.0 → 2.0.0
```

## Troubleshooting

### Permission Denied

If publishing fails with permission error:
- Verify your GitHub token has `write:packages` scope
- Ensure you're authenticated: `npm whoami --registry=https://npm.pkg.github.com`

### Package Already Exists

If the version already exists:
- Update version: `npm version patch`
- Or delete the package version from GitHub Packages UI

### Tests Fail

Publishing will not proceed if tests fail. Fix issues and re-run:
```bash
npm test
```

## Viewing Published Packages

Visit: https://github.com/sfc-gh-dflippo?tab=packages

Or check directly:
```bash
npm view @sfc-gh-dflippo/skills-mcp-server
```

