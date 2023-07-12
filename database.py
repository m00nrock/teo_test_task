from datetime import datetime as dt

from sqlalchemy import BigInteger, Column, Date, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()
now = dt.now()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, unique=True)
    name = Column(String, nullable=True, default='')
    user_question = Column(Text, nullable=True, default='')
    register_date = Column(Date, nullable=True, default=now.date())
