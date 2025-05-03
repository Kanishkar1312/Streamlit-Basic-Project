import pymysql
from pymysql.cursors import Cursor
from typing import Dict, List
from Constant.Constant import CREATEDATABASE, CREATETABLE, FOREIGNKEY, REFERENCES, SQL_FLOAT, SQL_INTEGER, SQL_STRING,INSERTINTO, USEDATABASE, VALUES


def CreateConnnectDatabase():
    conn = pymysql.connect(host="localhost",user="root",password="Kanishkar@1312")
    cursor = conn.cursor()
    cursor.execute(CREATEDATABASE)
    cursor.execute(USEDATABASE)
    return conn

def infer_sql_type(value):
    if isinstance(value, int):
        return SQL_INTEGER
    elif isinstance(value, float):
        return SQL_FLOAT
    elif isinstance(value, str):
        return SQL_STRING
    else:
        return SQL_STRING

def GetTableSchema(data: Dict[str, any]) -> Dict[str, str]:
    return {k: infer_sql_type(v) for k, v in data.items()}

def CreateTable(cursor, table_name: str, schema: Dict[str, str], foreign_keys: Dict[str, str] = None, primary_key: str = "id"):
    cols = []
    for key, val in schema.items():
        col_def = f"{key} {val}"
        if key == primary_key:
            col_def += " PRIMARY KEY"
        cols.append(col_def)

    if foreign_keys:
        for fk_col, ref in foreign_keys.items():
            cols.append(f"FOREIGN KEY({fk_col}) REFERENCES {ref}")

    sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(cols)})"
    cursor.execute(sql)

    

def InsertBulkRecords(cursor: Cursor, table_name: str, rows: List[Dict[str, any]]):
    if not rows:
        return
    try:
        keys = rows[0].keys()
        placeholders = ", ".join(["%s"] * len(keys))
        sql = f"{INSERTINTO} {table_name} ({', '.join(keys)}) {VALUES} ({placeholders})"
        values = [list(row.values()) for row in rows]
        cursor.executemany(sql, values)
    except pymysql.MySQLError as e:
        print("Exception at insert_many for table '{table_name}': {e}")
        raise