from sqlalchemy import BigInteger, String, ForeignKey, Text, Integer, Boolean
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    Mapped,
    mapped_column,
)


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True)


class User(Base):
    tg_id = mapped_column(BigInteger())
    username: Mapped[str] = mapped_column(String())


class Product(Base):
    agent_id: Mapped[int] = mapped_column(
        ForeignKey(User.id, ondelete="cascade", onupdate="cascade")
    )

    title: Mapped[str] = mapped_column(String(30))
    desc: Mapped[str] = mapped_column(Text)
    price: Mapped[int]


class Order(Base):
    agent_id: Mapped[int] = mapped_column(
        ForeignKey(User.id, ondelete="cascade", onupdate="cascade")
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey(Product.id, ondelete="cascade", onupdate="cascade")
    )
    product_count: Mapped[int] = mapped_column(Integer, default=1, server_default="1")
    is_complete: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="False"
    )
    customer: Mapped[str]
