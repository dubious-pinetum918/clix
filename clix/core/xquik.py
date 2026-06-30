"""Optional Xquik read helpers for search workflows."""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

XQUIK_SEARCH_URL = "https://api.xquik.com/v1/x/search"


@dataclass(frozen=True)
class XquikSearchConfig:
    """Configuration for the Xquik search endpoint."""

    api_key: str
    base_url: str = XQUIK_SEARCH_URL
    timeout: float = 30.0


def build_xquik_search_url(
    query: str,
    *,
    query_type: str = "Top",
    cursor: str | None = None,
    limit: int | None = None,
    base_url: str = XQUIK_SEARCH_URL,
) -> str:
    """Build a Xquik search URL with only populated query parameters."""
    params: dict[str, str] = {"q": query, "queryType": query_type}
    if cursor:
        params["cursor"] = cursor
    if limit is not None:
        params["limit"] = str(limit)
    return f"{base_url}?{urlencode(params)}"


def build_xquik_headers(api_key: str) -> dict[str, str]:
    """Build HTTP headers for Xquik API requests."""
    return {
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}",
    }


def search_xquik(
    query: str,
    config: XquikSearchConfig,
    *,
    query_type: str = "Top",
    cursor: str | None = None,
    limit: int | None = None,
    opener: Callable[..., Any] = urlopen,
) -> dict[str, Any]:
    """Run a Xquik search request and return the decoded JSON payload."""
    url = build_xquik_search_url(
        query,
        query_type=query_type,
        cursor=cursor,
        limit=limit,
        base_url=config.base_url,
    )
    request = Request(url, headers=build_xquik_headers(config.api_key), method="GET")
    with opener(request, timeout=config.timeout) as response:
        payload = response.read().decode("utf-8")
    decoded = json.loads(payload)
    if not isinstance(decoded, dict):
        raise ValueError("Xquik search response must be a JSON object")
    return decoded
