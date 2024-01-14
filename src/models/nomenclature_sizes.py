from pydantic import BaseModel, Field, ConfigDict

__all__ = ('NomenclatureSize',)


class NomenclatureSize(BaseModel):
    tech_size: str = Field(alias='techSize')
    skus: list[str]

    model_config = ConfigDict(populate_by_name=True)
