
import os
import pyodbc
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")


def get_connection():
    connection_string = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={os.getenv('DB_SERVER')};"
        f"DATABASE={os.getenv('DB_DATABASE')};"
        f"UID={os.getenv('DB_USERNAME')};"
        f"PWD={os.getenv('DB_PASSWORD')};"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )

    return pyodbc.connect(connection_string, timeout=10)


if __name__ == "__main__":
    print("Starting SQL connection test...")

    conn = get_connection()
    print("Connected successfully!")

    cursor = conn.cursor()
    cursor.execute("""
        SELECT TOP 10 PLAYER_NAME, TEAM_NAME, SHOT_TYPE
        FROM dbo.shotchartdetail
    """)

    rows = cursor.fetchall()
    print(f"Rows retrieved: {len(rows)}")

    for row in rows:
        print(row)

    conn.close()