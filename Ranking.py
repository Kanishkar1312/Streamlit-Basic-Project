from typing import List, Optional, Union
from pydantic import BaseModel, ConfigDict

class Competitor(BaseModel):
    id: Union[str, int]
    name: str = ""
    country: str = ""
    country_code: str = ""
    abbreviation: str = ""

class CompetitorRanking(BaseModel):
    rank: Union[str, int]
    movement: int
    points: int
    competitions_played: int
    competitor: Competitor

class Ranking(BaseModel):
    type_id: Union[str, int]
    name: str= ""
    year: int= ""
    week: int= ""
    gender: str= ""
    competitor_rankings: Optional[List[CompetitorRanking]] 

class RankingPayload(BaseModel):
    generated_at: str
    rankings: List[Ranking]
    model_config = ConfigDict(arbitrary_types_allowed=True) 
