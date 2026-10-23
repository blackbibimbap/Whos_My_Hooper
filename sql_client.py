##https://www.mssqltips.com/sqlservertip/11606/getting-started-with-mssql-python/ refer to this link
"""
02: MSSQLTips.com General database connection configuration class
"""
import os
from attrs import define, field, validators
import mssql_python
from mssql_python import Connection
from dotenv import load_dotenv
 
load_dotenv()


@define
class RDSConfigMSSQLPython:
    DB_SERVER: str = field(
        factory=lambda: os.getenv("DB_SERVER", "ZacSanJuan\\ZSQL"), ##MUST BE SAME AS ENV FILE
        validator=validators.instance_of(str)
    )
    DB_DATABASE: str = field(
        factory=lambda: os.getenv("DB_DATABASE", "NBA"), ##MUST BE SAME AS ENV FILE
        validator=validators.instance_of(str)
    )
    DB_USERNAME: str = field(
        factory=lambda: os.getenv("DB_USERNAME", "NBAdmin"), ##MUST BE SAME AS ENV FILE
        validator=validators.instance_of(str)
    )
    DB_PASSWORD: str = field(
        factory=lambda: os.getenv("DB_PASSWORD", "basketball"), ##MUST BE SAME AS ENV FILE
        validator=validators.instance_of(str)
    )
 
    def get_connection(self) -> Connection: ##Creates connection object. Requires a connection string
        connection_str = ""
        if not self.DB_USERNAME or not self.DB_PASSWORD:
            # Windows Authentication
            connection_str = f"Server={self.DB_SERVER};\
                Database={self.DB_DATABASE};\
                Trusted_Connection=yes;\
                TrustServerCertificate=yes;"
        else:
            # SQL Server Authentication
            connection_str = f"Server={self.DB_SERVER};\
                Database={self.DB_DATABASE};\
                UID={self.DB_USERNAME};\
                PWD={self.DB_PASSWORD};\
                TrustServerCertificate=yes;"

        return mssql_python.connect(connection_str)

##This checks the output and sees if it works
if __name__ == "__main__":
    db_cfg_mssqlpython = RDSConfigMSSQLPython()
    engine = db_cfg_mssqlpython.get_connection()
    print(engine) ##If it shows a connection object, that means it successfully connected
##This entire file connects the file to the SQL database. 
