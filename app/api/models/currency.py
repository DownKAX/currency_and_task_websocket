from pydantic import BaseModel
from typing import Union

class Currency(BaseModel):
    currency_code1: str
    currency_code2: str
    amount: Union[float | int] = 1
