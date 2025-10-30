
from fastapi import APIRouter, WebSocket, WebSocketDisconnect


class WebSocketConnectionManager:
    """
    Manages WebSocket connections and broadcasting
    messages to all connected clients.
    """

    def __init__(self) -> None:
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        # Accept the websocket handshake explicitly when the endpoint runs.
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str) -> None:
        # iterate over a copy to avoid mutation while sending
        for connection in list(self.active_connections):
            try:
                await connection.send_text(message)
            except Exception:
                # remove dead/errored connection
                try:
                    self.active_connections.remove(connection)
                except ValueError:
                    pass


# Shared instance that other modules can import
ws_manager = WebSocketConnectionManager()

# Router for websocket endpoints (keeps websocket code out of main.py)
router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """WebSocket endpoint that registers clients with the shared manager.

    Note: During the WebSocket handshake the browser will send an Origin header.
    FastAPI/Starlette will reject the connection with 403 if that origin is not
    allowed by the app's CORSMiddleware. Ensure your frontend origin
    (for example http://localhost:8080 or http://127.0.0.1:8080) is included
    in the `allow_origins` list in `main.py`.
    """
    await ws_manager.connect(websocket)
    try:
        # Keep the connection open. We don't expect messages from the client;
        # awaiting receive_text() simply allows detecting disconnects.
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
