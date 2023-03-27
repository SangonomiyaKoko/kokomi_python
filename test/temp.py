#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
*** This is a file used to temporarily store some methods that are not currently used ***
@Time     : 2023-03-27
@Author   : Maoyu
@Name     : temp.py
@Verson   : 1.0.0
"""
import asyncio
import hashlib
import httpx
from nonebot.log import logger


"""

*** Download QQ user's avatar ***

async def download_url(url: str) -> bytes:
    async with httpx.AsyncClient() as client:
        for i in range(3):
            try:
                resp = await client.get(url, timeout=20)
                resp.raise_for_status()
                return resp.content
            except Exception as e:
                logger.warning(f"Error downloading {url}, retry {i}/3: {e}")
                await asyncio.sleep(3)
    raise Exception(f"{url} Download failure！")


async def download_avatar(user_id: str) -> bytes:
    url = f"http://q1.qlogo.cn/g?b=qq&nk={user_id}&s=640"
    data = await download_url(url)
    if hashlib.md5(data).hexdigest() == "acef72340ac0e914090bd35799f5594e":
        url = f"http://q1.qlogo.cn/g?b=qq&nk={user_id}&s=100"
        data = await download_url(url)
    return data
    
"""
