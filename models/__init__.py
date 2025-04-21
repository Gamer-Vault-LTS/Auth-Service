from utils.db import Base, engine
from sqlalchemy import Column, Integer, String, Float, Date, Boolean, Enum, ForeignKey, TIMESTAMP, JSON, func, Numeric, DateTime

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid
Base = declarative_base()
Base.metadata.create_all(bind=engine)