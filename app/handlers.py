from typing import Any, Dict
from aiogram import F, Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    
)

router = Router()
bot = Bot(token='TOKEN')

class From(StatesGroup):
    first = State()
    second = State()
    third = State()
    photo = State()


@router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(From.first)
    await message.answer( "Начнем тест. Введите текст:")

@router.message(From.first)
async def process_first_step(message: Message, state: FSMContext) -> None:
    await state.update_data(first_text=message.text)
    await state.set_state(From.second)
    await message.answer("Введите текст второй раз:")

@router.message(From.second)
async def process_second_step(message: Message, state: FSMContext)-> None:
    data = await state.get_data()
    data['second_text'] = message.text
    await state.update_data(**data)
    await state.set_state(From.third)
    await message.answer("Введите текст третий раз:")

@router.message(From.third)
async def process_third_step(message: Message, state: FSMContext)-> None:
    data = await state.get_data()
    data['third_text'] = message.text
    await state.update_data(**data)
    await state.set_state(From.photo)
    await message.answer("Теперь отправьте фото:")


@router.message(From.photo, F.content_type.in_({'photo'}))
async def process_photo_step(message: Message, state: FSMContext):
    data = await state.get_data()
    photo_id = message.photo[-1].file_id
    caption = f"Тексты:\n\n1. {data['first_text']}\n2. {data['second_text']}\n3. {data['third_text']}"
    await bot.send_photo('@chanel', photo_id, caption=caption)
    await message.answer("Спасибо! Ваша информация была успешно отправлена в канал.")
    await state.clear()

@router.message(From.photo, F.content_type.in_({'text', 'sticker'}))
async def process_photo_step(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, отправьте фото.")