from fastapi import WebSocket, HTTPException
from app.core.security import user_data_from_token

class WebsocketUtil:
    def __init__(self):
        self.websocket_clients: list[SocketClient] = []

    async def on_connect(self, websocket: WebSocket, session_token: [str | None]):
        if session_token:
            username = await user_data_from_token(session_token); username = username['username']
            await websocket.accept()
            self.websocket_clients.append(websocket)
            websocket.state.username = username
            for client in self.websocket_clients:
                await client.send_text(f"{websocket.state.username} has joined the general chat!")
        else:
            raise HTTPException(status_code=403, detail="Access rejected") #возможно стоит использовать close или что-то ещё

    async def on_disconnect(self, websocket: WebSocket):
        self.websocket_clients.remove(websocket)
        for client in self.websocket_clients:
            await client.send_text(f"{websocket.state.username} has left the general chat!")

    async def on_message(self, message: str, websocket: WebSocket):
        for client in self.websocket_clients:
            await client.send_text(f"{websocket.state.username}: {message}")

    async def on_task_event(self, task_title: str, username: str, action: str):
        for client in self.websocket_clients:
            await client.send_text(f'{username} {action} - "{task_title}"!')