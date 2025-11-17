import asyncio, base64
from openai import AsyncOpenAI

client = AsyncOpenAI()

async def vision_ocr(img_bytes):
    # base64 encode
    b64_img = base64.b64encode(img_bytes).decode("utf-8")
    # New format: image_url expects an object with url
    message = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Extract all readable text from this image. Preserve lines."},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64_img}"}}
            ]
        }
    ]

    resp = await client.chat.completions.create(
        model="gpt-4o",
        messages=message
    )
    # new SDK -> response.choices[0].message.content
    return resp.choices[0].message.content

def ocr_sync(img_bytes):
    return asyncio.run(vision_ocr(img_bytes))
