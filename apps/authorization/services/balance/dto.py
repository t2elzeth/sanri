from dataclasses import dataclass
from typing import Optional


@dataclass
class CreateBalanceRecordDTO:
    client_id: int
    date: Optional[str]
    sum_in_jpy: int
    sum_in_usa: Optional[int]
    rate: Optional[int]
    payment_type: str
    sender_name: str
    comment: str
