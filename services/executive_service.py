import traceback
import pandas as pd

from services.snowflake_connection import get_connection


class ExecutiveService:

    def __init__(self):

        self.conn = get_connection()

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

        df = pd.read_sql(query, self.conn)

        print(f"Business Summary Rows Returned: {len(df)}")

        return df

    def get_master_incident_id(self):

        cursor = self.conn.cursor()

        try:

            cursor.execute("""
                SELECT MIN(INCIDENT_ID)
                FROM AGENTGRAVITY.INCIDENTS.INCIDENTS
            """)

            result = cursor.fetchone()

            if result is None or result[0] is None:
                raise Exception("No Incident ID found in INCIDENTS table.")

            incident_id = int(result[0])

            print(f"Master Incident ID: {incident_id}")

            return incident_id

        finally:
            cursor.close()

    def save_executive_report(
        self,
        summary,
        recommended_action,
        priority
    ):

        cursor = None

        try:

            print("\nEntering save_executive_report()")

            if summary is None or str(summary).strip() == "":
                raise Exception("Executive Summary is empty.")

            cursor = self.conn.cursor()

            incident_id = self.get_master_incident_id()

            print(f"Incident ID : {incident_id}")
            print(f"Priority    : {priority}")
            print(f"Summary Length : {len(summary)}")

            print("\nDeleting existing Executive Reports...")

            cursor.execute("""
                DELETE FROM AGENTGRAVITY.INCIDENTS.EXECUTIVE_REPORTS
            """)

            print("Delete completed.")

            print("\nExecuting INSERT...")

            cursor.execute(
                """
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
                """,
                (
                    incident_id,
                    summary,
                    recommended_action,
                    priority
                )
            )

            print("INSERT executed successfully.")

            self.conn.commit()

            print("Commit successful.")
            print("Executive Report saved successfully.")

        except Exception as e:

            print("\n==============================")
            print("SAVE EXECUTIVE REPORT FAILED")
            print("==============================")
            print(f"Error Type : {type(e).__name__}")
            print(f"Error      : {e}")
            traceback.print_exc()

            raise

        finally:

            if cursor is not None:
                cursor.close()

    def close(self):

        if self.conn:
            self.conn.close()