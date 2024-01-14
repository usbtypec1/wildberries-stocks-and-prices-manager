from pydantic import BaseModel, ConfigDict

__all__ = ('NomenclatureSize',)


class NomenclatureSize(BaseModel):
    skus: list[str]

    model_config = ConfigDict(populate_by_name=True)
