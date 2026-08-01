import asyncio
async def parallel(operations):return await asyncio.gather(*operations,return_exceptions=True)
