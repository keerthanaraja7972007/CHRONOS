from __future__ import annotations
import asyncio
from collections.abc import AsyncIterator
from backend.models.schemas import WorkflowProgress
class EventBus:
    def __init__(self):self._subscribers:set[asyncio.Queue[WorkflowProgress]] = set()
    async def publish(self,event:WorkflowProgress)->None:
        for subscriber in tuple(self._subscribers):await subscriber.put(event)
    async def subscribe(self)->AsyncIterator[WorkflowProgress]:
        queue:asyncio.Queue[WorkflowProgress]=asyncio.Queue();self._subscribers.add(queue)
        try:
            while True:yield await queue.get()
        finally:self._subscribers.discard(queue)
