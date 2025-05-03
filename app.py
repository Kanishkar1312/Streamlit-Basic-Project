'''
Entry Point of the project -

Gets data from the JSON files present,
inserts them into the database, then calls streamlit UI

'''

import json
from Constant.Constant import CompetitionsJSONPath,ComplexJSONPath, DoubleCompetitorJSONPath
from SeedData import ProcessCategories, ProcessCompetitions, PrcoessComplexes, ProcessRankings
from SportsRadarResponseModels import Competition as ResponseCompetition, Complex as ResponseComplex, Ranking as ResponseRanking
from DatabaseUtilities import CreateConnnectDatabase


conn = CreateConnnectDatabase()
cursor = conn.cursor()

with open(CompetitionsJSONPath) as f:
    competitions_payload = ResponseCompetition.CompetitionPayLoad(**json.load(f))
    competitions = competitions_payload.competitions

with open(ComplexJSONPath) as f:
    complexes_payload = ResponseComplex.ComplexPayLoad(**json.load(f))
    complexes = complexes_payload.complexes

with open(DoubleCompetitorJSONPath) as f:
    rankings_payload = ResponseRanking.RankingPayload(**json.load(f))
    rankings = rankings_payload.rankings

ProcessCategories(cursor, competitions)
ProcessCompetitions(cursor, competitions)
PrcoessComplexes(cursor, complexes)
ProcessRankings(cursor, rankings)

conn.commit()
conn.close()