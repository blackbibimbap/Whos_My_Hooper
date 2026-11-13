import pandas as pd
from sql_client_mac import get_connection

conn = get_connection()

query = """
SELECT TOP 100 PLAYER_NAME, TEAM_NAME, SHOT_TYPE, LOC_X, LOC_Y
FROM dbo.shotchartdetail
WHERE PLAYER_NAME = 'Dyson Daniels'
"""

df = pd.read_sql_query(query, conn)

print(df.head())
print(df.columns.tolist())

conn.close()