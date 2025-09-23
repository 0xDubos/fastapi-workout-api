from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
# Imports from other local files
from models import Workout, WorkoutCreate
from database import get_session, engine

router = APIRouter()

# Defines a "path operation decorator" for /workouts
@router.post("/workouts")
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

@router.get("/workouts")
def get_workouts(session: Session = Depends(get_session)):
    statement = select(Workout)
    results = session.exec(statement)
    workout = results.all()
    return workout

@router.delete("/workouts/{workout_id}")
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

@router.put("/workouts/{workout_id}")
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