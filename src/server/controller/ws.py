from typing import Dict, Any, Set
from fastapi import WebSocket
from src.server.logs.index import Logger

logger = Logger('WSManager')

TMessagePayload = Any
TActiveConnections = Dict[str, Set[WebSocket]]
UserSessions = Dict[str, Set[WebSocket]]

class WSManager:
    def __init__(self):
        self.active_connections: TActiveConnections = {}
        self.user_sessions: UserSessions = {}

    async def connect(self, poll_id: str, ws: WebSocket, email: str):
        if poll_id not in self.active_connections:
            self.active_connections[poll_id] = set()
            logger.info(f'New poll connection: {poll_id}')
        self.active_connections[poll_id].add(ws)
        
        if email not in self.user_sessions:
            self.user_sessions[email] = set()
            logger.info(f'New user session: {email}')
        self.user_sessions[email].add(ws)

        logger.info(f'WebSocket connected: {poll_id}, Total connections: {len(self.active_connections[poll_id])}')

    async def disconnect(self, poll_id: str, ws: WebSocket, email: str):
        self.active_connections[poll_id].discard(ws)  # Remove se existir, não gera erro se não existir
        self.user_sessions[email].discard(ws)

        logger.info(f'WebSocket disconnected: {poll_id}, Remaining connections: {len(self.active_connections[poll_id])}')

    async def send_message_to_poll(self, poll_id: str, message: TMessagePayload):
        if poll_id not in self.active_connections:
            logger.error(f'No active connections for poll_id: {poll_id}')
            return

        for ws in self.active_connections[poll_id]:
            await ws.send_json(message)

    async def send_message_to_user(self, email: str, message: TMessagePayload):
        if email not in self.user_sessions:
            logger.error(f'No active sessions for user email: {email}')
            return

        for ws in self.user_sessions[email]:
            await ws.send_json(message)

ws_manager = WSManager()
