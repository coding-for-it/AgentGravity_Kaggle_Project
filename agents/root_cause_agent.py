from services.snowflake_connection import get_connection
from services.audit_logger import log_agent_activity
from services.kpi_analysis_service import KPIAnalysisService

import pandas as pd


class RootCauseAgent:

    def __init__(self):

        self.agent_name = "Root Cause Agent"

        self.service = KPIAnalysisService()

    def get_open_incidents(self):

        conn = get_connection()

        query = """
        SELECT *
        FROM AGENTGRAVITY.INCIDENTS.INCIDENTS
        WHERE STATUS = 'OPEN'
        ORDER BY INCIDENT_ID
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

    def investigate_incident(self, kpi_id):

        incident_kpi = self.service.get_kpi_by_id(kpi_id)

        if incident_kpi.empty:

            return (
                "Unknown Cause",
                0.50
            )

        averages = self.service.get_historical_averages()

        row = incident_kpi.iloc[0]

        if row["INVENTORY"] < averages["AVG_INVENTORY"] * 0.70:

            return (
                "Inventory Shortage",
                0.92
            )

        elif row["CHURN_RATE"] > averages["AVG_CHURN"] * 1.50:

            return (
                "Customer Satisfaction Issue",
                0.90
            )

        elif row["CUSTOMERS"] < averages["AVG_CUSTOMERS"] * 0.75:

            return (
                "Customer Demand Drop",
                0.88
            )

        elif row["REVENUE"] < averages["AVG_REVENUE"] * 0.75:

            return (
                "Revenue Decline",
                0.87
            )

        else:

            return (
                "Unknown Cause",
                0.50
            )

    def run(self):

        print(f"\n[{self.agent_name}] Started")

        log_agent_activity(
            self.agent_name,
            "Started Root Cause Analysis"
        )

        incidents = self.get_open_incidents()

        print(f"\nOpen Incidents: {len(incidents)}")

        for _, incident in incidents.iterrows():

            cause, confidence = self.investigate_incident(
                incident["KPI_ID"]
            )

            self.save_root_cause(
                incident["INCIDENT_ID"],
                cause,
                confidence
            )

            print(
                f"""
Incident ID : {incident['INCIDENT_ID']}
KPI ID      : {incident['KPI_ID']}
Type        : {incident['INCIDENT_TYPE']}
Cause       : {cause}
Confidence  : {confidence}
"""
            )

        log_agent_activity(
            self.agent_name,
            "Completed Root Cause Analysis"
        )

        print(f"\n[{self.agent_name}] Completed")


if __name__ == "__main__":

    RootCauseAgent().run()