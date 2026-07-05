from mcp.snowflake_mcp import SnowflakeMCP


class RecoveryService:

    def __init__(self):

        self.mcp = SnowflakeMCP()

    # ----------------------------------------------------

    def get_executive_report(self):

        query = """
        SELECT
            EXECUTIVE_SUMMARY,
            BUSINESS_PRIORITY
        FROM AGENTGRAVITY.INCIDENTS.EXECUTIVE_REPORTS
        ORDER BY CREATED_AT DESC
        LIMIT 1
        """

        return self.mcp.execute_query(query)

    # ----------------------------------------------------

    def save_recovery_plan(

        self,

        executive_summary,

        immediate_actions,

        short_term_actions,

        long_term_actions,

        expected_outcome,

        success_metrics,

        risk_level

    ):

        self.mcp.execute_dml("""

        DELETE FROM AGENTGRAVITY.INCIDENTS.RECOVERY_PLAN

        """)

        query = """
        INSERT INTO
        AGENTGRAVITY.INCIDENTS.RECOVERY_PLAN
        (
            EXECUTIVE_SUMMARY,
            IMMEDIATE_ACTIONS,
            SHORT_TERM_ACTIONS,
            LONG_TERM_ACTIONS,
            EXPECTED_BUSINESS_OUTCOME,
            SUCCESS_METRICS,
            RISK_LEVEL
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        """

        values = (

            executive_summary,

            immediate_actions,

            short_term_actions,

            long_term_actions,

            expected_outcome,

            success_metrics,

            risk_level

        )

        self.mcp.execute_dml(

            query,

            values

        )

    # ----------------------------------------------------

    def close(self):

        pass