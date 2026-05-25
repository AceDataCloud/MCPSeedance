"""Utility functions for Seedance MCP server."""

import json
from typing import Any


def _with_submission_guidance(
    data: dict[str, Any], poll_tool: str, batch_poll_tool: str | None = None
) -> dict[str, Any]:
    payload = dict(data)
    task_id = payload.get("task_id")
    if not task_id:
        return payload

    payload["mcp_async_submission"] = {
        "task_id": task_id,
        "poll_tool": poll_tool,
        "batch_poll_tool": batch_poll_tool,
        "recommended_action": "poll",
        "should_poll": True,
        "terminal_state_reached": False,
        "polling_interval_seconds": 15,
        "max_poll_attempts": 100,
        "expected_wait_seconds": 600,
        "next_step": (
            f'Call {poll_tool}(task_id="{task_id}") to poll until the task completes '
            f"and the final media URLs are available. "
            f"IMPORTANT: Media generation typically takes 1-5 minutes. "
            f"Wait at least 15 seconds between each poll. "
            f"Keep polling for up to 100 attempts. Do NOT stop early — the task is still running."
        ),
    }
    return payload


def _with_task_guidance(
    data: dict[str, Any], poll_tool: str, batch_poll_tool: str | None = None
) -> dict[str, Any]:
    payload = dict(data)
    task_id = payload.get("id") or payload.get("task_id")
    if not task_id:
        return payload

    state = str(payload.get("state", "")).lower()
    response = payload.get("response", {})
    response_success = response.get("success", False) if isinstance(response, dict) else False
    top_level_success = (
        payload.get("success", False) if isinstance(payload.get("success", False), bool) else False
    )

    is_complete = (
        state in {"complete", "completed", "succeeded", "success"}
        or response_success
        or top_level_success
    )
    is_failed = state in {"failed", "error", "cancelled", "canceled"}
    should_poll = not (is_complete or is_failed)

    payload["mcp_task_polling"] = {
        "task_id": task_id,
        "poll_tool": poll_tool,
        "batch_poll_tool": batch_poll_tool,
        "recommended_action": "poll" if should_poll else "stop",
        "should_poll": should_poll,
        "terminal_state_reached": not should_poll,
        "is_complete": is_complete,
        "is_failed": is_failed,
        "state": state,
        "polling_interval_seconds": 15,
        "max_poll_attempts": 100,
        "next_step": (
            "Task is complete. Stop polling and present final media URLs to the user."
            if is_complete
            else (
                "Task reached a terminal failure/cancelled state. Stop polling and report the failure details to the user."
                if is_failed
                else (
                    f"The task is still pending or processing. "
                    f'Wait 15 seconds, then call {poll_tool}(task_id="{task_id}") again. '
                    f"IMPORTANT: Media generation typically takes 1-5 minutes. "
                    f"Keep polling — do NOT give up or tell the user it failed. "
                    f"You should poll at least 100 times before considering the task stuck."
                )
            )
        ),
    }
    return payload


def format_video_result(data: dict[str, Any]) -> str:
    """Format video generation result as JSON.

    Args:
        data: API response dictionary

    Returns:
        JSON string representation of the result
    """
    return json.dumps(
        _with_submission_guidance(data, "seedance_get_task", "seedance_get_tasks_batch"),
        ensure_ascii=False,
        indent=2,
    )


def format_task_result(data: dict[str, Any]) -> str:
    """Format task query result as JSON.

    Args:
        data: API response dictionary

    Returns:
        JSON string representation of the result
    """
    return json.dumps(
        _with_task_guidance(data, "seedance_get_task", "seedance_get_tasks_batch"),
        ensure_ascii=False,
        indent=2,
    )


def format_batch_task_result(data: dict[str, Any]) -> str:
    """Format batch task query result as JSON.

    Args:
        data: API response dictionary

    Returns:
        JSON string representation of the result
    """
    return json.dumps(data, ensure_ascii=False, indent=2)
