from backend.debate.event_bus import EventBus
from backend.websocket.manager import manager
class StreamManager:
    def __init__(self,bus:EventBus):self.bus=bus
    async def emit(self,event):
        await self.bus.publish(event); await manager.broadcast(event.model_dump(mode="json"))
