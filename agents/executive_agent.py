from services.antigravity_service import AntigravityService
from agents.impact_agent import ImpactAgent
from services.snowflake_connection import get_connection

import pandas as pd


class ExecutiveAgent:

    def __init__(self):

        self.impact_agent = ImpactAgent()

        self.antigravity = AntigravityService()

    def get_root_cause(self, incident_id):

        conn = get_connection()

        query = f"""
        SELECT CAUSE_NAME
        FROM AGENTGRAVITY.INCIDENTS.ROOT_CAUSES
        WHERE INCIDENT_ID = {incident_id}
        ORDER BY CONFIDENCE_SCORE DESC
        LIMIT 1
        """

        df = pd.read_sql(query, conn)

        conn.close()

        if df.empty:
            return "Unknown Cause"

        return df.iloc[0]["CAUSE_NAME"]

    def run(self):

        impacts = self.impact_agent.run()

        executive_reports = []

        for item in impacts:

            incident_id = item["incident_id"]

            incident_type = item["incident_type"]

            impact = item["estimated_loss"]

            root_cause = self.get_root_cause(
                incident_id
            )

            investigation = (
                self.antigravity
                .generate_investigation_plan(
                    incident_type
                )
            )

            recovery = (
                self.antigravity
                .generate_recovery_plan(
                    root_cause
                )
            )

            summary = (
                self.antigravity
                .generate_executive_summary(
                    incident_type,
                    root_cause,
                    impact
                )
            )

            executive_reports.append({

                "incident_id": incident_id,

                "incident_type": incident_type,

                "root_cause": root_cause,

                "impact": impact,

                "investigation": investigation,

                "recovery": recovery,

                "summary": summary

            })

        return executive_reports


if __name__ == "__main__":

    reports = ExecutiveAgent().run()

    for report in reports:

        print("\n" + "=" * 60)

        print(report["summary"])

        print("\nInvestigation Plan:")

        for step in report["investigation"]:

            print("-", step)

        print("\nRecovery Plan:")

        print(report["recovery"])