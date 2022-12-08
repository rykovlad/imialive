import asyncio
import pprint

import aioschedule
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram.utils import executor
from aiogram.utils.json import json

import config

bot = Bot(token=config.BOT_TOKEN)

dp = Dispatcher(bot)


@dp.message_handler(commands=['do_it_4_all'])
async def process_do_it_4_all(message: types.Message):
    await bot.send_message(config.CHANNEL_ID, config.MSG)


@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(msg: types.Message):
    await msg.reply('fuck off, i dont know how to react  2 this shit')


async def send_4_all():
    await bot.send_message(config.CHANNEL_ID, config.MSG)


async def scheduler():
    aioschedule.every(2).minutes.do(send_4_all)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
