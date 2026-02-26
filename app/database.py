from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
DATABASE_URL = "sqlite:///./test.db"

# connect_args={"check_same_thread": False} is needed only for SQLite. It's not needed for other databases.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# autocommit=False means that the session will not automatically commit transactions. You will need to call session.commit() explicitly to save changes to the database.
# autoflush=False means that the session will not automatically flush changes to the database. You will need to call session.flush() explicitly to send changes to the database before they are committed.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the base class for all the models in the application. It is created using the declarative_base() function from SQLAlchemy. All the models will inherit from this Base class, which provides them with the necessary functionality to interact with the database.
Base = declarative_base()

# get_db is a dependency function that can be used in FastAPI routes to get a database session. It creates a new session using SessionLocal, yields it to the route, and then closes the session after the route is finished. This ensures that each request gets its own database session and that the sessions are properly closed after use.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
