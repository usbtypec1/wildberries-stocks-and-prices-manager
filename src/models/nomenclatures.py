from pydantic import BaseModel, Field, ConfigDict

from models import NomenclatureSize

__all__ = ('Nomenclature', 'NomenclatureWithPrice')


class Nomenclature(BaseModel):
    id: int = Field(alias='nmID')
    subject_name: str = Field(alias='subjectName')
    sizes: list[NomenclatureSize]

    model_config = ConfigDict(populate_by_name=True)

    @property
    def skus(self) -> set[str]:
        return {
            sku
            for size in self.sizes
            for sku in size.skus
        }


class NomenclatureWithPrice(Nomenclature):
    price: int
    discount: int

    model_config = ConfigDict(populate_by_name=True)
