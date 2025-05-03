from typing import List, Optional, Union
from pydantic import BaseModel, ConfigDict

class Category(BaseModel):
    id: Union[str, int]
    name: str
class Competition(BaseModel):
    id: Union[str, int]
    name: str
    parent_id: str = 0
    type: str
    gender: str
    level: str = "" 
    category: Optional[Category]
    
class CompetitionPayLoad(BaseModel):
    generated_at: str
    competitions: List[Competition]
    model_config = ConfigDict(arbitrary_types_allowed=True) 