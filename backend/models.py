from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "Admin"
    MANAGER = "Manager"
    OFFICER = "Officer"
    USER = "User"

class Task(BaseModel):
    code: str
    name: str
    start_date: Optional[str] = None
    finish_date: Optional[str] = None
    actual_start: Optional[str] = None
    actual_finish: Optional[str] = None
    status: str
    progress: int = 0
    sub_tasks: List['Task'] = []
    category: Optional[str] = None
    note: Optional[str] = None
    is_active: bool = True

class TaskUpdate(BaseModel):
    task_code: str
    start_date: Optional[str] = None
    finish_date: Optional[str] = None
    scheduled_days: Optional[str] = None
    actual_start: Optional[str] = None
    actual_finish: Optional[str] = None
    actual_days: Optional[str] = None
    status: Optional[str] = None
    note: Optional[str] = None
    is_active: Optional[bool] = None
    role: UserRole = UserRole.USER

# Re-enable self-referencing model
Task.model_rebuild()

class Phase(BaseModel):
    name: str
    code: str
    status: str
    tasks: List[Task]

class Roadmap(BaseModel):
    project_name: str
    phases: List[Phase]
