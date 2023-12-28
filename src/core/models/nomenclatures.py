from datetime import datetime

from pydantic import BaseModel, Field

from core.models import NomenclatureSize

__all__ = ('Nomenclature',)


class Nomenclature(BaseModel):
    id: int = Field(alias='nmID')
    subject_name: str = Field(alias='subjectName')
    brand: str
    sizes: list[NomenclatureSize]
    updated_at: datetime = Field(alias='updatedAt')
