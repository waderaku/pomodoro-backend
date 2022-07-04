from app.presentation.http.response.task_response import Task, TaskData, TaskResponse
from app.usecase.service.fetch_task_service import fetch_task_service
from fastapi import Header

table_name = "pomodoro_info"


async def fetch_task(userId: str = Header(None)) -> list[TaskResponse]:
    task_list, root_task_list = fetch_task_service(user_id=userId)
    response_task_list = [_create_task(task) for task in task_list]
    response_root_id = [root_task["DataType"][:-5] for root_task in root_task_list]
    return TaskResponse(task=response_task_list, rootTaskId=response_root_id)


def _create_task(task: dict):
    task_data_dict = task["TaskInfo"]
    task_data = TaskData(
        name=task_data_dict["name"],
        childrenIdList=task_data_dict["children_task_id"],
        done=task["DataValue"],
        finishedWorkload=task_data_dict["finished_workload"],
        estimatedWorkload=task_data_dict["estimated_workload"],
        deadline=task_data_dict["deadline"],
        notes=task_data_dict["notes"],
    )
    return Task(id=task["DataType"], taskData=task_data)
