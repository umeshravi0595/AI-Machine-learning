from sqlalchemy import create_engine
import pandas as pd

# Connection details
server_name = "LAPTOP-BGELBRCQ"
database_name = "llm"

# Create the engine
connection_string = f"mssql+pyodbc://@{server_name}/{database_name}?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(connection_string)

# Query a table
query = "SELECT  * FROM dbo.student"  # Replace 'your_table_name' with the actual table name

# Fetch data into a DataFrame
with engine.connect() as conn:
    result = pd.read_sql(query, conn)

print(result)
