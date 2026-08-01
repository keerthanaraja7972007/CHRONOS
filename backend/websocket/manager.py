from fastapi import WebSocket
class ConnectionManager:
    def __init__(self): self.connections: set[WebSocket] = set()
    async def connect(self, socket: WebSocket): await socket.accept(); self.connections.add(socket)
    def disconnect(self, socket: WebSocket): self.connections.discard(socket)
    async def broadcast(self, message: dict):
        for socket in list(self.connections): await socket.send_json(message)
manager = ConnectionManager()
