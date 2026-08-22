"""Video generation tools for Seedance API."""

from typing import Annotated, Any

from pydantic import Field

from core.client import client
from core.server import mcp
from core.types import (
    DEFAULT_DURATION,
    DEFAULT_MODEL,
    DEFAULT_RATIO,
    DEFAULT_RESOLUTION,
    AspectRatio,
    OmniReferenceTaskType,
    OutputFormat,
    Resolution,
    SeedanceModel,
    SeedanceWebSearchTool,
)
from core.utils import format_video_result


@mcp.tool()
async def seedance_generate_video(
    prompt: Annotated[
        str,
        Field(
            description=(
                "Description of the video to generate. Max 1000 characters. "
                "Be descriptive about the scene, motion, style, and mood. "
                "You can also include inline parameters like "
                "'--rs 720p --rt 16:9 --dur 5'. "
                "Examples: 'A cat walking through a garden with butterflies', "
                "'Cinematic aerial shot of mountains at sunset'"
            )
        ),
    ],
    model: Annotated[
        SeedanceModel,
        Field(
            description=(
                "Model version to use. Options: "
                "'doubao-seedance-2-5-260628' (latest flagship, up to 30 seconds, "
                "multimodal reference, edit/extend, default), "
                "'doubao-seedance-2-0-260128' (highest resolution, supports 4k), "
                "'doubao-seedance-2-0-fast-260128' (latest generation, faster, up to 720p), "
                "'doubao-seedance-2-0-mini-260615' (latest generation, lightweight, "
                "cheapest within the 2.0 series, up to 720p), "
                "'doubao-seedance-1-5-pro-251215' (1.5 flagship, supports audio), "
                "'doubao-seedance-1-0-pro-250528' (1.0 standard), "
                "'doubao-seedance-1-0-pro-fast-251015' (1.0 fast, cost-optimized), "
                "'doubao-seedance-1-0-lite-t2v-250428' (lightweight text-to-video), "
                "'doubao-seedance-1-0-lite-i2v-250428' (lightweight image-to-video)."
            )
        ),
    ] = DEFAULT_MODEL,
    resolution: Annotated[
        Resolution,
        Field(
            description=(
                "Video resolution. Options: '480p', '720p' (default), '1080p', '4k'. "
                "'4k' is supported only by 'doubao-seedance-2-0-260128'; "
                "'2-5' maxes out at '1080p'; '2-0-fast' and '2-0-mini' max out at '720p'."
            )
        ),
    ] = DEFAULT_RESOLUTION,
    ratio: Annotated[
        AspectRatio,
        Field(
            description=(
                "Video aspect ratio. Options: '16:9' (landscape, default), "
                "'9:16' (portrait), '1:1' (square), '4:3', '3:4', "
                "'21:9' (ultrawide), 'adaptive'."
            )
        ),
    ] = DEFAULT_RATIO,
    duration: Annotated[
        int | None,
        Field(
            description=(
                "Video duration in seconds. 1.0 series: 2–12; 1.5 Pro: 4–12; "
                "2.0 series: 4–15; 2.5: 4–30. Use -1 for auto-duration (1.5 Pro and 2.x). "
                "Default is 5. Mutually exclusive with 'frames'."
            ),
            ge=-1,
            le=30,
        ),
    ] = None,
    frames: Annotated[
        int | None,
        Field(
            description=(
                "Frame count for the generated video (1.0 series only). "
                "Must satisfy 25+4n (e.g. 29, 33, 37, ..., 289). "
                "Mutually exclusive with 'duration'."
            ),
            ge=29,
            le=289,
        ),
    ] = None,
    generate_audio: Annotated[
        bool,
        Field(
            description=(
                "If true, generate audio along with the video. "
                "Supported by 'doubao-seedance-1-5-pro-251215' and the "
                "'doubao-seedance-2-0' series; other models ignore it. "
                "Approximately doubles the cost. Default is false."
            )
        ),
    ] = False,
    seed: Annotated[
        int,
        Field(
            description=(
                "Random seed for reproducible generation. "
                "Range: -1 to 4294967295. Use -1 for random. Default is -1."
            ),
            ge=-1,
            le=4294967295,
        ),
    ] = -1,
    camera_fixed: Annotated[
        bool,
        Field(description=("If true, keep the camera fixed during generation. Default is false.")),
    ] = False,
    watermark: Annotated[
        bool,
        Field(description="If true, add a watermark to the video. Default is false."),
    ] = False,
    return_last_frame: Annotated[
        bool,
        Field(
            description=(
                "If true, also return the last frame of the generated video "
                "as an image URL. Useful for video extension workflows. "
                "Default is false."
            )
        ),
    ] = False,
    output_format: Annotated[
        OutputFormat | None,
        Field(description="Seedance 2.5 output format: mp4 or mov."),
    ] = None,
    tools: Annotated[
        list[SeedanceWebSearchTool] | None,
        Field(
            description="Optional Seedance 2.5 web search tool configuration.",
            max_length=1,
        ),
    ] = None,
    priority: Annotated[
        int,
        Field(description="Seedance 2.5 task priority from 0 to 9.", ge=0, le=9),
    ] = 0,
    safety_identifier: Annotated[
        str | None,
        Field(
            description="Stable anonymous end-user identifier. Do not use personal information.",
            max_length=64,
        ),
    ] = None,
    callback_url: Annotated[
        str | None,
        Field(
            description=(
                "Webhook callback URL for asynchronous notifications. "
                "When provided, the API returns immediately with a task_id "
                "and calls this URL when the video is generated."
            )
        ),
    ] = None,
    execution_expires_after: Annotated[
        int,
        Field(
            description=("Task timeout threshold in seconds. Default is 172800 (48 hours)."),
        ),
    ] = 172800,
) -> str:
    """Generate AI video from a text prompt using ByteDance Seedance.

    This is the simplest way to create video - just describe what you want and
    Seedance will generate a high-quality AI video.

    Use this when:
    - You want to create a video from a text description
    - You don't have reference images
    - You want quick text-to-video generation

    For using reference images (first/last frame, reference), use
    seedance_generate_video_from_image instead.

    Returns:
        Task ID and generated video information including URLs and metadata.
    """
    if frames is not None and duration is not None:
        return "Error: 'frames' and 'duration' are mutually exclusive. Provide only one."

    payload: dict[str, Any] = {
        "model": model,
        "content": [{"type": "text", "text": prompt}],
        "resolution": resolution,
        "ratio": ratio,
        "camerafixed": camera_fixed,
        "watermark": watermark,
        "return_last_frame": return_last_frame,
        "execution_expires_after": execution_expires_after,
        "priority": priority,
    }

    if frames is not None:
        payload["frames"] = frames
    else:
        payload["duration"] = duration if duration is not None else DEFAULT_DURATION

    if seed != -1:
        payload["seed"] = seed

    if generate_audio:
        payload["generate_audio"] = True

    if output_format:
        payload["output_format"] = output_format

    if tools:
        payload["tools"] = [
            tool.model_dump(exclude_none=True) if isinstance(tool, SeedanceWebSearchTool) else tool
            for tool in tools
        ]

    if safety_identifier:
        payload["safety_identifier"] = safety_identifier
    if callback_url:
        payload["callback_url"] = callback_url

    result = await client.generate_video(**payload)
    return format_video_result(result)


@mcp.tool()
async def seedance_generate_video_from_image(
    prompt: Annotated[
        str,
        Field(
            description=(
                "Description of the video motion and content. "
                "Describe what should happen in the video, "
                "how objects should move, what transitions to include."
            )
        ),
    ],
    first_frame_url: Annotated[
        str,
        Field(
            description=(
                "URL of the image to use as the first frame of the video. "
                "The video will animate from this image. "
                "Supports https:// URLs or base64 data:image/... URIs."
            )
        ),
    ] = "",
    last_frame_url: Annotated[
        str,
        Field(
            description=(
                "URL of the image to use as the last frame of the video. "
                "The video will animate towards this image. "
                "Supports https:// URLs or base64 data:image/... URIs."
            )
        ),
    ] = "",
    reference_image_urls: Annotated[
        list[str],
        Field(
            description=(
                "List of reference image URLs for style/content guidance. "
                "For the Seedance 2.0 series these can be real-person / character "
                "references that keep the subject consistent (up to 9). "
                "These images influence the look but are not used as frames. "
                "Cannot be combined with first_frame_url or last_frame_url."
            )
        ),
    ] = [],  # noqa: B006
    reference_audio_urls: Annotated[
        list[str],
        Field(
            description=(
                "Seedance 2.0 only. Reference audio URLs (up to 3) for voice timbre / "
                "background music. Ignored by 1.x models."
            )
        ),
    ] = [],  # noqa: B006
    reference_video_urls: Annotated[
        list[str],
        Field(
            description=(
                "Seedance 2.0 only. Reference video URLs (up to 3) for subject, camera "
                "movement, motion or overall style. Ignored by 1.x models."
            )
        ),
    ] = [],  # noqa: B006
    model: Annotated[
        SeedanceModel,
        Field(
            description=(
                "Model version to use. "
                "Use 'doubao-seedance-2-0-260128' (default) for latest-generation quality "
                "and multimodal reference, 'doubao-seedance-2-0-fast-260128' or "
                "'doubao-seedance-2-0-mini-260615' for faster/cheaper 2.0, or a 1.x model "
                "such as 'doubao-seedance-1-0-lite-i2v-250428' for lightweight I2V."
            )
        ),
    ] = DEFAULT_MODEL,
    resolution: Annotated[
        Resolution,
        Field(
            description=(
                "Video resolution. Options: '480p', '720p', '1080p', '4k'. "
                "'4k' is supported only by 'doubao-seedance-2-0-260128'; "
                "'2-5' maxes out at '1080p'; '2-0-fast' and '2-0-mini' max out at '720p'."
            )
        ),
    ] = DEFAULT_RESOLUTION,
    ratio: Annotated[
        AspectRatio,
        Field(description=("Video aspect ratio. Use 'adaptive' to match your input image ratio.")),
    ] = DEFAULT_RATIO,
    duration: Annotated[
        int | None,
        Field(
            description=(
                "Video duration in seconds. 1.0 series: 2–12; 1.5 Pro: 4–12; "
                "2.0 series: 4–15; 2.5: 4–30. Use -1 for auto-duration (1.5 Pro and 2.x). "
                "Default is 5. Mutually exclusive with 'frames'."
            ),
            ge=-1,
            le=30,
        ),
    ] = None,
    frames: Annotated[
        int | None,
        Field(
            description=(
                "Frame count for the generated video (1.0 series only). "
                "Must satisfy 25+4n (e.g. 29, 33, 37, ..., 289). "
                "Mutually exclusive with 'duration'."
            ),
            ge=29,
            le=289,
        ),
    ] = None,
    generate_audio: Annotated[
        bool,
        Field(
            description=(
                "If true, generate audio. Supported by 'doubao-seedance-1-5-pro-251215' "
                "and the Seedance 2.x series. Default is false."
            )
        ),
    ] = False,
    seed: Annotated[
        int,
        Field(
            description="Random seed. -1 for random. Default is -1.",
            ge=-1,
            le=4294967295,
        ),
    ] = -1,
    return_last_frame: Annotated[
        bool,
        Field(
            description=("If true, return the last frame of the generated video. Default is false.")
        ),
    ] = False,
    omni_reference_task_type: Annotated[
        OmniReferenceTaskType | None,
        Field(description="Seedance 2.5 task type: auto, edit, or extend."),
    ] = None,
    output_format: Annotated[
        OutputFormat | None,
        Field(description="Seedance 2.5 output format: mp4 or mov."),
    ] = None,
    tools: Annotated[
        list[SeedanceWebSearchTool] | None,
        Field(
            description="Optional Seedance 2.5 web search tool configuration.",
            max_length=1,
        ),
    ] = None,
    priority: Annotated[
        int,
        Field(description="Seedance 2.5 task priority from 0 to 9.", ge=0, le=9),
    ] = 0,
    safety_identifier: Annotated[
        str | None,
        Field(
            description="Stable anonymous end-user identifier. Do not use personal information.",
            max_length=64,
        ),
    ] = None,
    callback_url: Annotated[
        str | None,
        Field(description="Webhook callback URL for asynchronous notifications."),
    ] = None,
    execution_expires_after: Annotated[
        int,
        Field(
            description=("Task timeout threshold in seconds. Default is 172800 (48 hours)."),
        ),
    ] = 172800,
) -> str:
    """Generate AI video using reference images with ByteDance Seedance.

    This allows you to control the video by specifying first frame, last frame,
    or reference images. Seedance will generate smooth motion based on the inputs.

    Use this when:
    - You have a specific image you want to animate
    - You want to create a video transition between two images
    - You need style guidance from reference images
    - You need precise control over the video's visual content

    Note: reference_image_urls cannot be combined with first_frame_url/last_frame_url.
    At least one image input must be provided.

    Returns:
        Task ID and generated video information including URLs and metadata.
    """
    if (
        not first_frame_url
        and not last_frame_url
        and not reference_image_urls
        and not reference_audio_urls
        and not reference_video_urls
    ):
        return (
            "Error: At least one of first_frame_url, last_frame_url, "
            "reference_image_urls, reference_audio_urls, or reference_video_urls "
            "must be provided."
        )

    if reference_image_urls and (first_frame_url or last_frame_url):
        return (
            "Error: reference_image_urls cannot be combined with first_frame_url or last_frame_url."
        )

    if frames is not None and duration is not None:
        return "Error: 'frames' and 'duration' are mutually exclusive. Provide only one."

    # Build content array
    content: list[dict[str, Any]] = [{"type": "text", "text": prompt}]

    if first_frame_url:
        content.append(
            {
                "type": "image_url",
                "image_url": {"url": first_frame_url},
                "role": "first_frame",
            }
        )

    if last_frame_url:
        content.append(
            {
                "type": "image_url",
                "image_url": {"url": last_frame_url},
                "role": "last_frame",
            }
        )

    for ref_url in reference_image_urls:
        content.append(
            {
                "type": "image_url",
                "image_url": {"url": ref_url},
                "role": "reference_image",
            }
        )

    for audio_url in reference_audio_urls:
        content.append(
            {"type": "audio_url", "audio_url": {"url": audio_url}, "role": "reference_audio"}
        )

    for video_url in reference_video_urls:
        content.append(
            {"type": "video_url", "video_url": {"url": video_url}, "role": "reference_video"}
        )

    payload: dict[str, Any] = {
        "model": model,
        "content": content,
        "resolution": resolution,
        "ratio": ratio,
        "return_last_frame": return_last_frame,
        "execution_expires_after": execution_expires_after,
        "priority": priority,
    }

    if frames is not None:
        payload["frames"] = frames
    else:
        payload["duration"] = duration if duration is not None else DEFAULT_DURATION

    if seed != -1:
        payload["seed"] = seed

    if generate_audio:
        payload["generate_audio"] = True

    if omni_reference_task_type:
        payload["omni_reference_task_type"] = omni_reference_task_type

    if output_format:
        payload["output_format"] = output_format

    if tools:
        payload["tools"] = [
            tool.model_dump(exclude_none=True) if isinstance(tool, SeedanceWebSearchTool) else tool
            for tool in tools
        ]

    if safety_identifier:
        payload["safety_identifier"] = safety_identifier
    if callback_url:
        payload["callback_url"] = callback_url

    result = await client.generate_video(**payload)
    return format_video_result(result)
