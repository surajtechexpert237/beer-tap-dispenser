from datetime import datetime
from typing import Union

from pydantic import BaseModel

from apps.common.schemas import ResponseMessage


class OpenDispenserTaoSchema(BaseModel):
    dispenser_id: str


class OpenDispenserTapResponseSchema(BaseModel):
    id: str
    dispenser_id: str
    open_time: datetime
    status: bool


class OpenDispenserResponseSchema(ResponseMessage):
    data: Union[OpenDispenserTapResponseSchema, None]
