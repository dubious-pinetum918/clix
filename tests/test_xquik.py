"""Tests for optional Xquik search helpers."""

from __future__ import annotations

import json
from typing import Any
from urllib.request import Request

import pytest

from clix.core.xquik import (
    XquikSearchConfig,
    build_xquik_headers,
    build_xquik_search_url,
    search_xquik,
)


class FakeResponse:
    """Minimal context manager for urllib response tests."""

    def __init__(self, payload: object) -> None:
        self.payload = payload

    def __enter__(self) -> FakeResponse:
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def read(self) -> bytes:
        return json.dumps(self.payload).encode("utf-8")


def test_build_xquik_search_url_uses_source_truth_params() -> None:
    url = build_xquik_search_url(
        "open source ai",
        query_type="Latest",
        cursor="abc",
        limit=25,
    )

    assert url == (
        "https://xquik.com/api/v1/x/tweets/search?"
        "q=open+source+ai&queryType=Latest&cursor=abc&limit=25"
    )


def test_build_xquik_headers_uses_api_key_header() -> None:
    assert build_xquik_headers("test-key") == {
        "Accept": "application/json",
        "x-api-key": "test-key",
    }


def test_search_xquik_decodes_json_response() -> None:
    captured: dict[str, Any] = {}

    def fake_opener(request: Request, *, timeout: float) -> FakeResponse:
        captured["url"] = request.full_url
        captured["api_key"] = request.headers["X-api-key"]
        captured["timeout"] = timeout
        return FakeResponse({"data": [{"id": "1"}]})

    result = search_xquik(
        "mcp",
        XquikSearchConfig(api_key="test-key", base_url="https://example.test/search", timeout=3),
        opener=fake_opener,
    )

    assert result == {"data": [{"id": "1"}]}
    assert captured == {
        "url": "https://example.test/search?q=mcp&queryType=Latest",
        "api_key": "test-key",
        "timeout": 3,
    }


def test_search_xquik_rejects_non_object_response() -> None:
    def fake_opener(_request: Request, *, timeout: float) -> FakeResponse:
        assert timeout == 30.0
        return FakeResponse(["not-object"])

    with pytest.raises(ValueError, match="JSON object"):
        search_xquik("mcp", XquikSearchConfig(api_key="test-key"), opener=fake_opener)
