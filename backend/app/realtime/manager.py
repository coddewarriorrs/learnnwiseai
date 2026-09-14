from fastapi import WebSocket
from typing import Dict, List, Any
import json
import logging

logger = logging.getLogger('learnwise.realtime')

class ConnectionManager:
    def __init__(self):
        self.active_teacher_connections: Dict[int, List[WebSocket]] = {}
        self.all_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket, teacher_id: int):
        await websocket.accept()
        if teacher_id not in self.active_teacher_connections:
            self.active_teacher_connections[teacher_id] = []
        self.active_teacher_connections[teacher_id].append(websocket)
        self.all_connections.append(websocket)
        logger.info(f'WebSocket connected for teacher {teacher_id}')

    def disconnect(self, websocket: WebSocket, teacher_id: int):
        if teacher_id in self.active_teacher_connections:
            if websocket in self.active_teacher_connections[teacher_id]:
                self.active_teacher_connections[teacher_id].remove(websocket)
            if not self.active_teacher_connections[teacher_id]:
                del self.active_teacher_connections[teacher_id]
        if websocket in self.all_connections:
            self.all_connections.remove(websocket)

    async def broadcast_to_teacher(self, teacher_id: int, message: Dict[str, Any]):
        if teacher_id in self.active_teacher_connections:
            dead = []
            for connection in self.active_teacher_connections[teacher_id]:
                try:
                    await connection.send_text(json.dumps(message))
                except Exception as e:
                    dead.append(connection)
            for d in dead:
                self.disconnect(d, teacher_id)

    async def broadcast_event(self, event_type: str, data: Dict[str, Any], target_teacher_ids: List[int] = None):
        payload = {'event': event_type, 'data': data}
        if target_teacher_ids:
            for tid in target_teacher_ids:
                await self.broadcast_to_teacher(tid, payload)
        else:
            dead = []
            for ws in self.all_connections:
                try:
                    await ws.send_text(json.dumps(payload))
                except Exception:
                    dead.append(ws)
            for d in dead:
                if d in self.all_connections:
                    self.all_connections.remove(d)

ws_manager = ConnectionManager()
