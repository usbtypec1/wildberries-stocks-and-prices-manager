from sqlalchemy.orm import mapped_column, Mapped

from database.base import Base

__all__ = ('SkuStock',)


class SkuStock(Base):
    __tablename__ = 'sku_stocks'

    sku: Mapped[str] = mapped_column(primary_key=True)
    warehouse_id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[int]
