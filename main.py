"""This is a echo bot.

It echoes any incoming text messages.
"""

import logging
import os

from aiogram import Bot, Dispatcher, executor, types
import aiohttp

API_TOKEN = os.environ.get('TG_API_TOKEN', '')
KORONA_URL = 'https://koronapay.com'

# Configure logging
log = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Handler called when user sends `/start` or `/help`."""
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


TEST_PARAMS = {
    'sendingCountryId': 'RUS',
    'sendingCurrencyId': 810,
    'receivingCountryId': 'TUR',
    'receivingCurrencyId': '949',
    'paymentMethod': 'debitCard',
    'receivingAmount': 1000,
    'receivingMethod': 'cash',
    'paidNotificationEnabled': 'false',
}

@dp.message_handler(commands=['korona'])
async def rates(message: types.Message):
    """Echo handler."""
    msg = ''
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'{KORONA_URL}/transfers/online/api/transfers/tariffs',
            params=TEST_PARAMS,
        ) as resp:
            rates = await resp.json()
            if resp.status != 200:
                msg = 'Something happend :('
            rub_tl = rates[0]['exchangeRate']
            msg = f'RUB/TL: {rub_tl}'
    await message.answer(msg)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
