import pandas as pd

from services.snowflake_connection import get_connection


class SnowflakeMCP:

    def execute_query(self, query):

        conn = get_connection()

        df = pd.read_sql(
            query,
            conn
        )

        conn.close()

        return df

    def execute_dml(
        self,
        query,
        values=None
    ):

        conn = get_connection()

        cursor = conn.cursor()

        if values:

            cursor.execute(
                query,
                values
            )

        else:

            cursor.execute(query)

        conn.commit()

        cursor.close()

        conn.close()

    def fetch_scalar(self, query):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(query)

        value = cursor.fetchone()[0]

        cursor.close()

        conn.close()

        return value

    def table_count(self, table_name):

        query = f"""
        SELECT COUNT(*)
        FROM {table_name}
        """

        return self.fetch_scalar(query)

    def table_exists(self, table_name):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            f"""
            SHOW TABLES LIKE '{table_name.split('.')[-1]}'
            """
        )

        exists = cursor.fetchone() is not None

        cursor.close()

        conn.close()

        return exists