import pandas as pd
from services.snowflake_connection import get_connection


class KPIAnalysisService:

    def get_kpi_for_date(self, kpi_date):

        conn = get_connection()

        query = f"""
        SELECT *
        FROM AGENTGRAVITY.BUSINESS.KPI_METRICS
        WHERE KPI_DATE = '{kpi_date}'
        """

        df = pd.read_sql(query, conn)

        conn.close()

        return df

    def get_historical_averages(self):

        conn = get_connection()

        query = """
        SELECT
            AVG(REVENUE) AS AVG_REVENUE,
            AVG(ORDERS) AS AVG_ORDERS,
            AVG(CUSTOMERS) AS AVG_CUSTOMERS,
            AVG(INVENTORY) AS AVG_INVENTORY,
            AVG(CHURN_RATE) AS AVG_CHURN
        FROM AGENTGRAVITY.BUSINESS.KPI_METRICS
        """

        df = pd.read_sql(query, conn)

        conn.close()

        return df.iloc[0]