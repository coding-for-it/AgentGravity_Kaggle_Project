from services.snowflake_connection import get_connection
from services.executive_service import ExecutiveService
from services.audit_logger import log_agent_activity

import pandas as pd


class ExecutiveAgent:

    def __init__(self):

        self.agent_name = "Executive Agent"

        self.service = ExecutiveService()

    def load_data(self):

        conn = get_connection()

        query = """
        SELECT
            i.INCIDENT_ID,
            i.INCIDENT_TYPE,
            r.CAUSE_NAME,
            a.ESTIMATED_REVENUE_LOSS,
            a.BUSINESS_SEVERITY
        FROM AGENTGRAVITY.INCIDENTS.INCIDENTS i
        JOIN AGENTGRAVITY.INCIDENTS.ROOT_CAUSES r
            ON i.INCIDENT_ID = r.INCIDENT_ID
        JOIN AGENTGRAVITY.INCIDENTS.IMPACT_ANALYSIS a
            ON i.INCIDENT_ID = a.INCIDENT_ID
        """

        df = pd.read_sql(query, conn)

        conn.close()

        return df

    def generate_action(self, cause):

        actions = {
            "Inventory Shortage":
            "Increase supplier replenishment and review safety stock levels.",

            "Customer Satisfaction Issue":
            "Investigate customer complaints and improve retention campaigns.",

            "Customer Demand Drop":
            "Launch targeted promotions and review product pricing."
        }

        return actions.get(
            cause,
            "Conduct detailed investigation."
        )

    def run(self):

        log_agent_activity(
            self.agent_name,
            "Executive Analysis Started"
        )

        df = self.load_data()

        for _, row in df.iterrows():

            summary = (
                f"Incident {row['INCIDENT_ID']} "
                f"was caused by {row['CAUSE_NAME']}. "
                f"Estimated revenue loss is "
                f"{row['ESTIMATED_REVENUE_LOSS']}."
            )

            action = self.generate_action(
                row["CAUSE_NAME"]
            )

            priority = row["BUSINESS_SEVERITY"]

            self.service.save_report(
                row["INCIDENT_ID"],
                summary,
                action,
                priority
            )

            print("\n" + "=" * 50)
            print(summary)
            print(action)
            print("Priority:", priority)

        log_agent_activity(
            self.agent_name,
            "Executive Analysis Completed"
        )


if __name__ == "__main__":
    ExecutiveAgent().run()