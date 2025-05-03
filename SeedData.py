

'''
SeedData - Creates Table, Database for the sports  data into the database  
For each class, separate method is used for creation of table and insertion of records

'''



from Constant.Constant import Category, Competition, Competitor, Competitor_Ranking, Complex, Ranking, Venue
from DatabaseUtilities import InsertBulkRecords, CreateTable, GetTableSchema


def ParseId(id):
    return int(id.split(":")[-1])

#Covnerts string Ids to Id 
def ParseIdFields(data: dict) -> dict:
    return {
        k: ParseId(v) if k.endswith("_id") and isinstance(v, str) else v
        for k, v in data.items()
    }

#Remvoves suplicates from json data
def RemoveDuplicateJson(dicts: list[dict]) -> list[dict]:
    seen = set()
    unique = []
    for d in dicts:
        t = tuple(sorted(d.items()))
        if t not in seen:
            seen.add(t)
            unique.append(d)
    return unique


#Categories
def ProcessCategories(cursor, competitions):
    categories = []
    for comp in competitions:
        cat = comp.category.dict()
        cat["id"] = ParseId(cat["id"])
        categories.append(cat)
    categories = RemoveDuplicateJson(categories)
    category_schema = GetTableSchema(categories[0])
    CreateTable(cursor, Category, category_schema,primary_key="id")
    InsertBulkRecords(cursor, Category, categories)


#Competitions
def ProcessCompetitions(cursor, competitions):
    competition_rows = []
    for comp in competitions:
        comp_data = comp.dict(exclude={"category"})
        comp_data = ParseIdFields(comp_data)
        competition_rows.append(comp_data)
    competition_rows = RemoveDuplicateJson(competition_rows)
    competition_schema = GetTableSchema(competition_rows[0])
    CreateTable(cursor, Competition, competition_schema, foreign_keys={"category_id": "Category(id)"},primary_key="id")
    InsertBulkRecords(cursor, Competition, competition_rows)

#Complexes
def PrcoessComplexes(cursor, complexes):
    complex_data_0 = complexes[0].dict(exclude={"venues"})
    complex_data_0 = ParseIdFields(complex_data_0)
    complex_schema = GetTableSchema(complex_data_0)
    CreateTable(cursor, Complex, complex_schema,primary_key="id")

    venue_data_0 = complexes[0].venues[0].dict()
    venue_data_0 = ParseIdFields(venue_data_0)
    venue_data_0["complex_id"] = complex_data_0["id"]
    venue_schema = GetTableSchema(venue_data_0)
    CreateTable(cursor, Venue, venue_schema, foreign_keys={"complex_id": "Complex(id)"},primary_key="id")

    complex_rows = []
    venue_rows = []
    for complex_obj in complexes:
        complex_data = complex_obj.dict(exclude={"venues"})
        complex_data["id"] = ParseId(complex_data["id"])
        complex_rows.append(complex_data)
        for venue in complex_obj.venues:
            venue_data = venue.dict()
            venue_data["id"] = ParseId(venue_data["id"])
            venue_data["complex_id"] = complex_data["id"]
            venue_rows.append(venue_data)
    
    complex_rows = RemoveDuplicateJson(complex_rows)
    venue_rows = RemoveDuplicateJson(venue_rows)
    InsertBulkRecords(cursor, Complex, complex_rows)
    InsertBulkRecords(cursor, Venue, venue_rows)

#ProcessRankins
def ProcessRankings(cursor, rankings):
    ranking_sample = rankings[0].dict(exclude={"competitor_rankings"})
    ranking_schema = GetTableSchema(ranking_sample)
    CreateTable(cursor, Ranking, ranking_schema,primary_key="id")

    competitor_sample = rankings[0].competitor_rankings[0].competitor.dict()
    competitor_sample["id"] = ParseId(competitor_sample["id"])
    competitor_schema = GetTableSchema(competitor_sample)
    CreateTable(cursor, Competitor, competitor_schema,primary_key="id")

    ranking_rel_sample = rankings[0].competitor_rankings[0].dict(exclude={"competitor"})
    ranking_rel_sample["ranking_id"] = 1 
    ranking_rel_sample["competitor_id"] = 1  
    ranking_rel_schema = GetTableSchema(ranking_rel_sample)
    CreateTable(cursor, Competitor_Ranking, ranking_rel_schema, foreign_keys={
        "ranking_id": "Ranking(id)",
        "competitor_id": "Competitor(id)"
    },primary_key="id")

    ranking_rows = []
    competitor_rows = []
    competitor_ranking_rows = []

    for idx, rank_obj in enumerate(rankings):
        rank_data = rank_obj.dict(exclude={"competitor_rankings"})
        ranking_id = idx + 1
        rank_data = ParseIdFields(rank_data)
        ranking_rows.append(rank_data)

        for cr in rank_obj.competitor_rankings:
            comp_data = cr.competitor.dict()
            comp_data = ParseIdFields(comp_data)
            competitor_rows.append(comp_data)

            cr_data = cr.dict(exclude={"competitor"})
            cr_data["ranking_id"] = ranking_id
            cr_data["competitor_id"] = comp_data["id"]
            competitor_ranking_rows.append(cr_data)
    ranking_rows = RemoveDuplicateJson(ranking_rows)
    competitor_rows = RemoveDuplicateJson(competitor_rows)
    competitor_ranking_rows = RemoveDuplicateJson(competitor_ranking_rows)
    InsertBulkRecords(cursor, Ranking, ranking_rows)
    InsertBulkRecords(cursor, Competitor, competitor_rows)
    InsertBulkRecords(cursor, Competitor_Ranking, competitor_ranking_rows)