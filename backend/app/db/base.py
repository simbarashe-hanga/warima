from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import every model
import app.models

