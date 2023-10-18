from sqlalchemy import Column, String, BigInteger
from bot.loader import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, unique=True)
    name = Column(String)
    city = Column(String)


