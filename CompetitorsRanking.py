from typing import List, Optional, Union


class Competitor:
    id: Union[str, int]
    name: str = ""
    country: str = ""
    country_code: str = ""
    abbreviation: str = ""


class CompetitionRanking:
    rank: Union[str, int]
    movement: int
    points: int
    competitions_played: int
    competitor: Optional[Competitor] = None


class CompetitorPayLoad():
    generated_at: str
    competitor_rankings: List[CompetitionRanking] = []