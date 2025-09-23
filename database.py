from sqlmodel import SQLModel, create_engine, Session

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
