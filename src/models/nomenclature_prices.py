from pydantic import BaseModel, Field, PositiveInt

__all__ = ('NomenclaturePrice', 'NomenclaturePriceToUpdate')


class NomenclaturePrice(BaseModel):
    nomenclature_id: int = Field(alias='nmId')
    price: int
    discount: int


class NomenclaturePriceToUpdate(BaseModel):
    nomenclature_id: int
    price: PositiveInt
