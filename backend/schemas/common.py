from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict
class APIModel(BaseModel): model_config = ConfigDict(from_attributes=True)
class Message(APIModel): message: str
class Pagination(APIModel): total: int; limit: int; offset: int
class ErrorDetail(APIModel): code: str; message: str
