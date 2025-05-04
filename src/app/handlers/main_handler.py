from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.states import AddOrder
from app.keyboards import get_products_kb, get_product_counter, START_KB
from app.db import crud

router = Router()


@router.callback_query(F.data == "add_order")
async def add_order(call_back: CallbackQuery, state: FSMContext):
    await call_back.answer("Buyurtma qo'shish")
    user = call_back.from_user

    await state.set_state(AddOrder.customer)
    await call_back.message.edit_text(
        "Buyurtma qo'shish uchun buyurtmachini ismini jo'nating."
    )


@router.message(AddOrder.customer)
async def add_customer(message: Message, state: FSMContext):
    text = message.text

    await state.update_data(customer=text)
    user_id = await crud.get_user_id_by_tg(message.from_user.id)
    products = await crud.get_products_by_user_id(user_id)

    if len(products) == 0:
        await message.answer(
            "Hozirda sizning mahsulotlar bizning ma'lumotlar bazamizga qo'shilmagan. \
                             \nIltimos mahsulotlaringizni bazamizga qo'sha olishimiz uchun adminga aloqaga chiqing."
        )
        return

    await state.set_state(AddOrder.products)
    await message.answer(
        "Mahsulotni tanlang.", reply_markup=await get_products_kb(products)
    )


@router.callback_query(F.data.startswith("product_"), AddOrder.products)
async def add_product(call_back: CallbackQuery, state: FSMContext):
    await call_back.answer("Mahsulot tanlandi")
    product_id = call_back.data.split("_")[1]
    agent_id = call_back.from_user.id

    info = "Buyurtma:"
    customer = (await state.get_data())["customer"]
    info += f"\nBuyurtmachi: {customer}"
    product = await crud.get_product(product_id)
    info += f"\n\nMahsulot nomi: {product.title}"
    info += f"\nMahsulot narxi: {product.price}"
    info += f"\nMahsulot haqida: {product.desc}"
    info += f"\n\nMahsulot soni: 1"

    order = await crud.add_order(agent_id, customer, product_id)

    await state.set_state(AddOrder.count_products)
    await call_back.message.edit_text(
        info, reply_markup=await get_product_counter(order.id)
    )


@router.callback_query(F.data.startswith("minus_"), AddOrder.count_products)
async def minus_products(call_back: CallbackQuery, state: FSMContext):
    await call_back.answer("Minus")

    count = call_back.data.split("_")[1]
    order_id = call_back.data.split("_")[2]

    order = await crud.get_order(order_id)

    if order.product_count - int(count) >= 1:
        c = order.product_count - int(count)
        order = await crud.add_c_order(order.id, c)
    else:
        return

    info = "Buyurtma:"
    info += f"\nBuyurtmachi: {order.customer}"
    product = await crud.get_product(order.product_id)
    info += f"\n\nMahsulot nomi: {product.title}"
    info += f"\nMahsulot narxi: {product.price}"
    info += f"\nMahsulot haqida: {product.desc}"
    info += f"\n\nMahsulot soni: {order.product_count}"

    await call_back.message.edit_text(
        info, reply_markup=await get_product_counter(order.id)
    )


@router.callback_query(F.data.startswith("plus_"), AddOrder.count_products)
async def minus_products(call_back: CallbackQuery, state: FSMContext):
    await call_back.answer("Plus")

    count = call_back.data.split("_")[1]
    order_id = call_back.data.split("_")[2]

    order = await crud.get_order(order_id)

    c = order.product_count + int(count)
    order = await crud.add_c_order(order.id, c)

    info = "Buyurtma:"
    info += f"\nBuyurtmachi: {order.customer}"
    product = await crud.get_product(order.product_id)
    info += f"\n\nMahsulot nomi: {product.title}"
    info += f"\nMahsulot narxi: {product.price}"
    info += f"\nMahsulot haqida: {product.desc}"
    info += f"\n\nMahsulot soni: {order.product_count}"

    await call_back.message.edit_text(
        info, reply_markup=await get_product_counter(order.id)
    )


@router.callback_query(F.data.startswith("complete_"), AddOrder.count_products)
async def minus_products(call_back: CallbackQuery, state: FSMContext):
    await call_back.answer("Complete")

    order_id = call_back.data.split("_")[1]

    await crud.complete_order(order_id)
    await state.clear()

    await call_back.message.edit_text(
        "➕Buyurtma 'Buyurtmalar tarixi' bo'limiga qo'shildi"
    )
    await call_back.message.answer(text="Menu: ", reply_markup=START_KB)


@router.callback_query(F.data == "history")
async def history(call_back: CallbackQuery):
    await call_back.answer("Tarix")

    user = call_back.from_user
    user_id = await crud.get_user_id_by_tg(user.id)
    orders = await crud.get_orders(user_id)

    if len(orders) == 0:
        await call_back.message.answer(
            "Sizda buyurtmalar tarixi bo'sh, chunki buyurtma qo'shmagansiz."
        )
    else:
        i = 1
        for order in orders:
            info = f"{1}.Buyurtma: "
            info += f"\nBuyurtmachi: {order.customer}"
            product = await crud.get_product(order.product_id)
            info += f"\n\nMahsulot nomi: {product.title}"
            info += f"\nMahsulot narxi: {product.price}"
            info += f"\nMahsulot haqida: {product.desc}"
            info += f"\n\nMahsulot soni: {order.product_count}"

            await call_back.message.answer(info)
            i += 1

    await call_back.message.answer(text="Menu: ", reply_markup=START_KB)
