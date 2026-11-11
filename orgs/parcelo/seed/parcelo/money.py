from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP


@dataclass(frozen=True)
class Money:
    cents: int
    currency: str = "USD"

    @classmethod
    def zero(cls):
        return cls(0)

    @classmethod
    def parse(cls, value):
        """Build Money from a dollar amount given as float, int, str or Decimal."""
        if isinstance(value, Money):
            return value
        cents = (Decimal(str(value)) * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        return cls(int(cents))

    def __add__(self, other):
        return Money(self.cents + other.cents, self.currency)

    def __sub__(self, other):
        return Money(self.cents - other.cents, self.currency)

    def scale(self, factor):
        cents = (Decimal(self.cents) * Decimal(str(factor))).quantize(
            Decimal("1"), rounding=ROUND_HALF_UP
        )
        return Money(int(cents), self.currency)

    def __lt__(self, other):
        return self.cents < other.cents

    def __le__(self, other):
        return self.cents <= other.cents

    def __str__(self):
        return f"{self.cents / 100:.2f} {self.currency}"
