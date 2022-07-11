from dataclasses import asdict

from app.domain.model.entity.task_user import TaskUser
from app.domain.repository.task_user_repository import TaskUserRepository
from app.infrastructure.dynamodb.model.task_model import TaskModel
from app.infrastructure.dynamodb.model.user_model import UserModel
from app.infrastructure.dynamodb.repository.dynamo_repository import \
    DynamoRepository


class TaskUserDynamoRepository(TaskUserRepository, DynamoRepository):
    def register_task_user(self, task_user: TaskUser):
        user_model = UserModel.to_model(task_user._user)
        task_model_list = [
            TaskModel.to_model(task=task) for task in task_user._task_list
        ]
        with self._table.batch_writer() as batch:
            batch.put_item(Item=asdict(user_model))
            for task_model in task_model_list:
                batch.put_item(Item=asdict(task_model))
