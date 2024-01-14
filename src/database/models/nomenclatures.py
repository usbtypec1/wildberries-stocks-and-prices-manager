from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base

__all__ = ('Nomenclature',)


class Nomenclature(Base):
    __tablename__ = 'nomenclatures'

    id: Mapped[int] = mapped_column(primary_key=True)
    subject_name: Mapped[str] = mapped_column()
    price: Mapped[int | None]
    discount: Mapped[int | None]
