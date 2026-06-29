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

        elif revenue_loss > 3000:
            return "HIGH"

        elif revenue_loss > 1000:
            return "MEDIUM"

        else:
            return "LOW"

    def run(self):

        print(f"\n[{self.agent_name}] Started")

        log_agent_activity(
            self.agent_name,
            "Impact Analysis Started"
        )

        avg_revenue = self.service.get_historical_average_revenue()

        incidents = self.get_incidents()

        impact_results = []

        for _, incident in incidents.iterrows():

            actual_revenue = self.service.get_revenue_for_date(
                incident["KPI_DATE"]
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

            result = {
                "incident_id": incident["INCIDENT_ID"],
                "incident_type": incident["INCIDENT_TYPE"],
                "estimated_loss": revenue_loss,
                "severity": severity
            }

            impact_results.append(result)

            print(
                f"""
Incident: {incident['INCIDENT_ID']}
Type: {incident['INCIDENT_TYPE']}
Revenue Loss: {revenue_loss}
Severity: {severity}
"""
            )

        log_agent_activity(
            self.agent_name,
            "Impact Analysis Completed"
        )

        print(f"\n[{self.agent_name}] Completed")

        return impact_results


if __name__ == "__main__":

    reports = ImpactAgent().run()

    print("\n===== IMPACT REPORT =====")

    for report in reports:
        print(report)