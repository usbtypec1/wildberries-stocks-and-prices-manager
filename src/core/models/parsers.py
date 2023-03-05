from pydantic import BaseModel

__all__ = (
    'SupplierCredentials',
)


class SupplierCredentials(BaseModel):
    shop_name: str
    api_key: str
