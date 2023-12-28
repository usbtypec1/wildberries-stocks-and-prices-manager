from datetime import datetime

from pydantic import BaseModel, Field

from core.models.nomenclature_sizes import NomenclatureSize

__all__ = ('Nomenclature',)


class Nomenclature(BaseModel):
    id: int = Field(alias='nmID')
    sizes: list[NomenclatureSize]
    media_files: list[str] = Field(alias='mediaFiles')
    colors: list[str]
    update_at: datetime = Field(alias='updateAt')
    vendor_code: str = Field(alias='vendorCode')
    brand: str
    object: str
