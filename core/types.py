"""Type definitions for Seedance MCP server."""

from typing import Literal

# Seedance video models
SeedanceModel = Literal[
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
]

# Service tiers
ServiceTier = Literal[
    "default",
    "flex",
]

# Content item types
ContentType = Literal[
    "text",
    "image_url",
]

# Image roles for content items
ImageRole = Literal[
    "first_frame",
    "last_frame",
    "reference_image",
]

# Default values
DEFAULT_MODEL: SeedanceModel = "doubao-seedance-1-0-pro-250528"
DEFAULT_RESOLUTION: Resolution = "720p"
DEFAULT_RATIO: AspectRatio = "16:9"
DEFAULT_DURATION: int = 5
