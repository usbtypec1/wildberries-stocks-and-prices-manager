from dataclasses import dataclass

from pydantic import BaseModel, Field, PositiveInt

__all__ = (
    'NomenclaturePrice',
    'NomenclaturePriceToUpdate',
    'NomenclaturePriceWithSubjectName',
)


class NomenclaturePrice(BaseModel):
    nomenclature_id: int = Field(alias='nmId')
    price: int
    discount: int


class NomenclaturePriceToUpdate(BaseModel):
    nomenclature_id: int
    price: PositiveInt


@dataclass(frozen=True, slots=True)
class NomenclaturePriceWithSubjectName:
    nomenclature_id: int
    price: int
    discount: int
    subject_name: str
