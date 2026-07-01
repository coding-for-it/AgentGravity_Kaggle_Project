import pandas as pd

from services.snowflake_connection import get_connection


class RecoveryService:

    def __init__(self):

        self.conn = get_connection()

    def get_executive_report(self):

        query = """
        SELECT
            EXECUTIVE_SUMMARY,
            BUSINESS_PRIORITY
        FROM AGENTGRAVITY.INCIDENTS.EXECUTIVE_REPORTS
        ORDER BY CREATED_AT DESC
        LIMIT 1
        """

        return pd.read_sql(query, self.conn)

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

        cursor = self.conn.cursor()

        cursor.execute("""
        DELETE FROM AGENTGRAVITY.INCIDENTS.RECOVERY_PLAN
        """)

        cursor.execute(
            """
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
            """,
            (
                executive_summary,
                immediate_actions,
                short_term_actions,
                long_term_actions,
                expected_outcome,
                success_metrics,
                risk_level
            )
        )

        self.conn.commit()

        cursor.close()

    def close(self):

        self.conn.close()