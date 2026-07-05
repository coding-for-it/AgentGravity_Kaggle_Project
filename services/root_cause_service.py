from mcp.snowflake_mcp import SnowflakeMCP


class RootCauseService:

    def __init__(self):

        self.mcp = SnowflakeMCP()

    # --------------------------------------------------

    def get_open_incidents(self):

        query = """
        SELECT
            INCIDENT_ID,
            KPI_ID,
            INCIDENT_TYPE,
            SEVERITY
        FROM AGENTGRAVITY.INCIDENTS.INCIDENTS
        WHERE STATUS='OPEN'
        ORDER BY INCIDENT_ID
        """

        return self.mcp.execute_query(query)

    # --------------------------------------------------

    def get_all_kpis(self):

        query = """
        SELECT *
        FROM AGENTGRAVITY.BUSINESS.KPI_METRICS
        """

        return self.mcp.execute_query(query)

    # --------------------------------------------------

    def get_historical_averages(self):

        query = """
        SELECT
            AVG(REVENUE) AS AVG_REVENUE,
            AVG(ORDERS) AS AVG_ORDERS,
            AVG(CUSTOMERS) AS AVG_CUSTOMERS,
            AVG(INVENTORY) AS AVG_INVENTORY,
            AVG(CHURN_RATE) AS AVG_CHURN
        FROM AGENTGRAVITY.BUSINESS.KPI_METRICS
        """

        return self.mcp.execute_query(query).iloc[0]

    # --------------------------------------------------

    def get_existing_root_causes(self):

        query = """
        SELECT INCIDENT_ID
        FROM AGENTGRAVITY.INCIDENTS.ROOT_CAUSES
        """

        df = self.mcp.execute_query(query)

        if df.empty:

            return set()

        return set(df["INCIDENT_ID"])

    # --------------------------------------------------

    def save_root_causes(self, results):
        if len(results) == 0:
            print("No new root causes to insert.")
            
            return

        query = """
        INSERT INTO
        AGENTGRAVITY.INCIDENTS.ROOT_CAUSES
        (
        INCIDENT_ID,
        CAUSE_NAME,
        CONFIDENCE_SCORE
        )
        VALUES
        (
        %s,
        %s,
        %s
        )
        """

        values = [
            (
                row["incident_id"],
                row["cause"],
                row["confidence"]
            )

            for row in results

        ]

        self.mcp.execute_many(
            query,
            values
        )

        print(f"Saved {len(values)} root causes.")
    # --------------------------------------------------

    def close(self):

        self.mcp.close()