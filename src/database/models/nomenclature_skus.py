from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base

__all__ = ('NomenclatureSku',)


class NomenclatureSku(Base):
    __tablename__ = 'nomenclature_sku'

    nomenclature_id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(primary_key=True)
