from app.presentation.http.request.register_task_request import \
    RegisterTaskRequest
from app.usecase.service.register_task_service import register_task_service
from fastapi import Header


async def register_task(request: RegisterTaskRequest, userId: str = Header(None)):
    task = register_task_service(
        user_id=userId,
        parent_id=request.parentId,
        name=request.name,
        estimated_workload=request.estimatedWorkload,
        deadline=request.deadline,
        notes=request.notes,
    )
