from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from database.connector import Base


class Code(Base):
    __tablename__ = 'code'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    code = Column(String(255))
    receipt_code = Column(String(255))
    used = Column(Boolean, default=False)

    user = relationship('User', back_populates='codes')
