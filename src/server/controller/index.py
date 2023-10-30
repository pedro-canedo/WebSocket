from fastapi import APIRouter, Query, WebSocket, Depends, HTTPException, Request

from src.server.middleware.auth import get_current_user
from src.server.logs.index import Logger
from .ws import ws_manager

router = APIRouter()
logger = Logger('CONTROLLER')



@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str, token: str = Query(...)):
    current_user = get_current_user(token)
    await websocket.accept()
    await ws_manager.connect(client_id, websocket, current_user)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except:
        ws_manager.disconnect(client_id, websocket, current_user)
        await websocket.close()

@router.post("/send-poll")
async def send_poll(poll_id: str, request: Request):
    """
    Endpoint para emitir uma mensagem para todos os WebSockets associados a um determinado poll_id.
    """
    client_ip = request.client.host
    logger.info(f"Received poll send request from IP: {client_ip}, Poll ID: {poll_id}")

    await ws_manager.send_message_to_poll(poll_id, {"type": "new_task", "message": "New task available"})
    return {"status": "poll sent"}

@router.post("/send-poll-to-user")
async def send_poll_to_user(email: str, poll_id: str, request: Request):
    """
    Endpoint para emitir uma mensagem para todos os WebSockets associados a um determinado e-mail.
    """
    client_ip = request.client.host
    logger.info(f"Received poll send request from IP: {client_ip}, Email: {email}, Poll ID: {poll_id}")

    await ws_manager.send_message_to_user(email, {"type": "new_task", "message": "New task available"})
    return {"status": "poll sent"}


@router.post("/send-message")
async def send_message(email: str, message: str, request: Request):
    """
    Endpoint para emitir uma mensagem para todos os WebSockets associados a um determinado e-mail.
    """
    client_ip = request.client.host
    logger.info(f"Received message send request from IP: {client_ip}, Email: {email}, Message: {message}")

    await ws_manager.send_message_to_user(email, {"type": "new_task", "message": message})
    return {"status": "message sent"}


