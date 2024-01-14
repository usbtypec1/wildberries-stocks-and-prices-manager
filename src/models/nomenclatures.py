from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from models import NomenclatureSize

__all__ = ('Nomenclature', 'NomenclatureWithPrice')


class Nomenclature(BaseModel):
    id: int = Field(alias='nmID')
    subject_name: str = Field(alias='subjectName')
    brand: str
    sizes: list[NomenclatureSize]
    updated_at: datetime = Field(alias='updatedAt')

    model_config = ConfigDict(populate_by_name=True)


class NomenclatureWithPrice(Nomenclature):
    price: int
    discount: int
    promocode: int

    model_config = ConfigDict(populate_by_name=True)
