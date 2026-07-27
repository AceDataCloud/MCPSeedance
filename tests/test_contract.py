"""Guards against re-introducing params the API no longer accepts."""

import inspect

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
