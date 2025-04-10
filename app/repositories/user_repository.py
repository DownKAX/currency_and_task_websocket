from app.database.db_models import Users
from app.database.db_models import Tasks
from app.repositories.base_repository import Repository

class UserRepository(Repository):
    model = Users

class TaskRepository(Repository):
    model = Tasks