from services.snowflake_connection import get_connection
from services.audit_logger import log_agent_activity
from services.kpi_analysis_service import KPIAnalysisService

import pandas as pd


class RootCauseAgent:

    def __init__(self):

        self.agent_name = "Root Cause Agent"

    def get_open_incidents(self):

        conn = get_connection()

        query = """
        SELECT *
        FROM AGENTGRAVITY.INCIDENTS.INCIDENTS
        WHERE STATUS='OPEN'
        """

        df = pd.read_sql(query, conn)

        conn.close()

        return df

    def save_root_cause(
        self,
        incident_id,
        cause_name,
        confidence
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
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
            """,
            (
                int(incident_id),
                cause_name,
                float(confidence)
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

    def investigate_incident(self, kpi_date):

        service = KPIAnalysisService()

        incident_kpi = service.get_kpi_for_date(kpi_date)

        averages = service.get_historical_averages()

        row = incident_kpi.iloc[0]

        if row["INVENTORY"] < averages["AVG_INVENTORY"] * 0.70:

            return (
                "Inventory Shortage",
                0.92
            )

        if row["CHURN_RATE"] > averages["AVG_CHURN"] * 1.50:

            return (
                "Customer Satisfaction Issue",
                0.90
            )

        if row["CUSTOMERS"] < averages["AVG_CUSTOMERS"] * 0.75:

            return (
                "Customer Demand Drop",
                0.88
            )

        return (
            "Unknown Cause",
            0.50
        )

    def run(self):

        log_agent_activity(
            self.agent_name,
            "Started Root Cause Analysis"
        )

        incidents = self.get_open_incidents()

        for _, incident in incidents.iterrows():

            cause, confidence = self.investigate_incident(
                incident["KPI_DATE"]
            )

            self.save_root_cause(
                incident["INCIDENT_ID"],
                cause,
                confidence
            )

            print(
                f"""
Incident {incident['INCIDENT_ID']}
Date: {incident['KPI_DATE']}
Cause: {cause}
Confidence: {confidence}
"""
            )

        log_agent_activity(
            self.agent_name,
            "Completed Root Cause Analysis"
        )


if __name__ == "__main__":

    RootCauseAgent().run()