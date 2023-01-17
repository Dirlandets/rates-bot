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


REQUEST_PARAMS = {
    'sendingCountryId': 'RUS',
    'sendingCurrencyId': 810,
    'receivingCountryId': 'TUR',
    'paymentMethod': 'debitCard',
    'receivingAmount': 1000,
    'receivingMethod': 'cash',
    'paidNotificationEnabled': 'false',
}

CURR_MAP = {
    'usd': 840,
    'eur': 978,
    'try': 949,
    'rub': 810,
    'gel': 981,
}

DEFAULT_CURR = 'try'

@dp.message_handler(commands=['korona'])
async def korona(message: types.Message):
    """Echo handler."""
    args = message.text.lower().split()[1:]
    currency = args[0] if args else DEFAULT_CURR
    currency_code = CURR_MAP.get(currency)
    print(f'{args}, {currency}, {currency_code}')

    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'{KORONA_URL}/transfers/online/api/transfers/tariffs',
            params={
                **REQUEST_PARAMS,
                'receivingCurrencyId': str(currency_code),
            },
        ) as resp:
            rates = await resp.json()
            print(rates)
            if resp.status != 200:
                msg = 'Something happend :('
            rate = rates[0]['exchangeRate']
            msg = f'{currency.upper()}:RUB: {rate}'
    await message.answer(msg)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
