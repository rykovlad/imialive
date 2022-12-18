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
mode = config.MODE

# holy shit
@dp.message_handler(commands=['is_bot_alive'])
async def process_is_bot_alive(message: types.Message):
    await bot.send_message(message.chat.id, "так, " + message.from_user.first_name + ", світло і інет є")


@dp.message_handler(commands=['update_bot_on_server'])
async def process_update_bot_on_server(message: types.Message):
    if message.from_id in config.BOSSES_ID:
        import subprocess
        subprocess.call(config.PATH_TO_UPDATER_SCRIPT)
        await message.reply("done)")
    else:
        await message.reply("fuck oF")


@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message():
    pass


async def scheduler():
    await send_4_all()
    aioschedule.every(3).minutes.do(send_4_all)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def send_4_all():
    if mode == "release":
        try:
            await bot.send_message(config.CHANNEL_ID_LOGS, config.MSG_LOGS)
            ob.new_state = 1
        except NetworkError as e:
            print("noooo \n", e)
            ob.new_state = 0

        if (ob.state != ob.new_state) & (ob.new_state == 1):
            await bot.send_message(config.CHANNEL_ID_LOGS, config.MSG_LIGHT_BACK)
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
        time.sleep(31)
