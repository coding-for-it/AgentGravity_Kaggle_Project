import pandas as pd

from services.snowflake_connection import get_connection


class ImpactService:

    def __init__(self):

        self.conn = get_connection()

    def get_open_incidents(self):

        query = """
        SELECT
            INCIDENT_ID,
            KPI_ID,
            INCIDENT_TYPE
        FROM AGENTGRAVITY.INCIDENTS.INCIDENTS
        WHERE STATUS='OPEN'
        ORDER BY INCIDENT_ID
        """

        return pd.read_sql(query, self.conn)

    def get_all_kpis(self):

        query = """
        SELECT
            KPI_ID,
            REVENUE,
            INVENTORY,
            CHURN_RATE
        FROM AGENTGRAVITY.BUSINESS.KPI_METRICS
        """

        return pd.read_sql(query, self.conn)

    def get_average_revenue(self):

        query = """
        SELECT AVG(REVENUE) AS AVG_REVENUE
        FROM AGENTGRAVITY.BUSINESS.KPI_METRICS
        """

        df = pd.read_sql(query, self.conn)

        return float(df.iloc[0]["AVG_REVENUE"])

    def get_existing_impacts(self):

        query = """
        SELECT INCIDENT_ID
        FROM AGENTGRAVITY.INCIDENTS.IMPACT_ANALYSIS
        """

        df = pd.read_sql(query, self.conn)

        return set(df["INCIDENT_ID"])

    def save_impacts(self, results):

        if len(results) == 0:

            print("No new impact records.")

            return

        cursor = self.conn.cursor()

        query = """
        INSERT INTO
        AGENTGRAVITY.INCIDENTS.IMPACT_ANALYSIS
        (
            INCIDENT_ID,
            ESTIMATED_REVENUE_LOSS,
            BUSINESS_SEVERITY,
            CREATED_AT
        )
        VALUES
        (
            %s,
            %s,
            %s,
            CURRENT_TIMESTAMP()
        )
        """

        values = [

            (
                row["incident_id"],
                row["estimated_loss"],
                row["severity"]
            )

            for row in results

        ]

        cursor.executemany(query, values)

        self.conn.commit()

        cursor.close()

    def close(self):

        self.conn.close()