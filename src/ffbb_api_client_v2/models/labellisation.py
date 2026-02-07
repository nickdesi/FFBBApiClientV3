from __future__ import annotations

from typing import Any

from ..utils.converter_utils import from_int


class Labellisation:
    basket_santé_résolutions: int | None = None
    micro_basket: int | None = None

    def __init__(
        self,
        basket_santé_résolutions: int | None,
        micro_basket: int | None,
    ) -> None:
        self.basket_santé_résolutions = basket_santé_résolutions
        self.micro_basket = micro_basket

    @staticmethod
    def from_dict(obj: Any) -> Labellisation:
        assert isinstance(obj, dict)
        basket_santé_résolutions = from_int(obj, "Basket Santé / Résolutions")
        micro_basket = from_int(obj, "Micro Basket")
        return Labellisation(basket_santé_résolutions, micro_basket)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.basket_santé_résolutions is not None:
            result["Basket Santé / Résolutions"] = self.basket_santé_résolutions
        if self.micro_basket is not None:
            result["Micro Basket"] = self.micro_basket
        return result
