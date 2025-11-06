from fastapi import WebSocket, APIRouter, Cookie, WebSocketDisconnect, Depends, Body, HTTPException
from datetime import datetime

from app.api.auth.register import check_token
from app.api.endpoints.dependencies import task_service
from app.utils.websocket import WebsocketUtil
from app.api.models.tasks import Task, TaskUpdate

task = APIRouter(prefix='/tasks')

task_socket_util = WebsocketUtil()


@task.websocket("/general_chat")
async def websocket_endpoint(websocket: WebSocket, payload: dict = Depends(check_token)):
    await task_socket_util.on_connect(websocket, payload)
    try:
        while True:
            message = await websocket.receive_text() #если текста нет, то дальнейший код блокируется, если клиент отключился -> WebSocketDisconnect
            await task_socket_util.on_message(message, websocket)
    except WebSocketDisconnect:
        await task_socket_util.on_disconnect(websocket)

@task.post("/create_task")
async def create_task(task: Task, service: task_service, payload: dict = Depends(check_token)):
    added_task = await service.add_task(task=task, username=payload.get('username'), util=task_socket_util)
    return added_task


@task.delete('/delete_task')
async def delete_task(id: int, service: task_service, payload: dict = Depends(check_token)):
    deleted_data = await service.delete_task(id=id, role=payload.get('role'), username=payload.get('username'), util=task_socket_util)
    return deleted_data

@task.put('/update_task')
async def update_task(id: int, service: task_service, new_task_data: TaskUpdate | None = Body(None), payload: dict = Depends(check_token)):
    if new_task_data is not None:
        updated_data = await service.update_task(id=id, username=payload.get('username'), util=task_socket_util, **new_task_data.__dict__)
        return updated_data
    else:
        raise HTTPException(status_code=400, detail='You must provide at least one parameter')

@task.put('/finish_task')
async def finish_task(id: int, service: task_service, payload: dict = Depends(check_token)):
    username = payload.get('username')
    finish_values = {'finished_by': username, 'date_of_finish': datetime.now()}
    updated_data = await service.update_task(id=id, username=username, util=task_socket_util, action='finished', **finish_values)
    return updated_data








