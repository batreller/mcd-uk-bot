from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.connector import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, unique=True)
    username = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255), nullable=True)
    language = Column(String(15), default='no')

    codes = relationship('Code', back_populates='user')
