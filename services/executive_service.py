from services.snowflake_connection import get_connection


class ExecutiveService:

    def save_report(
        self,
        incident_id,
        summary,
        action,
        priority
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO
            AGENTGRAVITY.INCIDENTS.EXECUTIVE_REPORTS
            (
                INCIDENT_ID,
                EXECUTIVE_SUMMARY,
                RECOMMENDED_ACTION,
                PRIORITY,
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
            """,
            (
                incident_id,
                summary,
                action,
                priority
            )
        )

        conn.commit()

        cursor.close()
        conn.close()