import asyncio
async def retry(operation,attempts:int=2):
    last=None
    for attempt in range(attempts+1):
        try:return await operation()
        except Exception as exc:
            last=exc
            if attempt<attempts:await asyncio.sleep(.2*(2**attempt))
    raise last
