import asyncio
import pprint
import time

import aioschedule
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram.utils import executor
from aiogram.utils.exceptions import NetworkError
from aiogram.utils.json import json

import config
from observer import Observer

bot = Bot(token=config.BOT_TOKEN)

dp = Dispatcher(bot)
ob = Observer()


@dp.message_handler(commands=['do_it_4_all'])
async def process_do_it_4_all(message: types.Message):
    await bot.send_message(config.CHANNEL_ID_LOGS, config.MSG_LOGS)


@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(msg: types.Message):
    pprint.pprint(json(msg))
    await msg.reply('fuck off, i dont know how to react 2 this shit')


async def scheduler():
    aioschedule.every(2).seconds.do(send_4_all)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def send_4_all():
    try:
        await bot.send_message(config.CHANNEL_ID_LOGS, config.MSG_LOGS)
        ob.new_state = 1
    except NetworkError as e:
        print("noooo \n", e)
        ob.new_state = 0

    if (ob.state != ob.new_state) & (ob.new_state == 1):
        await bot.send_message(config.CHANNEL_ID, config.MSG_LIGHT_BACK)
    elif ob.new_state == 0:
        pass  # mb it will be msg when power off, but i`m not sure
    ob.state = ob.new_state

async def on_startup(_):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    while True:
        try:
            executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
        except NetworkError as e:
            print(e)
        time.sleep(30)
