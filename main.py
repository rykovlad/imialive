import asyncio
import pprint
import time
import aioschedule

from datetime import datetime

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
mode = config.MODE


@dp.message_handler(commands=['is_bot_alive'])
async def process_is_bot_alive(message: types.Message):
    await bot.send_message(message.chat.id, "так, " + message.from_user.first_name + ", світло і інет є. не спам пліз")


@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message():
    pass


async def scheduler():
    await send_4_all()
    aioschedule.every(2).minutes.do(send_4_all)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def send_4_all():
    if mode == "release" and ob.state:
        if ob.is_first:
            ob.m = await bot.send_message(config.CHANNEL_ID, config.MSG_LIGHT_BACK)
            await bot.send_message(config.CHANNEL_ID_LOGS, config.MSG_LIGHT_BACK)
            ob.time_internet_start = datetime.now().strftime("%d/%m/%Y, %H:%M")
            ob.is_first = 0
        else:
            text = config.MSG_LIGHT_BACK
            text = text + "\nсвітло вернулось в " + time_power_start
            text = text + "\nінет вернувся    в " + ob.time_internet_start
            text = text + "\nбули востаннє    в " + datetime.now().strftime("%d/%m/%Y, %H:%M")
            await ob.m.edit_text(text)
            await bot.send_message(config.CHANNEL_ID_LOGS, config.MSG_LOGS)


async def on_startup(_):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    time_power_start = datetime.now().strftime("%d/%m/%Y, %H:%M")
    while True:
        try:
            executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
        except NetworkError as e:
            print(e)
        time.sleep(15)
