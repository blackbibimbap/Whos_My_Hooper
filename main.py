##MSSQLTips.com Python
from sql_client import RDSConfigMSSQLPython
from query import QueryContainer
import mssql_python
from rich.console import Console
from rich.table import Table

mssql_python.setup_logging(output='stdout')

mssql_python_cfg = RDSConfigMSSQLPython() ##instance of config class
conn = mssql_python_cfg.get_connection() ##connection
cursor = conn.cursor() ##creates a cursor for SQL

queries = QueryContainer.get_query() ##gets query from module

console = Console() ##instantiate a console for formatting

table = Table( ##table that displays output
    title="Shot Chart Records",
    show_header=True,
    header_style="bold cyan"
)
##Add rows for each expected column from the query
table.add_column("PLAYER_NAME")
table.add_column("TEAM_NAME")
table.add_column("SHOT_TYPE")


for key, val in queries.items():
    cursor.execute(val) ##executes query
    rows = cursor.fetchall() ##gets all rows
    for player_name, team_name, shot_type in rows:
        table.add_row( ##iterate over elements
            player_name, ##populates table
            team_name,
            shot_type,
        )

console.print(table)
conn.close() ##Explicitly closes the connection