import os
from dotenv import load_dotenv
import snowflake.connector

load_dotenv()

def get_connection():

    account = os.getenv("SNOWFLAKE_ACCOUNT")
    user = os.getenv("SNOWFLAKE_USER")

    print(f"ACCOUNT: {account}")
    print(f"USER: {user}")

    conn = snowflake.connector.connect(
        account=account,
        user=user,
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA")
    )

    return conn