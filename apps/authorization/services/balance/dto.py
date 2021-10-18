from dataclasses import dataclass
from typing import Optional


@dataclass
class CreateBalanceRecordDTO:
    client_id: int
    sum_in_jpy: int
    payment_type: str
    sender_name: str
    comment: str
    date: Optional[str] = None
    sum_in_usa: Optional[int] = None
    rate: Optional[int] = None
