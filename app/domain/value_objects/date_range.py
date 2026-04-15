from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class DateRange:
    start_date: date
    end_date: date

    def __post_init__(self) -> None:
        if self.start_date > self.end_date:
            raise ValueError("start_date cannot be after end_date")
