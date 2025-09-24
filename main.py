from fastapi import FastAPI
from database import create_db_and_tables
from workouts_router import router as workouts_router
from users_router import router as users_router 

# Creates an instance of the FastAPI class
app = FastAPI()

# This event handler runs the funciton once the app starts up
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Includes the router from our workouts_router.py file
app.include_router(workouts_router)

# Includes the router from our users_router.py file
app.include_router(users_router)
