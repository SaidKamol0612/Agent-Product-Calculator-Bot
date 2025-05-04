from sqlalchemy import select, delete

from app.db.models import User, Product, Order
from app.db.helper import db_helper


async def set_user(tg_id, username):
    async with db_helper.session_factory() as session:
        stmt = select(User).where(User.tg_id == tg_id)
        user = await session.scalar(stmt)

        if not user:
            user = User(tg_id=tg_id, username=username)
            session.add(user)
        else:
            user.username = username

        await session.commit()

        return True


async def get_user_id_by_tg(tg_id):
    async with db_helper.session_factory() as session:
        stmt = select(User).where(User.tg_id == tg_id)
        user = await session.scalar(stmt)

        return user.id


async def get_products_by_user_id(user_id) -> list[Product]:
    async with db_helper.session_factory() as session:
        stmt = select(Product).where(Product.agent_id == user_id)
        products = await session.scalars(stmt)

        return [product for product in products]


async def get_product(product_id):
    async with db_helper.session_factory() as session:
        stmt = select(Product).where(Product.id == product_id)
        product = await session.scalar(stmt)

        return product


async def add_order(agent_tg_id, customer, product_id):
    async with db_helper.session_factory() as session:
        user_id = await get_user_id_by_tg(agent_tg_id)
        new_order = Order(agent_id=user_id, customer=customer, product_id=product_id)

        session.add(new_order)
        await session.commit()
        return new_order


async def get_order(order_id):
    async with db_helper.session_factory() as session:
        stmt = select(Order).where(Order.id == order_id)
        order = await session.scalar(stmt)

        return order


async def comm():
    async with db_helper.session_factory() as session:
        await session.commit()


async def add_c_order(order_id, count):
    async with db_helper.session_factory() as session:
        stmt = select(Order).where(Order.id == order_id)
        order = await session.scalar(stmt)

        order.product_count = count
        await session.commit()
        await session.refresh(order)

        return order


async def complete_order(order_id):
    async with db_helper.session_factory() as session:
        stmt = select(Order).where(Order.id == order_id)
        order = await session.scalar(stmt)

        order.is_complete = True
        await session.commit()
        await session.refresh(order)

        return order


async def clear_non_complete_orders(user_id: int):
    async with db_helper.session_factory() as session:
        await session.execute(
            delete(Order).where(Order.agent_id == user_id, Order.is_complete == False)
        )
        await session.commit()


async def get_orders(user_id) -> list[Order]:
    async with db_helper.session_factory() as session:
        stmt = select(Order).where(Order.agent_id == user_id)
        orders = await session.scalars(stmt)

        return [order for order in orders]
