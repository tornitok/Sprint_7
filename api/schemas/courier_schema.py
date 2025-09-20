from typing import List, Tuple

from pydantic import BaseModel, RootModel


class CourierLoginArray(RootModel):
    root: List[Tuple[str, str]]


class CourierLoginResponse(BaseModel):
    message: int


class CourierCreateArray(RootModel):
    root: List[Tuple[str, str, str]]


class CourierCreateResponse(BaseModel):
    message: str


