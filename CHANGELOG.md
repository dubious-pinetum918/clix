# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.1] - 2026-03-15

### Added
- MCP tools: `get_user_tweets`, `get_user_likes`, `get_followers`, `get_following` (42 tools total)
- Pagination cursor parameter on all read MCP tools (`get_feed`, `search`, `list_bookmarks`, `get_list_timeline`, `get_list_members`)

### Fixed
- Structured error responses with `status_code`, `retry`, `retry_after_seconds` fields
- Rate limit errors now include `retry_after` from API headers
- Auth, rate limit, and stale endpoint errors have distinct retry guidance

## [0.3.0] - 2026-03-15

### Added

#### Social Actions
- `clix follow/unfollow <handle>` — follow and unfollow users
- `clix block/unblock <handle>` — block and unblock users
- `clix mute/unmute <handle>` — mute and unmute users

#### Content
- `clix post <text> --image FILE` — image upload support (up to 4 images, 5MB each)
- `clix schedule <text> --at <time>` — schedule tweets for future posting
- `clix scheduled` — list scheduled tweets
- `clix unschedule <id>` — cancel a scheduled tweet
- `clix download <tweet-id>` — download media (images/videos) from tweets
- `clix tweet <id> --export FILE` — export Twitter Articles as Markdown

#### Discovery
- `clix trending` — show trending topics with tweet volume
- `clix tweets <id1> <id2> ...` — batch fetch multiple tweets
- `clix users <handle1> <handle2> ...` — batch fetch multiple users

#### Lists
- `clix lists` — view your Twitter Lists
- `clix lists view <id>` — read tweets from a list
- `clix lists create <name>` — create a list
- `clix lists delete <id>` — delete a list
- `clix lists members <id>` — view list members
- `clix lists add-member/remove-member <id> <handle>` — manage list members
- `clix lists pin/unpin <id>` — pin/unpin lists

#### Direct Messages
- `clix dm inbox` — view DM conversations
- `clix dm send <handle> <text>` — send a DM

#### Output Modes
- `--compact` / `-c` — token-optimized JSON for AI agents
- `--yaml` — YAML output format
- `--full-text` — disable text truncation in rich display

#### Infrastructure
- `CLIX_PROXY` env var + `[network] proxy` config for HTTP/SOCKS5 proxies
- `X-Client-Transaction-Id` header on all requests (anti-detection)
- Full browser cookie forwarding (all ~15-20 cookies, not just 2)
- Chrome multi-profile support for cookie extraction (`--profile`, `--list-profiles`)
- `clix doctor` — diagnostic command (system info, auth, connectivity, cache)

#### MCP Server
- 38 tools (up from 14): all new commands exposed as MCP tools

### Changed
- Output mode system unified with `get_output_mode()` helper
- `XClient` now supports `proxy`, `rest_post()`, `rest_get()`, `graphql_post_raw()` methods

### Fixed
- Fallback query IDs for operations removed from X.com JS bundles (`SearchTimeline`, `CreateRetweet`, `CreateBookmark`, `DeleteBookmark`)
- Duplicate `_get_headers()` call dropping `X-Client-Transaction-Id` header
- `doctor` cookie validation using removed REST endpoint (switched to GraphQL `Viewer`)

## [0.2.0] - 2026-03-11

### Added
- Runtime extraction of GraphQL operation IDs from X.com JS bundles (`clix/core/endpoints.py`)
- Per-operation feature switch extraction — only sends the features each query needs
- Disk + memory cache for extracted endpoints (`~/.config/clix/graphql_ops.json`, 24h TTL)
- Auto-retry on HTTP 404 with cache invalidation (stale operation IDs)
- Full browser-like headers (Client Hints, Sec-Fetch-*) for Cloudflare bypass
- Runtime Chrome impersonation target detection (`best_chrome_target()`)
- Integration tests against live X.com

### Changed
- GraphQL endpoints are no longer hardcoded — resolved dynamically at runtime
- Feature flags are no longer hardcoded — extracted from `__INITIAL_STATE__` and scoped per-operation
- `Bookmarks` operation renamed to `BookmarkSearchTimeline` (X.com API change)

### Fixed
- HTTP 404 on GraphQL endpoints due to stale hardcoded operation IDs (closes #9)
- HTTP 503 from Cloudflare due to missing browser-like headers

## [0.1.0] - 2026-03-09

### Added
- Initial release
- CLI commands: feed, search, tweet, user, post, delete, like/unlike, retweet/unretweet, bookmark/unbookmark, bookmarks, auth, config
- MCP server with 14 tools (stdio transport)
- Cookie-based authentication (browser extraction, env vars, manual)
- Rich terminal output + `--json` flag for piped/scripted usage
- TLS fingerprinting via curl_cffi
