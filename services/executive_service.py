import traceback

from mcp.snowflake_mcp import SnowflakeMCP


class ExecutiveService:

    def __init__(self):

        self.mcp = SnowflakeMCP()

    # ----------------------------------------------------

    def get_business_summary(self):

        print("\nExecuting Business Summary Query...")

        query = """
        SELECT
            i.INCIDENT_TYPE,
            rc.CAUSE_NAME,
            ia.BUSINESS_SEVERITY,
            ia.ESTIMATED_REVENUE_LOSS
        FROM AGENTGRAVITY.INCIDENTS.INCIDENTS i

        INNER JOIN AGENTGRAVITY.INCIDENTS.ROOT_CAUSES rc
        ON i.INCIDENT_ID = rc.INCIDENT_ID

        INNER JOIN AGENTGRAVITY.INCIDENTS.IMPACT_ANALYSIS ia
        ON i.INCIDENT_ID = ia.INCIDENT_ID
        """

        df = self.mcp.execute_query(query)

        print(f"Business Summary Rows Returned: {len(df)}")

        return df

    # ----------------------------------------------------

    def get_master_incident_id(self):

        query = """
        SELECT MIN(INCIDENT_ID)
        FROM AGENTGRAVITY.INCIDENTS.INCIDENTS
        """

        incident_id = self.mcp.fetch_scalar(query)

        if incident_id is None:

            raise Exception("No Incident ID found.")

        print(f"Master Incident ID : {incident_id}")

        return int(incident_id)

    # ----------------------------------------------------

    def save_executive_report(

        self,

        summary,

        recommended_action,

        priority

    ):

        try:

            if summary is None or str(summary).strip() == "":

                raise Exception("Executive Summary is empty.")

            self.mcp.execute_dml("""

                DELETE FROM AGENTGRAVITY.INCIDENTS.EXECUTIVE_REPORTS

            """)

            incident_id = self.get_master_incident_id()

            query = """
            INSERT INTO AGENTGRAVITY.INCIDENTS.EXECUTIVE_REPORTS
            (
                INCIDENT_ID,
                EXECUTIVE_SUMMARY,
                RECOMMENDED_ACTION,
                BUSINESS_PRIORITY,
                CREATED_AT
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                CURRENT_TIMESTAMP()
            )
            """

            values = (

                incident_id,

                summary,

                recommended_action,

                priority

            )

            self.mcp.execute_dml(

                query,

                values

            )

            print("Executive Report saved successfully.")

        except Exception:

            traceback.print_exc()

            raise

    # ----------------------------------------------------

    def close(self):

        pass