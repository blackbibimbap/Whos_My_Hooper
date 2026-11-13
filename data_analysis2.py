import pandas as pd
from sql_client_mac import get_connection

player = "Dyson Daniels"

conn = get_connection()

query = """
SELECT PLAYER_NAME, EVENT_TYPE, LOC_X, LOC_Y
FROM dbo.shotchartdetail
WHERE PLAYER_NAME = ?
"""

df = pd.read_sql_query(query, conn, params=[player])
conn.close()

print(df.head())
print(df["EVENT_TYPE"].value_counts())

made = df[df["EVENT_TYPE"] == "Made Shot"]
missed = df[df["EVENT_TYPE"] == "Missed Shot"]

print("Made shots:", len(made))
print("Missed shots:", len(missed))
print("Field Goal %:", round(len(made) / len(df) * 100, 1))