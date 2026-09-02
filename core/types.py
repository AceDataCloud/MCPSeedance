"""Type definitions for Seedance MCP server."""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

# Seedance video models
SeedanceModel = Literal[
    "doubao-seedance-2-5-260628",
    "doubao-seedance-2-0-260128",
    "doubao-seedance-2-0-fast-260128",
    "doubao-seedance-2-0-mini-260615",
    "doubao-seedance-1-5-pro-251215",
    "doubao-seedance-1-0-pro-250528",
    "doubao-seedance-1-0-pro-fast-251015",
    "doubao-seedance-1-0-lite-t2v-250428",
    "doubao-seedance-1-0-lite-i2v-250428",
]

# Video aspect ratios
AspectRatio = Literal[
    "16:9",
    "9:16",
    "1:1",
    "4:3",
    "3:4",
    "21:9",
    "adaptive",
]

# Video resolutions
Resolution = Literal[
    "480p",
    "720p",
    "1080p",
    "4k",
]

# Content item types
ContentType = Literal[
    "text",
    "image_url",
    "audio_url",
    "video_url",
]

# Image roles for content items
ImageRole = Literal[
    "first_frame",
    "last_frame",
    "reference_image",
]

OmniReferenceTaskType = Literal["auto", "reference", "edit", "extend"]
OutputFormat = Literal["mp4", "mov"]
WebSearchSource = Literal["toutiao", "douyin", "moji", "search_engine"]


class SeedanceWebSearchTool(BaseModel):
    """Seedance web search tool configuration."""

    model_config = ConfigDict(extra="forbid")

    type: Literal["web_search"]
    limit: Annotated[int, Field(ge=1, le=50)] = 10
    max_keyword: Annotated[int | None, Field(ge=1, le=50)] = None
    sources: list[WebSearchSource] | None = None


# Default values
DEFAULT_MODEL: SeedanceModel = "doubao-seedance-2-0-260128"
DEFAULT_RESOLUTION: Resolution = "720p"
DEFAULT_RATIO: AspectRatio = "16:9"
DEFAULT_DURATION: int = 5
