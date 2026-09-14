from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.realtime.manager import ws_manager
import logging

logger = logging.getLogger('learnwise.ws')
router = APIRouter(tags=['websocket'])

@router.websocket('/ws/teacher/{teacher_id}')
async def websocket_teacher_endpoint(websocket: WebSocket, teacher_id: int):
    await ws_manager.connect(websocket, teacher_id)
    try:
        while True:
            data = await websocket.receive_text()
            if data == 'ping':
                await websocket.send_text('pong')
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, teacher_id)
    except Exception as e:
        logger.warning(f'WebSocket error: {e}')
        ws_manager.disconnect(websocket, teacher_id)
