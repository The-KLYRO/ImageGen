# api.py
from __future__ import annotations

import os
import aiohttp
from urllib.parse import quote
from dataclasses import dataclass
from typing import Any, Dict, Optional

# from src.Config import API

class ApiError(Exception):
    """Raised when the ImgGen API call fails or returns an error."""
    pass


@dataclass
class GenerateResult:
    success: bool
    filename: Optional[str] = None
    path: Optional[str] = None
    message: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None



class Api:
    def __init__(self, api_base="https://imggen.ct.ws"):
        self.api_base = api_base.rstrip("/")

    async def generate(self, prompt: str) -> GenerateResult:
        url = f"{self.api_base}/gen.php?prompt={quote(prompt or '', safe='')}"
        print(url)
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as s:
            async with s.get(url) as r:
                try:
                    # Check response status
                    if r.status != 200:
                        return GenerateResult(
                            success=False,
                            message=f"HTTP {r.status}: {r.reason}",
                            raw={}
                        )
                    
                    # Get response text first
                    text = await r.text()
                    print(f"Response: {text[:200]}...")  # Increased debug output to see more of the challenge
                    
                    # Check for common anti-bot challenge markers
                    if "aes.js" in text or "toNumbers" in text:
                        return GenerateResult(
                            success=False,
                            message="API blocked by anti-bot challenge (Javascript required)",
                            raw={"text": text[:500]}
                        )

                    # Check if response is empty
                    if not text.strip():
                        return GenerateResult(
                            success=False,
                            message="Empty response from API",
                            raw={}
                        )
                    
                    # Try to parse JSON from the text
                    try:
                        import json
                        data = json.loads(text)
                    except json.JSONDecodeError:
                         return GenerateResult(
                            success=False,
                            message="Failed to parse JSON response",
                            raw={"text": text[:500]}
                        )

                    print(f"Parsed data: {data}")
                    return GenerateResult(
                        success=data.get("success", False),
                        filename=data.get("filename"),
                        path=data.get("path"),
                        raw=data
                    )
                except Exception as e:
                    return GenerateResult(
                        success=False,
                        message=f"API call failed: {str(e)}",
                        raw={}
                    )

    async def download(self, path: str) -> bytes:
        url = f"{self.api_base}/{path.lstrip('/')}"
        async with aiohttp.ClientSession() as s:
            async with s.get(url) as r:
                return await r.read()

async def test(prompt):
    # result = await api.generate(prompt)
    # print(result)
    # if result.success:
        data = await api.download("images/698249092deae.jpg")
        with open("test.jpg", "wb") as f:
            f.write(data)


if __name__ == "__main__":
    import asyncio
    api= Api()
    asyncio.run(test("girl with red hair"))


