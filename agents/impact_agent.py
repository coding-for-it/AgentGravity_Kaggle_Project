from services.snowflake_connection import get_connection
from services.impact_service import ImpactService
from services.audit_logger import log_agent_activity

import pandas as pd


class ImpactAgent:

    def __init__(self):

        self.agent_name = "Impact Agent"

        self.service = ImpactService()

    def get_incidents(self):

        conn = get_connection()

        query = """
        SELECT *
        FROM AGENTGRAVITY.INCIDENTS.INCIDENTS
        """

        df = pd.read_sql(query, conn)

        conn.close()

        return df

    def calculate_severity(self, revenue_loss):

        if revenue_loss > 5000:
            return "CRITICAL"

        if revenue_loss > 3000:
            return "HIGH"

        if revenue_loss > 1000:
            return "MEDIUM"

        return "LOW"

    def run(self):

        log_agent_activity(
            self.agent_name,
            "Impact Analysis Started"
        )

        avg_revenue = (
            self.service.get_historical_average_revenue()
        )

        incidents = self.get_incidents()

        for _, incident in incidents.iterrows():

            actual_revenue = (
                self.service.get_revenue_for_date(
                    incident["KPI_DATE"]
                )
            )

            revenue_loss = max(
                0,
                avg_revenue - actual_revenue
            )

            severity = self.calculate_severity(
                revenue_loss
            )

            self.service.save_impact_analysis(
                incident["INCIDENT_ID"],
                revenue_loss,
                severity
            )

            print(
                f"""
Incident: {incident['INCIDENT_ID']}
Revenue Loss: {revenue_loss}
Severity: {severity}
"""
            )

        log_agent_activity(
            self.agent_name,
            "Impact Analysis Completed"
        )


if __name__ == "__main__":

    ImpactAgent().run()