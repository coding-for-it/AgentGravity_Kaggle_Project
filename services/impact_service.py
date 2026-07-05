from mcp.snowflake_mcp import SnowflakeMCP


class ImpactService:

    def __init__(self):

        self.mcp = SnowflakeMCP()

    # ----------------------------------------------------

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

        return self.mcp.execute_query(query)

    # ----------------------------------------------------

    def get_all_kpis(self):

        query = """
        SELECT
            KPI_ID,
            REVENUE,
            INVENTORY,
            CHURN_RATE
        FROM AGENTGRAVITY.BUSINESS.KPI_METRICS
        """

        return self.mcp.execute_query(query)

    # ----------------------------------------------------

    def get_average_revenue(self):

        query = """
        SELECT
            AVG(REVENUE) AS AVG_REVENUE
        FROM AGENTGRAVITY.BUSINESS.KPI_METRICS
        """

        df = self.mcp.execute_query(query)

        return float(df.iloc[0]["AVG_REVENUE"])

    # ----------------------------------------------------

    def get_existing_impacts(self):

        query = """
        SELECT INCIDENT_ID
        FROM AGENTGRAVITY.INCIDENTS.IMPACT_ANALYSIS
        """

        df = self.mcp.execute_query(query)

        if df.empty:

            return set()

        return set(df["INCIDENT_ID"])

    # ----------------------------------------------------

    def save_impacts(self, results):
        if len(results) == 0:
            print("No new impact records.")
            return

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

        self.mcp.execute_many(
            query,
            values
        )

        print(f"Saved {len(values)} impact records.")
    # ----------------------------------------------------

    def close(self):

        pass