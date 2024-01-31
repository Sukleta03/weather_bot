from aiogram import Bot, Dispatcher
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, declarative_base, sessionmaker
import asyncio
import os
import uvloop  # linux
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

os.environ['TZ'] = 'Europe/Kiev'

load_dotenv()

engine = create_engine(os.getenv("DB_URL"), echo=True)
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
token = os.getenv("BOT_TOKEN")
bot = Bot(token=token, parse_mode="html")
scheduler = AsyncIOScheduler()
loop = asyncio.get_event_loop()
dp = Dispatcher(bot, loop=loop)

session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = session.query_property()

