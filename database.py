from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Event(Base):
    tablename = 'events'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    date = Column(DateTime)
    location = Column(String)  # корпус (центральный, восточный и т.д.)
    category = Column(String)  # направление (спорт, культура и т.д.)
    roles = Column(String)     # роли (участник, волонтёр, организатор)
    registration_link = Column(String)

class User(Base):
    tablename = 'users'
    chat_id = Column(Integer, primary_key=True)
    is_admin = Column(Boolean, default=False)

engine = create_engine('sqlite:///kemgu_bot.db')
Base.metadata.create_all(engine)