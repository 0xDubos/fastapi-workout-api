from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, Session, select

# Creates an instance of the FastAPI class
app = FastAPI()
workout_db = [] # Simple in-memory database

# --- Data Models ---
# This model is for data that comes IN to the API
class WorkoutCreate(SQLModel):
    id: int
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

# --- DATABASE CONNECTION --- *

# The database file will be named "workouts.db"
sqlite_file_name = "workouts.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# The engine is the object that connects to our database
# echo=True will print the raw SQL statements it's running. This helps with debugging
engine = create_engine(sqlite_url, echo = True)

# --- Database Session ---
# This function will be our dependency. It creates and yields a new database session
def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    """Finds all SQLModel classes and creates the corresponding database tables"""
    SQLModel.metadata.create_all(engine)

# --- API ENDPOINTS--- *

# This event handler runs the funciton once the app starts up
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Defines a "path operation decorator" for /workouts
@app.post("/workouts")
def create_workout(workout: WorkoutCreate, session: Session = Depends(get_session)):
    
    db_workout = Workout.model_validate(workout)
    # Add the workout object to the session
    session.add(db_workout)
    # Commit the changes to the database
    session.commit()
    # Refresh the object to get the new ID
    session.refresh(db_workout)
    # Return newly created workout
    return db_workout

@app.get("/workouts")
def get_workouts(session: Session = Depends(get_session)):
    statement = select(Workout)
    results = session.exec(statement)
    workout = results.all()
    return workout

@app.delete("/workouts/{workout_id}")
def delete_workout(workout_id: int, session: Session = Depends(get_session)):
    # Find the specific workout in the database
    workout = session.get(Workout, workout_id)

    # If the workout doesn't exist, raise a 404 error
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    # Delete the wrokout and save the change
    session.delete(workout)
    session.commit()

    return {"ok": True, "message": "Workout deleted successfully!"}

@app.put("/workouts/{workout_id}")
def update_workout(workout_id: int, workout_update: WorkoutCreate, session: Session = Depends(get_session)):
    # Find the existing workout in the database
    db_workout = session.get(Workout, workout_id)
    if not db_workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    
    # Get the data from the incoming request
    workout_data = workout_update.model_dump(exclude_unset=True)
    # Update the fields on the existing workout object
    for key, value in workout_data.items():
        setattr(db_workout, key, value)

    # Add, commit, and refresh the session to save the changes
    session.add(db_workout)  
    session.commit()
    session.refresh(db_workout)

    return db_workout