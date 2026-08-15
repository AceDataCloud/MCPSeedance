"""Regression tests for async task terminal-state guidance."""

import json

from core.utils import format_task_result


def test_explicit_response_failure_without_state_is_terminal():
    result = json.loads(
        format_task_result(
            {
                "id": "failed-task",
                "state": "",
                "response": {
                    "success": False,
                    "error": {"code": "bad_request", "message": "invalid input"},
                },
            }
        )
    )

    guidance = result["mcp_task_polling"]
    assert guidance["is_failed"] is True
    assert guidance["should_poll"] is False
    assert guidance["terminal_state_reached"] is True
    assert guidance["recommended_action"] == "stop"


def test_missing_success_remains_pending():
    result = json.loads(
        format_task_result({"id": "pending-task", "state": "", "response": {"data": []}})
    )

    guidance = result["mcp_task_polling"]
    assert guidance["is_complete"] is False
    assert guidance["is_failed"] is False
    assert guidance["should_poll"] is True
    assert guidance["terminal_state_reached"] is False


from unittest.mock import AsyncMock, patch

import pytest

from tools.task_tools import seedance_get_task


@pytest.mark.asyncio
async def test_failed_task_does_not_sleep():
    task = {"id": "failed-task", "state": "", "response": {"success": False}}
    with (
        patch("tools.task_tools.client.query_task", new=AsyncMock(return_value=task)),
        patch("tools.task_tools.asyncio.sleep", new=AsyncMock()) as sleep,
    ):
        result = await seedance_get_task(task_id="failed-task")

    sleep.assert_not_awaited()
    guidance = json.loads(result)["mcp_task_polling"]
    assert guidance["is_failed"] is True
    assert guidance["should_poll"] is False
