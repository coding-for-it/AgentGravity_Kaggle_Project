from services.snowflake_connection import get_connection
import pandas as pd


class ImpactService:

    def get_historical_average_revenue(self):

        conn = get_connection()

        query = """
        SELECT AVG(REVENUE) AS AVG_REVENUE
        FROM AGENTGRAVITY.BUSINESS.KPI_METRICS
        """

        df = pd.read_sql(query, conn)

        conn.close()

        return float(df.iloc[0]["AVG_REVENUE"])

    def get_revenue_for_date(self, kpi_date):

        conn = get_connection()

        query = f"""
        SELECT REVENUE
        FROM AGENTGRAVITY.BUSINESS.KPI_METRICS
        WHERE KPI_DATE = '{kpi_date}'
        """

        df = pd.read_sql(query, conn)

        conn.close()

        return float(df.iloc[0]["REVENUE"])

    def save_impact_analysis(
        self,
        incident_id,
        revenue_loss,
        severity
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
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
            """,
            (
                incident_id,
                revenue_loss,
                severity
            )
        )

        conn.commit()

        cursor.close()
        conn.close()