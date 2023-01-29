import asyncio
import aiohttp
from aiolimiter import AsyncLimiter



async def main(count):
   async with limiter:
    print(count)
limiter = AsyncLimiter(2, 1)

for i in range(10):
    ults = asyncio.run(main(i))
