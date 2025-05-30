import randomimport os
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor

API_TOKEN = os.getenv("API_TOKEN")  # Токен берётся из переменных окружения

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Простая система баланса
user_balances = {}

# Команда /start
@dp.message_handler(commands=['start'])
async def start_handler(message: Message):
    user_id = message.from_user.id
    user_balances[user_id] = 1000
    await message.answer("🎰 Добро пожаловать в казино-бот!\nУ тебя 1000 монет.\nИспользуй /spin чтобы играть!")

# Команда /balance
@dp.message_handler(commands=['balance'])
async def balance_handler(message: Message):
    user_id = message.from_user.id
    balance = user_balances.get(user_id, 0)
    await message.answer(f"💰 Твой баланс: {balance} монет")

# Команда /spin
@dp.message_handler(commands=['spin'])
async def spin_handler(message: Message):
    user_id = message.from_user.id
    balance = user_balances.get(user_id, 0)

    if balance < 100:
        await message.answer("❌ Недостаточно монет для спина (нужно 100).")
        return

    user_balances[user_id] -= 100
    symbols = ['🍒', '🍋', '🔔', '⭐', '7️⃣']
    result = [random.choice(symbols) for _ in range(3)]

    win = 0
    if result[0] == result[1] == result[2]:
        win = 500
        user_balances[user_id] += win
        outcome = "🎉 Джекпот! Ты выиграл 500 монет!"
    elif result[0] == result[1] or result[1] == result[2] or result[0] == result[2]:
        win = 200
        user_balances[user_id] += win
        outcome = "✨ Малый выигрыш! Ты получил 200 монет."
    else:
        outcome = "😢 Ничего не выпало."

    await message.answer(f"{' | '.join(result)}\n{outcome}\n💰 Баланс: {user_balances[user_id]} монет")

if __name__ == '__main__':
    executor.start_polling(dp)
