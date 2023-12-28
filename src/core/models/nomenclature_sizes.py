from pydantic import BaseModel, Field

__all__ = ('NomenclatureSize',)


class NomenclatureSize(BaseModel):
    tech_size: str = Field(alias='techSize')
    skus: list[str]
