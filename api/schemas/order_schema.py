from typing import Tuple

from pydantic import BaseModel, RootModel
from typing import List


class OrderListArray(RootModel):
    root: List[Tuple[int, str, int, int]]

class PageInfo(BaseModel):
    page: int
    total: int
    limit: int

class Station(BaseModel):
    name: str
    number: str
    color: str

class OrderListResponse(BaseModel):
    orders: List[OrderListArray]
    pageInfo: PageInfo
    availableStations: List[Station]

class OrderCreateArray(RootModel):
    root: List[Tuple[str, str, str, int, str, int, str, str, List[str]]]

class OrderCreateResponse(BaseModel):
    firstName: str
    lastName: str
    address: str
    metroStation: int
    phone: str
    rentTime: int
    deliveryDate: str
    comment: str
    color: List[str]


