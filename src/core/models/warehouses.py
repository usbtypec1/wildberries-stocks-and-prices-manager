from pydantic import BaseModel

__all__ = ('Warehouse',)


class Warehouse(BaseModel):
    id: int
    name: str
