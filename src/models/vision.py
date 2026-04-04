from openai import OpenAI
import base64
import os

def get_openai_client():
    """Get OpenAI client, only if API key is available."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return OpenAI(api_key=api_key)


def encode_image(image_path):
    """Encode image to base64 for OpenAI API."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def describe_image(image_path, max_retries=1):
    """
    Generate a text description of an image using OpenAI's vision model.

    Args:
        image_path: Path to the image file
        max_retries: Number of retries on failure

    Returns:
        Text description of the image
    """
    if not os.path.exists(image_path):
        return f"[Image file not found: {image_path}]"

    try:
        base64_image = encode_image(image_path)

        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describe this image in detail, focusing on any charts, diagrams, technical drawings, or visual elements that might be relevant to engineering or policy documents."},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{base64_image}"}
                        },
                    ],
                }
            ],
            max_tokens=300,
        )

        description = response.choices[0].message.content
        return f"Image description: {description}"

    except Exception as e:
        error_msg = str(e)
        if "insufficient_quota" in error_msg:
            return f"[Image analysis unavailable: OpenAI quota exceeded. Image: {os.path.basename(image_path)}]"
        elif "rate_limit" in error_msg:
            return f"[Image analysis rate limited. Image: {os.path.basename(image_path)}]"
        else:
            return f"[Image analysis failed: {error_msg}. Image: {os.path.basename(image_path)}]"
