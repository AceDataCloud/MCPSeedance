"""Unit tests for utility functions."""

import json

from core.utils import (
    format_batch_task_result,
    format_task_result,
    format_video_result,
)


class TestFormatVideoResult:
    """Tests for format_video_result function."""

    def test_format_success(self, mock_video_response: dict) -> None:
        """Test formatting successful video response."""
        result = format_video_result(mock_video_response)
        data = json.loads(result)
        assert data["success"] is True
        assert data["task_id"] == "test-task-123"
        assert data["data"]["status"] == "succeeded"
        assert "video_url" in data["data"]["content"]

    def test_format_error(self, mock_error_response: dict) -> None:
        """Test formatting error response."""
        result = format_video_result(mock_error_response)
        data = json.loads(result)
        assert data["success"] is False
        assert data["error"]["code"] == "invalid_request"

    def test_format_empty_data(self) -> None:
        """Test formatting response with minimal data."""
        response = {"success": True, "task_id": "123"}
        result = format_video_result(response)
        data = json.loads(result)
        assert data["task_id"] == "123"


class TestFormatTaskResult:
    """Tests for format_task_result function."""

    def test_format_success(self, mock_task_response: dict) -> None:
        """Test formatting successful task response."""
        result = format_task_result(mock_task_response)
        data = json.loads(result)
        assert data["id"] == "task-123"
        assert data["request"]["model"] == "doubao-seedance-1-0-pro-250528"
        assert data["response"]["success"] is True


class TestFormatBatchTaskResult:
    """Tests for format_batch_task_result function."""

    def test_format_batch_success(self, mock_batch_task_response: dict) -> None:
        """Test formatting successful batch task response."""
        result = format_batch_task_result(mock_batch_task_response)
        data = json.loads(result)
        assert data["count"] == 2
        assert len(data["items"]) == 2
        assert data["items"][0]["id"] == "task-123"
        assert data["items"][1]["id"] == "task-789"
