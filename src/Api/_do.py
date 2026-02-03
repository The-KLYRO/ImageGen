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

    async def generate(self, prompt: str):
        url = f"{self.api_base}/gen.php?prompt={quote(prompt or '', safe='')}"
        async with aiohttp.ClientSession() as s:
            async with s.get(url) as r:
                return await r.json(content_type=None)

    async def download(self, path: str):
        url = f"{self.api_base}/{path.lstrip('/')}"
        async with aiohttp.ClientSession() as s:
            async with s.get(url) as r:
                data = await r.read()
        return data

async def test(prompt):
    result = await api.generate(prompt)
    print(result)
    if result["success"]:
        data = await api.download(result["path"])
        with open(result["filename"], "wb") as f:
            f.write(data)


if __name__ == "__main__":
    import asyncio
    api= Api()
    asyncio.run(test("test"))


