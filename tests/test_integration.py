"""
Integration tests for Seedance MCP Server.

These tests make REAL API calls to verify all tools work correctly.
Run with: pytest tests/test_integration.py -v -s

Note: These tests require ACEDATACLOUD_API_TOKEN to be set.
They are skipped in CI environments without the token.
"""

import os
import sys

import pytest

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# Check if API token is configured
HAS_API_TOKEN = bool(os.getenv("ACEDATACLOUD_API_TOKEN"))

# Decorator to skip tests that require API token
requires_api_token = pytest.mark.skipif(
    not HAS_API_TOKEN,
    reason="ACEDATACLOUD_API_TOKEN not configured - skipping integration test",
)


class TestVideoTools:
    """Integration tests for video generation tools."""

    @requires_api_token
    @pytest.mark.asyncio
    async def test_generate_video_basic(self) -> None:
        """Test basic video generation with real API."""
        from tools.video_tools import seedance_generate_video

        result = await seedance_generate_video(
            prompt="A simple test video, blue sky with clouds",
            model="doubao-seedance-1-0-pro-fast-251015",
            resolution="480p",
            duration=2,
        )

        print("\n=== Generate Video Result ===")
        print(result)

        # Verify response contains expected fields
        assert "task_id" in result


class TestInfoTools:
    """Integration tests for informational tools."""

    @pytest.mark.asyncio
    async def test_list_models(self) -> None:
        """Test seedance_list_models tool."""
        from tools.info_tools import seedance_list_models

        result = await seedance_list_models()

        print("\n=== List Models Result ===")
        print(result)

        assert "doubao-seedance-1-5-pro-251215" in result
        assert "doubao-seedance-1-0-pro-250528" in result
        assert "doubao-seedance-1-0-pro-fast-251015" in result

    @pytest.mark.asyncio
    async def test_list_resolutions(self) -> None:
        """Test seedance_list_resolutions tool."""
        from tools.info_tools import seedance_list_resolutions

        result = await seedance_list_resolutions()

        print("\n=== List Resolutions Result ===")
        print(result)

        assert "480p" in result
        assert "720p" in result
        assert "1080p" in result
        assert "16:9" in result
        assert "9:16" in result

    @pytest.mark.asyncio
    async def test_list_actions(self) -> None:
        """Test seedance_list_actions tool."""
        from tools.info_tools import seedance_list_actions

        result = await seedance_list_actions()

        print("\n=== List Actions Result ===")
        print(result)

        assert "seedance_generate_video" in result
        assert "seedance_generate_video_from_image" in result
        assert "seedance_get_task" in result


class TestTaskTools:
    """Integration tests for task query tools."""

    @requires_api_token
    @pytest.mark.asyncio
    async def test_get_task_with_real_id(self) -> None:
        """Test querying a task - first generate, then query."""
        from tools.task_tools import seedance_get_task
        from tools.video_tools import seedance_generate_video

        # Generate a video first
        gen_result = await seedance_generate_video(
            prompt="A simple test video",
            model="doubao-seedance-1-0-pro-fast-251015",
            resolution="480p",
            duration=2,
        )

        print("\n=== Generate Result ===")
        print(gen_result)

        # Extract task_id from result
        import json

        gen_data = json.loads(gen_result)
        task_id = gen_data.get("task_id")
        if task_id:
            # Query the task
            task_result = await seedance_get_task(task_id=task_id)
            print("\n=== Task Result ===")
            print(task_result)
            assert task_id in task_result
