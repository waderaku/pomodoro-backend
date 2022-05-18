from app.presentation.http.request.update_task_request import UpdateTaskRequest
from app.usecase.service.update_task_service import update_task_service
from fastapi import Header


async def update_task(id: str, request: UpdateTaskRequest, userId: str = Header(None)):
    update_task_service(
        userId,
        id,
        request.name,
        request.estimatedWorkload,
        request.deadline,
        request.notes,
        request.done,
    )
