from sqlmodel import Field, SQLModel
from typing import Optional

# --- Data Models ---
# This model is for data that comes IN to the API
class WorkoutCreate(SQLModel):
    name: str
    sets: int
    reps: int
    weight: int

class Workout(SQLModel, table = True):
    id: Optional[int] = Field(default = None, primary_key = True)
    name: str
    sets: int
    reps: int
    weight: int 