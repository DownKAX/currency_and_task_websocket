from pydantic import BaseModel
from datetime import datetime

class Task(BaseModel):
    title: str
    description: str

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
