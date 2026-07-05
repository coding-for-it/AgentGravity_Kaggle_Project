import pandas as pd

from services.snowflake_connection import get_connection


class SnowflakeMCP:

    def __init__(self):

        self.conn = get_connection()

    # ----------------------------------------------------
    # SELECT Queries
    # ----------------------------------------------------

    def execute_query(self, query):

        return pd.read_sql(query, self.conn)

    # ----------------------------------------------------
    # Single INSERT / UPDATE / DELETE
    # ----------------------------------------------------

    def execute_dml(
        self,
        query,
        values=None
    ):

        cursor = self.conn.cursor()

        try:

            if values is not None:

                cursor.execute(query, values)

            else:

                cursor.execute(query)

            self.conn.commit()

        finally:

            cursor.close()

    # ----------------------------------------------------
    # BULK INSERT
    # ----------------------------------------------------

    def execute_many(
        self,
        query,
        values
    ):

        if len(values) == 0:

            return

        cursor = self.conn.cursor()

        try:

            cursor.executemany(query, values)

            self.conn.commit()

        finally:

            cursor.close()

    # ----------------------------------------------------
    # Fetch Single Value
    # ----------------------------------------------------

    def fetch_scalar(self, query):

        cursor = self.conn.cursor()

        try:

            cursor.execute(query)

            row = cursor.fetchone()

            if row:

                return row[0]

            return None

        finally:

            cursor.close()

    # ----------------------------------------------------
    # Table Count
    # ----------------------------------------------------

    def table_count(self, table_name):

        query = f"""
        SELECT COUNT(*)
        FROM {table_name}
        """

        return self.fetch_scalar(query)

    # ----------------------------------------------------
    # Check Table Exists
    # ----------------------------------------------------

    def table_exists(self, table_name):

        cursor = self.conn.cursor()

        try:

            cursor.execute(
                f"""
                SHOW TABLES LIKE '{table_name.split('.')[-1]}'
                """
            )

            return cursor.fetchone() is not None

        finally:

            cursor.close()

    # ----------------------------------------------------
    # Close Connection
    # ----------------------------------------------------

    def close(self):

        if self.conn:

            self.conn.close()

            self.conn = None