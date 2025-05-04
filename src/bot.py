import sys
import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from aiogram.fsm.context import FSMContext

from app.core.config import settings
from app.db import db_helper
from app.db import crud
from app.handlers import main_router
from app.keyboards import START_KB

dispatcher = Dispatcher()


async def main():
    await db_helper.init_db()

    bot = Bot(
        token=settings.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dispatcher.include_router(main_router)

    await dispatcher.start_polling(bot)


@dispatcher.message(CommandStart())
async def cmd_start(message: Message):
    user = message.from_user

    await crud.set_user(user.id, user.username)

    start_msg = f"Assalomu alaykum @{user.username}!\n"
    start_msg += (
        f"Bu Telegram bot sizga buyurtmaga mahsulotlarni hisoblashga yordam beradi.\n"
    )

    await message.answer(text=start_msg, reply_markup=START_KB)


@dispatcher.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    user = message.from_user
    await crud.clear_non_complete_orders(user.id)
    await state.clear()
    
    await message.answer("Buyurtma qo'shish bekor qilindi")
    await message.answer(text="Menu: ", reply_markup=START_KB)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except:
        print("Bot stopped.")
    finally:
        asyncio.run(db_helper.dispose())
