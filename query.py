##https://www.mssqltips.com/sqlservertip/11606/getting-started-with-mssql-python/ refer to this link
from attrs import define
from typing import ClassVar

@define
class QueryContainer: ##Query class
    SHOT_CHART_DETAIL: ClassVar[str] = """
            SELECT PLAYER_NAME, TEAM_NAME, SHOT_TYPE FROM dbo.shotchartdetail
        """ ##Put query here

    @classmethod ##Fetches the query
    def get_query(cls, key: str | None = None) -> dict[str, str]:
        """Retrieves a query or all queries.
        Args:
            key (str | None, optional): query name. Defaults to None.
        Raises:
            KeyError: error if the query does not exist.
        Returns:
            str | dict[str, str]: query definition or dictionary of all queries.
        """
        queries = {
            'Shot Chart Record': cls.SHOT_CHART_DETAIL,
        }

        if key is None:
            return queries

        if key not in queries:
            raise KeyError(f"Query '{key}' not found. Available keys: {list(queries.keys())}")

        return {key: queries[key]}