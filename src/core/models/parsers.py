from dataclasses import dataclass

from pydantic import BaseModel

__all__ = (
    'SupplierCredentials',
)


@dataclass(frozen=True, slots=True)
class SupplierCredentials:
    shop_name: str
    api_key: str
