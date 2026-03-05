"""WebSocket endpoint for real-time communication."""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query

from app.core.websocket import ws_manager

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    task_id: str = Query(None),
):
    """WebSocket endpoint for real-time updates.

    Args:
        websocket: The WebSocket connection
        task_id: Optional task ID to subscribe to
    """
    await ws_manager.connect(websocket, task_id)

    try:
        while True:
            # Wait for messages from client
            data = await websocket.receive_text()

            # Handle different message types
            try:
                import json
                message = json.loads(data)
                msg_type = message.get("type")

                if msg_type == "subscribe":
                    # Subscribe to task updates
                    subscribe_task_id = message.get("taskId")
                    if subscribe_task_id:
                        await ws_manager.subscribe(websocket, subscribe_task_id)
                        await websocket.send_text(json.dumps({
                            "type": "subscribed",
                            "taskId": subscribe_task_id
                        }))

                elif msg_type == "unsubscribe":
                    # Unsubscribe from task updates
                    unsubscribe_task_id = message.get("taskId")
                    if unsubscribe_task_id:
                        await ws_manager.unsubscribe(websocket, unsubscribe_task_id)

                elif msg_type == "ping":
                    # Respond to ping
                    await websocket.send_text(json.dumps({"type": "pong"}))

            except json.JSONDecodeError:
                # Invalid JSON, ignore
                pass

    except WebSocketDisconnect:
        await ws_manager.disconnect(websocket, task_id)