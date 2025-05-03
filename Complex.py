from typing import List, Union
from pydantic import BaseModel, ConfigDict


class Venue(BaseModel):
    id: Union[str, int]
    name: str
    city_name: str
    country_name: str
    country_code: str
    timezone: str

class Complex(BaseModel):
    id: Union[str, int]
    name: str
    venue: List[Venue] = []

class ComplexPayLoad(BaseModel):
    generated_at: str
    complexes: List[Complex]
    model_config = ConfigDict(arbitrary_types_allowed=True) 