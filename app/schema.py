from pydantic import BaseModel
import datetime
from typing import Literal
from constant import SUCCCESS_RESPONSE


class IdResponse(BaseModel):
    id: int


class SuccessResponse(BaseModel):
    status: Literal["success"]


class createAdvRequest(BaseModel):
    Title: str
    Price: int | None = None
    Description: str | None = None
    Author: str


class CreateAdvResponse(IdResponse):
    pass


class UpdateAdvResponse(SuccessResponse):
    pass


class UpdateAdvRequest(BaseModel):
    Title: str | None = None
    Price: int | None = None
    Description: str | None = None


class GetAdvResponse(BaseModel):
    id: int
    Title: str
    Price: int
    Description: str 
    Author: str
    Create_time: datetime.datetime


class DeleteAdvResponse(SuccessResponse):
    pass


class SearchAdvResponse(BaseModel):
    results: list[GetAdvResponse]
