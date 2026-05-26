from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class Task(BaseModel):
    code: str
    name: str = Field(..., alias="name")
    start_date: Optional[str] = None
    finish_date: Optional[str] = None
    status: Optional[str] = None
    progress: Optional[int] = None
    note: Optional[str] = None
    is_active: Optional[bool] = None
    scheduled_days: Optional[int] = None
    actual_start: Optional[str] = None
    actual_finish: Optional[str] = None
    actual_days: Optional[int] = None
    sub_tasks: List[Task] = []

    class Config:
        from_attributes = True
        populate_by_name = True

class Phase(BaseModel):
    name: str
    code: str
    status: Optional[str] = None
    tasks: List[Task] = []

    class Config:
        orm_mode = True

class Roadmap(BaseModel):
    project_name: str
    phases: List[Phase] = []

    class Config:
        orm_mode = True

class TaskUpdate(BaseModel):
    task_code: str
    start_date: Optional[str] = None
    finish_date: Optional[str] = None
    scheduled_days: Optional[int] = None
    actual_start: Optional[str] = None
    actual_finish: Optional[str] = None
    actual_days: Optional[int] = None
    status: Optional[str] = None
    note: Optional[str] = None
    is_active: Optional[bool] = None
