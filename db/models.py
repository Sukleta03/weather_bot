from sqlalchemy import Column, String, Boolean, BigInteger
from bot.loader import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, unique=True)
    name = Column(String)
    city = Column(String)
    subscribe = Column(Boolean, default=True)


