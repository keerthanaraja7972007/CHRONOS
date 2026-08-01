import asyncio
async def with_timeout(operation,seconds:float):return await asyncio.wait_for(operation(),timeout=seconds)
