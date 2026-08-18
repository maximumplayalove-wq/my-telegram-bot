import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from google import genai

# Вот сюда хостинг будет передавать токен автоматически:
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Системная инструкция для сценариста Initial D
initial_system_instruction = (
    "Ты — сценарист и движок визуальной новеллы по аниме Initial D. "
    "Сейчас идет Серия 1: На заправке работают Такуми и Ицуки. "
    "Форматируй ответ строго так: ИМЯ_ПЕРСОНАЖА: Текст реплики."
)

chat_session = ai_client.chats.create(
    model="gemini-3.6-flash"",
    config={"system_instruction": initial_system_instruction}
)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    intro = (
        "📖 *Initial D: Story Mode*\n\n"
        "Ицуки: Эй, Такуми! Ты слышал? На эти выходные на Акину приезжают гонщики из Red Suns!\n"
        "Такуми: Мда? Мне всё равно, я спать хочу...\n\n"
        "Напиши своё действие или реплику, чтобы продолжить сюжет!"
    )
    await message.answer(intro, parse_mode="Markdown")

@dp.message()
async def handle_message(message: types.Message):
    user_text = message.text
    try:
        response = chat_session.send_message(user_text)
        await message.answer(response.text)
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")

async def main():
    print("Бот запущен и ждет сообщения...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
