from pydantic import BaseModel, Field, field_validator

__all__ = ('NomenclatureSize',)


class NomenclatureSize(BaseModel):
    tech_size: str = Field(alias='techSize')
    skus: list[str]

    @field_validator('skus')
    @classmethod
    def filter_empty_skus(cls, value: list[str]) -> list[str]:
        return [sku for sku in value if sku]
