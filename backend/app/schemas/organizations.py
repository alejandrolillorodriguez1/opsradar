from pydantic import BaseModel, Field,ConfigDict
from datetime import datetime

class OrganizationCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name : str = Field(min_length = 1, max_length = 200)

class OrganizationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : int
    name : str
    created_at : datetime

