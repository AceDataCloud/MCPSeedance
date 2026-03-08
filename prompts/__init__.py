"""Prompt templates for Seedance MCP server.

MCP Prompts provide guidance to LLMs on when and how to use the available tools.
These are exposed via the MCP protocol and help LLMs make better decisions.
"""

from core.server import mcp


@mcp.prompt()
def seedance_video_generation_guide() -> str:
    """Guide for choosing the right Seedance tool for video generation."""
    return """# Seedance Video Generation Guide

When the user wants to generate video, choose the appropriate tool based on their needs:

## Text to Video (Simple)
**Tool:** `seedance_generate_video`
**Use when:**
- User gives a text description: "make me a video of a cat"
- User wants Seedance to handle the visuals from scratch
- Quick, prompt-based video creation

**Example:** "Create a video of astronauts in space"
-> Call `seedance_generate_video` with prompt="Astronauts floating in space, stars in background, cinematic lighting"

## Image to Video (Reference Images)
**Tool:** `seedance_generate_video_from_image`
**Use when:**
- User provides an image URL to animate
- User wants video to start/end with a specific image
- User wants style guidance from reference images
- User needs precise visual control

**Example:** "Animate this image: [image_url]"
-> Call `seedance_generate_video_from_image` with first_frame_url=image_url and appropriate prompt

## Choosing the Right Model
- **Best quality + audio:** `doubao-seedance-1-5-pro-251215`
- **Balanced (default):** `doubao-seedance-1-0-pro-250528`
- **Fastest/cheapest:** `doubao-seedance-1-0-pro-fast-251015`
- **Lightweight T2V:** `doubao-seedance-1-0-lite-t2v-250428`
- **Lightweight I2V:** `doubao-seedance-1-0-lite-i2v-250428`

## Checking Status
**Tool:** `seedance_get_task`
**Use when:**
- Generation takes time and user wants to check if it's ready
- User asks "is my video done?"

## Important Notes:
1. Video generation may take 30s to several minutes depending on settings
2. Default resolution is 720p, default ratio is 16:9
3. Duration range: 2-12 seconds
4. Only 1.5 Pro model supports audio generation
5. Use 'flex' service_tier for 50% cost savings
6. Use seed parameter for reproducible results
7. reference_image_urls CANNOT be combined with first_frame/last_frame
8. Use callback_url for async processing in production
"""


@mcp.prompt()
def seedance_workflow_examples() -> str:
    """Common workflow examples for Seedance video generation."""
    return """# Seedance Workflow Examples

## Workflow 1: Quick Video Generation
1. User: "Make me a video of waves on a beach"
2. Call `seedance_generate_video(prompt="Ocean waves gently crashing on sandy beach, sunset, cinematic")`
3. Return task_id and video URL to user
4. If async, user can check status with `seedance_get_task(task_id)`

## Workflow 2: Animate an Image
1. User provides image URL
2. Call `seedance_generate_video_from_image(prompt="Camera slowly zooming in, gentle movement", first_frame_url=user_url)`
3. Return task_id and video URL

## Workflow 3: Create Transition Between Two Images
1. User provides two image URLs
2. Call `seedance_generate_video_from_image(first_frame_url=first_url, last_frame_url=second_url, prompt="Smooth morphing transition")`
3. Return task_id and video URL

## Workflow 4: Style-Guided Generation
1. User provides reference images for style
2. Call `seedance_generate_video_from_image(prompt="...", reference_image_urls=[ref1, ref2])`
3. Return task_id and video URL

## Workflow 5: High Quality with Audio
1. User wants premium video with sound
2. Call `seedance_generate_video(prompt="...", model="doubao-seedance-1-5-pro-251215", generate_audio=true, resolution="1080p")`
3. Return task_id and video URL

## Workflow 6: Budget-Friendly Generation
1. User wants cheap/fast results
2. Call `seedance_generate_video(prompt="...", model="doubao-seedance-1-0-pro-fast-251015", service_tier="flex", resolution="480p")`
3. Return task_id and video URL

## Workflow 7: Mobile-First Content
1. User wants content for TikTok/Instagram Reels
2. Call `seedance_generate_video(prompt="...", ratio="9:16")`
3. Return task_id and video URL

## Tips:
- Always be descriptive in prompts - include motion, style, mood
- Mention camera movements: "zooming in", "panning left", "tracking shot"
- Specify style: "cinematic", "realistic", "dreamy", "dramatic", "anime"
- For reproducible results, specify a seed value
- Use return_last_frame=true if planning to chain multiple video segments
"""


@mcp.prompt()
def seedance_prompt_suggestions() -> str:
    """Tips for writing effective Seedance video prompts."""
    return """# Seedance Prompt Writing Guide

## Prompt Structure
A good Seedance prompt typically includes:
1. **Subject** - What is in the video
2. **Action** - What is happening (motion is key for video!)
3. **Setting** - Where it takes place
4. **Style** - Visual style and mood
5. **Camera** - Camera movement or angle

## Example Prompts

### Nature
- "A majestic eagle soaring over snow-capped mountains, golden hour lighting, cinematic aerial tracking shot"
- "Cherry blossoms falling in slow motion in a Japanese garden, soft focus, dreamy atmosphere"

### People
- "A dancer performing ballet on a stage, dramatic spotlight, slow motion spin, artistic"
- "A chef preparing sushi in a traditional kitchen, close-up hands, warm lighting"

### Abstract
- "Colorful paint droplets falling into water, macro shot, vibrant colors, slow motion"
- "Geometric patterns transforming and flowing, neon colors on dark background, hypnotic"

### Cinematic
- "Drone shot flying through a misty forest at dawn, rays of light filtering through trees"
- "Futuristic cityscape at night, neon lights reflecting on wet streets, cyberpunk aesthetic"

## Tips
- Be specific about motion and movement
- Include lighting descriptions
- Mention camera movements for dynamic videos
- Use style keywords: cinematic, realistic, anime, watercolor, etc.
- Keep prompts under 1000 characters
- For I2V, describe what should change/move from the reference image
"""
