# x-cli — Twitter/X CLI Tool

## Project Overview
A command-line interface for Twitter/X that uses cookie-based authentication (no API keys).
Designed for both humans (rich terminal output) and AI agents (structured JSON output + SKILL.md).

## Tech Stack
- **Python 3.11+** with `uv` for package management
- **typer** for CLI framework
- **rich** for terminal formatting
- **curl_cffi** for HTTP with TLS fingerprinting
- **pydantic** for data models
- **browser_cookie3** for cookie extraction
- **ruff** for linting
- **pytest** for testing

## Project Structure
```
x_cli/
├── __init__.py        # version
├── __main__.py        # python -m x_cli
├── cli/               # typer commands
│   ├── app.py         # main app + global options
│   ├── feed.py        # feed commands
│   ├── tweet.py       # tweet commands
│   ├── user.py        # user commands
│   └── search.py      # search commands
├── core/              # business logic (no CLI deps)
│   ├── api.py         # API methods
│   ├── auth.py        # cookie extraction & management
│   ├── client.py      # HTTP client (curl_cffi)
│   ├── config.py      # TOML config management
│   └── constants.py   # endpoints, headers, defaults
├── models/            # pydantic models
│   ├── tweet.py       # Tweet model
│   └── user.py        # User model
├── display/           # rich formatting (humans only)
│   └── formatter.py   # tweet/user/thread formatting
└── utils/
    ├── filter.py      # engagement scoring
    └── rate_limit.py  # rate limiting with jitter
```

## Commands
- `x feed [--type for-you|following] [--count N]` — timeline
- `x search <query> [--type top|latest|photos|videos]` — search
- `x tweet <id>` — view tweet + thread
- `x user <handle>` — user profile + recent tweets
- `x post <text> [--reply-to ID]` — post tweet
- `x delete <id>` — delete tweet
- `x like/unlike <id>` — like operations
- `x retweet/unretweet <id>` — retweet operations
- `x bookmark/unbookmark <id>` — bookmark operations
- `x bookmarks` — list bookmarks
- `x auth` — authenticate / check auth status
- `x config` — manage config

## Conventions
- All commands support `--json` flag for structured JSON output
- Non-TTY detection: auto-switch to JSON when piped
- Exit codes: 0 success, 1 general error, 2 auth error, 3 rate limit
- Atomic commits with descriptive messages
- Never commit secrets (.env, cookies, tokens)
- Use `ruff` for formatting and linting before commits
- Tests in `tests/` mirroring `x_cli/` structure

## Git Config
- User: spideystreet <dhicham.pro@gmail.com>
- Branch strategy: dev branch, merge to main when stable
- Atomic commits, no sensitive data

## Auth Priority
1. Environment variables: `X_AUTH_TOKEN`, `X_CT0`
2. Stored credentials: `~/.config/x-cli/auth.json` (encrypted)
3. Browser cookie extraction (Chrome, Firefox, Edge, Brave)
