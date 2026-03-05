"""WebSocket manager for real-time communication."""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional, Set

from fastapi import WebSocket, WebSocketDisconnect


class ConnectionManager:
    """Manager for WebSocket connections."""

    def __init__(self):
        """Initialize connection manager."""
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, task_id: Optional[str] = None):
        """Accept a new WebSocket connection.

        Args:
            websocket: The WebSocket connection
            task_id: Optional task ID to subscribe to
        """
        await websocket.accept()

        async with self._lock:
            if task_id:
                if task_id not in self.active_connections:
                    self.active_connections[task_id] = set()
                self.active_connections[task_id].add(websocket)

    async def disconnect(self, websocket: WebSocket, task_id: Optional[str] = None):
        """Remove a WebSocket connection.

        Args:
            websocket: The WebSocket connection
            task_id: Optional task ID the connection was subscribed to
        """
        async with self._lock:
            if task_id and task_id in self.active_connections:
                self.active_connections[task_id].discard(websocket)
                if not self.active_connections[task_id]:
                    del self.active_connections[task_id]

    async def subscribe(self, websocket: WebSocket, task_id: str):
        """Subscribe a connection to task updates.

        Args:
            websocket: The WebSocket connection
            task_id: Task ID to subscribe to
        """
        async with self._lock:
            if task_id not in self.active_connections:
                self.active_connections[task_id] = set()
            self.active_connections[task_id].add(websocket)

    async def unsubscribe(self, websocket: WebSocket, task_id: str):
        """Unsubscribe a connection from task updates.

        Args:
            websocket: The WebSocket connection
            task_id: Task ID to unsubscribe from
        """
        async with self._lock:
            if task_id in self.active_connections:
                self.active_connections[task_id].discard(websocket)
                if not self.active_connections[task_id]:
                    del self.active_connections[task_id]

    async def send_progress(self, task_id: str, progress: float, **kwargs):
        """Send progress update to all connections subscribed to a task.

        Args:
            task_id: Task ID
            progress: Progress percentage (0-100)
            **kwargs: Additional data to include
        """
        message = {
            "type": "progress",
            "task_id": task_id,
            "timestamp": datetime.utcnow().isoformat(),
            "data": {
                "progress": progress,
                **kwargs
            }
        }

        await self._broadcast(task_id, message)

    async def send_log(self, task_id: str, level: str, log_message: str):
        """Send log message to all connections subscribed to a task.

        Args:
            task_id: Task ID
            level: Log level (debug, info, warning, error)
            log_message: Log message content
        """
        message = {
            "type": "log",
            "task_id": task_id,
            "timestamp": datetime.utcnow().isoformat(),
            "data": {
                "level": level,
                "message": log_message
            }
        }

        await self._broadcast(task_id, message)

    async def send_completed(self, task_id: str, status: str, results: Optional[dict] = None):
        """Send completion notification to all connections subscribed to a task.

        Args:
            task_id: Task ID
            status: Final status (completed, failed, cancelled)
            results: Optional results data
        """
        message = {
            "type": "completed",
            "task_id": task_id,
            "timestamp": datetime.utcnow().isoformat(),
            "data": {
                "status": status,
                "results": results or {}
            }
        }

        await self._broadcast(task_id, message)

    async def _broadcast(self, task_id: str, message: dict):
        """Broadcast a message to all connections subscribed to a task.

        Args:
            task_id: Task ID
            message: Message to broadcast
        """
        if task_id not in self.active_connections:
            return

        disconnected = set()
        message_json = json.dumps(message)

        for connection in self.active_connections[task_id]:
            try:
                await connection.send_text(message_json)
            except Exception:
                disconnected.add(connection)

        # Clean up disconnected clients
        if disconnected:
            async with self._lock:
                for conn in disconnected:
                    self.active_connections[task_id].discard(conn)


# Singleton instance
ws_manager = ConnectionManager()