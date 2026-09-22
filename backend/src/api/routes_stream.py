"""WebSocket route: /workflow/stream — streams agent messages to the UI."""
from __future__ import annotations

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from workflows.build_application import workflow_manager
from utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(tags=["stream"])


@router.websocket("/workflow/stream")
async def workflow_stream(websocket: WebSocket) -> None:
    await websocket.accept()
    logger.info("WebSocket client connected")
    # Replay existing history so a late client sees the full conversation.
    for msg in list(workflow_manager.messages):
        await websocket.send_json(msg)
    try:
        while True:
            msg = await workflow_manager.next_message()
            if msg is None:
                await websocket.send_json(
                    {
                        "source": "system",
                        "content": "__STREAM_END__",
                        "state": workflow_manager.state.value,
                    }
                )
                continue
            await websocket.send_json(msg)
    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
