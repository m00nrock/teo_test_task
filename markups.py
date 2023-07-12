from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

question = KeyboardButton('Какой был вопрос?')
register = KeyboardButton('Сколько я уже тут?')

main_menu = ReplyKeyboardMarkup(
    resize_keyboard=True).add(question).add(register)
