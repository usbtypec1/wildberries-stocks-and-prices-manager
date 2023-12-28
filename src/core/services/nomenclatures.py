from core.models import Nomenclature


def collect_nomenclature_skus(nomenclature: Nomenclature) -> set[str]:
    return {
        sku
        for size in nomenclature.sizes
        for sku in size.skus
        if sku
    }
