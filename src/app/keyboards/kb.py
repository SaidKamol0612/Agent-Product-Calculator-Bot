from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


START_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📑Buyurtmalar tarixi", callback_data="history"),
            InlineKeyboardButton(text="➕Buyurtma qo'shish", callback_data="add_order"),
        ]
    ]
)


async def get_products_kb(products):

    keyboard = InlineKeyboardBuilder()

    for product in products:
        keyboard.add(
            InlineKeyboardButton(
                text=product.title, callback_data=f"product_{product.id}"
            )
        )

    return keyboard.adjust(1).as_markup()


async def get_product_counter(order_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="-10", callback_data=f"minus_10_{order_id}"),
                InlineKeyboardButton(text="-1", callback_data=f"minus_1_{order_id}"),
                InlineKeyboardButton(text="+1", callback_data=f"plus_1_{order_id}"),
                InlineKeyboardButton(text="+10", callback_data=f"plus_10_{order_id}"),
            ],
            [InlineKeyboardButton(text="✅Buyurtmani tayyor", callback_data=f"complete_{order_id}")],
        ]
    )
