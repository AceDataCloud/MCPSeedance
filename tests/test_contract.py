"""Guards against re-introducing params the API no longer accepts."""

import inspect
from typing import get_args

import pytest
from pydantic import ValidationError

from core.types import OmniReferenceTaskType, SeedanceWebSearchTool
from tools import video_tools


def test_service_tier_is_not_exposed():
    # service_tier was removed from the API spec; the field was ignored and the
    # advertised "flex 50% discount" never existed in the cost rules.
    for name, fn in inspect.getmembers(video_tools, inspect.isfunction):
        if not name.startswith("seedance_"):
            continue
        assert "service_tier" not in inspect.signature(fn).parameters, name


def test_service_tier_is_not_sent():
    source = inspect.getsource(video_tools)
    assert '"service_tier"' not in source


def test_web_search_tool_matches_api_contract():
    tool = SeedanceWebSearchTool(
        type="web_search",
        limit=50,
        max_keyword=1,
        sources=["toutiao", "douyin", "moji", "search_engine"],
    )

    assert tool.model_dump(exclude_none=True) == {
        "type": "web_search",
        "limit": 50,
        "max_keyword": 1,
        "sources": ["toutiao", "douyin", "moji", "search_engine"],
    }

    with pytest.raises(ValidationError):
        SeedanceWebSearchTool(type="web_search", limit=51)

    with pytest.raises(ValidationError):
        SeedanceWebSearchTool(type="unsupported")

    with pytest.raises(ValidationError):
        SeedanceWebSearchTool(type="web_search", unsupported=True)


def test_omni_reference_task_type_matches_api_contract():
    assert set(get_args(OmniReferenceTaskType)) == {"auto", "reference", "edit", "extend"}
