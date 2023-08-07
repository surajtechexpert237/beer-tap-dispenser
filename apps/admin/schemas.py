from typing import Union

from pydantic import BaseModel

from apps.common.schemas import ResponseMessage


class CreateDispenserSchema(BaseModel):
    flow_volume: float
    price: float


class CreateDispenserResponseSchema(BaseModel):
    id: str
    flow_volume: float
    price: float
    status: bool


class DispenserResponseSchema(ResponseMessage):
    data: Union[CreateDispenserResponseSchema, None]
