from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, UniqueConstraint

from .db_settings import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    out_user_id = Column(Integer, unique=True)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    def __repr__(self) -> str:
        return "<User(fullname='%s %s')>" % (
               self.first_name, self.last_name)


class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    message = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='logs')

    __table_args__ = (UniqueConstraint('date', 'message', 'user_id'),)

    def __str__(self) -> str:
        return f'{self.date}: {self.message} by user {self.user}'

    def __repr__(self) -> str:
        return f'{self.date}: {self.message} by user {self.user}'
