"""Pytest configuration and fixtures."""

import os
import sys
from pathlib import Path

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load .env file BEFORE any other imports
from dotenv import load_dotenv

load_dotenv(dotenv_path=project_root / ".env")

# Set default log level for tests
os.environ.setdefault("LOG_LEVEL", "DEBUG")


@pytest.fixture
def api_token() -> str:
    """Get API token from environment for integration tests."""
    token = os.environ.get("ACEDATACLOUD_API_TOKEN", "")
    if not token:
        pytest.skip("ACEDATACLOUD_API_TOKEN not configured for integration tests")
    return token


@pytest.fixture
def mock_video_response() -> dict:
    """Mock successful video generation response."""
    return {
        "success": True,
        "task_id": "test-task-123",
        "trace_id": "test-trace-456",
        "data": {
            "id": "cgt-test-789",
            "model": "doubao-seedance-1-0-pro-250528",
            "status": "succeeded",
            "content": {
                "video_url": "https://platform.cdn.acedata.cloud/seedance/test-task-123.mp4",
            },
            "seed": 10,
            "resolution": "720p",
            "ratio": "16:9",
            "duration": 5,
            "framespersecond": 24,
            "service_tier": "default",
            "usage": {
                "completion_tokens": 108900,
                "total_tokens": 108900,
            },
            "created_at": 1743414619,
            "updated_at": 1743414673,
        },
    }


@pytest.fixture
def mock_task_response() -> dict:
    """Mock task query response."""
    return {
        "id": "task-123",
        "created_at": 1743414619.0,
        "request": {
            "model": "doubao-seedance-1-0-pro-250528",
            "content": [{"type": "text", "text": "A test video"}],
        },
        "response": {
            "success": True,
            "task_id": "task-123",
            "trace_id": "trace-456",
            "data": {
                "id": "cgt-test-789",
                "model": "doubao-seedance-1-0-pro-250528",
                "status": "succeeded",
                "content": {
                    "video_url": "https://platform.cdn.acedata.cloud/seedance/task-123.mp4",
                },
                "resolution": "720p",
                "ratio": "16:9",
                "duration": 5,
            },
        },
    }


@pytest.fixture
def mock_batch_task_response() -> dict:
    """Mock batch task query response."""
    return {
        "items": [
            {
                "id": "task-123",
                "created_at": 1743414619.0,
                "request": {
                    "model": "doubao-seedance-1-0-pro-250528",
                    "content": [{"type": "text", "text": "First test video"}],
                },
                "response": {
                    "success": True,
                    "task_id": "task-123",
                    "data": {
                        "id": "cgt-test-789",
                        "status": "succeeded",
                        "content": {
                            "video_url": "https://platform.cdn.acedata.cloud/seedance/task-123.mp4",
                        },
                    },
                },
            },
            {
                "id": "task-789",
                "created_at": 1743414700.0,
                "request": {
                    "model": "doubao-seedance-1-0-pro-250528",
                    "content": [{"type": "text", "text": "Second test video"}],
                },
                "response": {
                    "success": True,
                    "task_id": "task-789",
                    "data": {
                        "id": "cgt-test-012",
                        "status": "succeeded",
                        "content": {
                            "video_url": "https://platform.cdn.acedata.cloud/seedance/task-789.mp4",
                        },
                    },
                },
            },
        ],
        "count": 2,
    }


@pytest.fixture
def mock_error_response() -> dict:
    """Mock error response."""
    return {
        "success": False,
        "error": {
            "code": "invalid_request",
            "message": "Invalid parameters provided",
        },
    }
