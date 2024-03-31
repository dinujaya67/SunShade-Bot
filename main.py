import asyncio
import logging
import sys
import requests

from dotenv import load_dotenv
from os import getenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold, hitalic

load_dotenv()

TOKEN = getenv('BOT_API')
ADMIN = int(getenv('ADMIN_ID'))
API_key = getenv('APIkey')
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message:Message):
    await message.answer(f'Hi {hbold(message.from_user.first_name)}!\n"SunShade Bot" is a weather bot designed to provide users with real-time weather updates and forecasts. With its intuitive interface, users can easily request weather information for their desired locations, helping them plan their day effectively. Whether it\'s checking the current temperature, getting a detailed forecast for the week, or receiving alerts for severe weather conditions, SunShade Bot ensures users stay informed and prepared. Additionally, the bot sends notifications when significant weather changes occur, keeping users updated on the go. Powered by accurate weather data, SunShade Bot is your reliable companion for staying ahead of the elements.')
    await message.answer(
        f"You can start like this /weather [city name] {hitalic(hbold('Example:'))} {hitalic('/weather London')}"
    )
    
@dp.message(Command('help'))
async def start_handler(message:Message):
    await message.answer(
        f"You can start like this /weather [city name] {hitalic(hbold('Example:'))} {hitalic('/weather London')}"
    )
    
@dp.message(Command('weather'))
async def access_weather(message: Message):
    text = message.text.strip()
    parts = text.split(maxsplit=1)
    args = parts[1] if len(parts) > 1 else await message.answer('Send command with city name')

    city = ''.join(args)

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    response = requests.get(url)
    data = response.json()

    if data['cod'] == 200:
        weather_desc = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        msg_text = f"Weather in {city}: {weather_desc}\nTemperature: {temperature}°C\nHumidity: {humidity}%\nWind Speed: {wind_speed} m/s"
    else:
        msg_text = "City not found. Please enter a valid city name."

    await message.answer(msg_text)

async def on_startup(bot: Bot):
    # Send a message to admin when bot start
    await bot.send_message(chat_id=ADMIN, text="Bot Started... 🤖✨")

async def on_shutdown(bot: Bot):
    # Send a message to admin when bot stop
    await bot.send_message(chat_id=ADMIN, text="Bot Stoped... 🤖✨")

async def handle_non_command(message):
    # Handle non-command messages here
    await message.answer("I'm sorry, I can only respond to commands. type /help to get assist")

async def main()->None:
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.message.register(handle_non_command)
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())