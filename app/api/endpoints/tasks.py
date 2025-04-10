from fastapi import WebSocket, APIRouter, Cookie, WebSocketDisconnect, Depends, Body, HTTPException
from datetime import datetime

from app.utils.websocket import WebsocketUtil
from app.api.models.tasks import Task, TaskUpdate
from app.service.users_service import TaskService
from app.core.security import user_data_from_token
from app.utils.unitofwork import UnitOfWork, AbstractUnitOfWork

task = APIRouter(prefix='/tasks')

task_socket_util = WebsocketUtil()

async def get_user_service(uow: AbstractUnitOfWork = Depends(UnitOfWork)) -> TaskService:
    return TaskService(uow)

@task.websocket("/general_chat")
async def websocket_endpoint(websocket: WebSocket, session_token=Cookie()):
    await task_socket_util.on_connect(websocket, session_token)
    try:
        while True:
            message = await websocket.receive_text() #если текста нет, то дальнейший код блокируется, если клиент отключился -> WebSocketDisconnect
            await task_socket_util.on_message(message, websocket)
    except WebSocketDisconnect:
        await task_socket_util.on_disconnect(websocket)

@task.post("/create_task")
async def create_task(task: Task, session_token: str = Cookie(), service: TaskService = Depends(get_user_service)):
    user_data = await user_data_from_token(session_token)
    added_task = await service.add_task(task=task, username=user_data.get('username'), util=task_socket_util)
    return added_task


@task.delete('/delete_task')
async def delete_task(id: int, session_token: str = Cookie(), service: TaskService = Depends(get_user_service)):
    user_data = await user_data_from_token(session_token)
    deleted_data = await service.delete_task(id=id, role=user_data.get('role'), username=user_data.get('username'), util=task_socket_util)
    return deleted_data

@task.put('/update_task')
async def update_task(id: int, new_task_data: TaskUpdate | None = Body(None), session_token: str = Cookie(), service: TaskService = Depends(get_user_service)):
    user_data = await user_data_from_token(session_token)
    if new_task_data is not None:
        updated_data = await service.update_task(id=id, username=user_data.get('username'), util=task_socket_util, **new_task_data.__dict__)
        return updated_data
    else:
        raise HTTPException(status_code=400, detail='You must provide at least one parameter')

@task.put('/finish_task')
async def finish_task(id: int, session_token: str = Cookie(), service: TaskService = Depends(get_user_service)):
    user_data = await user_data_from_token(session_token); username = user_data.get('username')
    finish_values = {'finished_by': username, 'date_of_finish': datetime.now()}
    updated_data = await service.update_task(id=id, username=username, util=task_socket_util, action='finished', **finish_values)
    return updated_data








