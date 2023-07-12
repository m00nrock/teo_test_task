import asyncio
import logging
import os
import sys
from datetime import datetime as dt

import aioschedule
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import scoped_session, sessionmaker

import markups as nav
from database import Base, User


load_dotenv()

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

bot = Bot(token=os.getenv('TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
URI = (f'postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:'
       f'{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("LOCAL_DB")}:{os.getenv("DB_PORT")}'
       f'/{os.getenv("DB_NAME")}')
engine = create_engine(URI)
session = scoped_session(sessionmaker(bind=engine))


class RegistrationState(StatesGroup):
    name = State()
    question = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user = session.query(User).filter(
        User.tg_id == message.from_user.id).first()
    if not user:
        await bot.send_message(
            message.from_user.id,
            'Здравствуйте! Введите своё имя:',
        )
        await RegistrationState.name.set()

    else:
        await bot.send_message(
            message.from_user.id,
            'Здравствуйте! Вы уже зарегистрированы.',
            reply_markup=nav.main_menu
        )


@dp.message_handler(state=RegistrationState.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await RegistrationState.next()
    await bot.send_message(
        message.from_user.id,
        'Введите свой вопрос:',
    )


@dp.message_handler(state=RegistrationState.question)
async def process_question(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['question'] = message.text
    await RegistrationState.next()
    await bot.send_message(
        message.from_user.id,
        'Спасибо за регистрацию!',
        reply_markup=nav.main_menu
    )
    now = dt.now().date()
    user = User(
        tg_id=message.from_user.id,
        name=data['name'],
        user_question=data['question'],
        register_date=now
    )
    try:
        session.add(user)
        session.commit()
        logger.info(f'User {user.name} registered.')
    except IntegrityError as e:
        session.rollback()
        logger.error(f'User {user.name} not registered because {e}.')
    await state.finish()


@dp.message_handler(filters.Text(equals='Какой был вопрос?'))
async def question(message: types.Message):
    user = session.query(User).filter(
        User.tg_id == message.from_user.id).first()
    if user:
        await bot.send_message(
            message.from_user.id,
            f'Ваш вопрос: {user.user_question}',
            reply_markup=nav.main_menu
        )
    else:
        await bot.send_message(
            message.from_user.id,
            'Вы не зарегистрированы.',
            reply_markup=nav.main_menu
        )


@dp.message_handler(filters.Text(equals='Сколько я уже тут?'))
async def register_date(message: types.Message):
    user = session.query(User).filter(
        User.tg_id == message.from_user.id).first()
    now = dt.now().date()
    days_passed = (now - user.register_date).days
    if user:
        await bot.send_message(
            message.from_user.id,
            f'Вы с нами уже {days_passed} дней.',
            reply_markup=nav.main_menu
        )
    else:
        await bot.send_message(
            message.from_user.id,
            'Вы не зарегистрированы.',
            reply_markup=nav.main_menu
        )


async def mailing():
    users = session.query(User).all()
    now = dt.now().date()
    for user in users:
        days_passed = (now - user.register_date).days
        await bot.send_message(
            user.tg_id,
            f'Вы с нами уже {days_passed} дней.'
        )


async def schedule():
    # выполняем рассылку в 17:00 (по системному времени сервера) каждый день
    aioschedule.every().day.at("17:00").do(mailing)
    while True:
        await aioschedule.run_pending()
        logger.info('Waiting...')
        await asyncio.sleep(30)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    loop = asyncio.get_event_loop()
    loop.create_task(schedule())
    executor.start_polling(dp, skip_updates=True)
