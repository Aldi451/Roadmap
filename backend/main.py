from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .models import Roadmap, Phase, Task, UserRole, TaskUpdate
from typing import List

app = FastAPI(title="Roadmap API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = Path(__file__).parent.parent / "frontend"
app.mount("/roadmap", StaticFiles(directory=str(static_dir), html=True), name="frontend")

@app.get("/", include_in_schema=False)
async def root_redirect():
    return RedirectResponse(url="/roadmap")

# Global data storage (in-memory for demo)
ROADMAP_DATA = {
    "project_name": "Project Roadmap : 4682 - Fortunasuite Malioboro - Yogyakarta",
    "phases": [
        Phase(
            name="Project Preparation",
            code="1.PRP",
            status="On Progress",
            tasks=[
                Task(code="1.1", name="Implementation Periode : 60 Days", start_date="2024-05-01", finish_date="2024-07-01", status="On Progress", progress=10, note="Initial phase"),
                Task(code="1.2", name="Setup Data Submission", start_date="2024-05-05", finish_date="2024-05-15", status="Completed", progress=100, note="Done"),
                Task(code="1.3", name="Setup Data Overview", start_date="2024-05-10", finish_date="2024-05-20", status="Completed", progress=100),
                Task(code="1.4", name="Server Information", start_date="2024-05-12", finish_date="2024-05-15", status="Completed", progress=100),
                Task(code="1.5", name="Keylock Information", start_date="2024-05-15", finish_date="2024-05-18", status="Completed", progress=100),
                Task(code="1.6", name="PABX Information", start_date="2024-05-18", finish_date="2024-05-22", status="On Progress", progress=60),
                Task(code="1.7", name="Channel Manager Information", start_date="2024-05-20", finish_date="2024-05-25", status="Scheduled", progress=0),
                Task(code="1.8", name="Power GO", start_date="2024-05-22", finish_date="2024-05-28", status="Scheduled", progress=0),
                Task(code="1.9", name="PB1 Integration", start_date="2024-05-25", finish_date="2024-05-30", status="Scheduled", progress=0),
            ]
        ),
        Phase(
            name="Implementation Cloud Full Version",
            code="2.ICF",
            status="Scheduled",
            tasks=[
                Task(code="2.1", name="Kick Off Meeting", start_date="2024-06-01", finish_date="2024-06-01", status="Scheduled", progress=0),
                Task(code="2.2", name="System Configuration", start_date="2024-06-02", finish_date="2024-06-15", status="Scheduled", progress=0),
                Task(
                    code="2.3", 
                    name="Training", 
                    status="Scheduled", 
                    progress=0,
                    sub_tasks=[
                        Task(code="2.3.1.1", name="Training Schedule", start_date="2024-06-16", finish_date="2024-06-20", status="Scheduled", progress=0),
                        Task(code="2.3.1.2", name="Training Status", start_date="2024-06-21", finish_date="2024-06-25", status="Scheduled", progress=0),
                    ]
                )
            ]
        )
    ]
}

# Mock National Holidays in Indonesia (May/June 2024)
HOLIDAYS = [
    "2024-05-01", # Labor Day
    "2024-05-09", # Ascension Day of Jesus Christ
    "2024-05-23", # Waisak Day
    "2024-06-01", # Pancasila Day
    "2024-06-17", # Eid al-Adha
]

@app.get("/api/roadmap", response_model=Roadmap)
async def get_roadmap():
    return ROADMAP_DATA

@app.get("/api/holidays")
async def get_holidays():
    return HOLIDAYS

@app.post("/api/roadmap/update-task")
async def update_task(update: TaskUpdate):
    # Finding task by code
    found = False
    for phase in ROADMAP_DATA["phases"]:
        for task in phase.tasks:
            if task.code == update.task_code:
                if update.start_date is not None: task.start_date = update.start_date
                if update.finish_date is not None: task.finish_date = update.finish_date
                if update.scheduled_days is not None: task.scheduled_days = update.scheduled_days
                if update.actual_start is not None: task.actual_start = update.actual_start
                if update.actual_finish is not None: task.actual_finish = update.actual_finish
                if update.actual_days is not None: task.actual_days = update.actual_days
                if update.status is not None: task.status = update.status
                if update.note is not None: task.note = update.note
                if update.is_active is not None: task.is_active = update.is_active
                found = True
                break
            for sub in task.sub_tasks:
                if sub.code == update.task_code:
                    if update.start_date is not None: sub.start_date = update.start_date
                    if update.finish_date is not None: sub.finish_date = update.finish_date
                    if update.scheduled_days is not None: sub.scheduled_days = update.scheduled_days
                    if update.actual_start is not None: sub.actual_start = update.actual_start
                    if update.actual_finish is not None: sub.actual_finish = update.actual_finish
                    if update.actual_days is not None: sub.actual_days = update.actual_days
                    if update.status is not None: sub.status = update.status
                    if update.note is not None: sub.note = update.note
                    if update.is_active is not None: sub.is_active = update.is_active
                    found = True
                    break
        if found: break
    
    if not found:
        # For demo purposes, if task not found in static data, we just return success
        # In a real app, you would save this to a database
        print(f"Task {update.task_code} not found in static data, but update accepted.")
        return {"message": "Update received (dynamic task)"}
    
    return {"message": "Updated successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
