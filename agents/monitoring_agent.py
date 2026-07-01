from services.analytics_engine import AnalyticsEngine
from services.incident_service import (
    clear_previous_workflow,
    save_incidents
)
from services.audit_logger import log_agent_activity


class MonitoringAgent:

    def __init__(self):

        self.agent_name = "Monitoring Agent"

        self.engine = AnalyticsEngine()

    def run(self):

        print(f"\n[{self.agent_name}] Started")

        log_agent_activity(
            self.agent_name,
            "Monitoring Started"
        )

        clear_previous_workflow()

        print("Loading KPI data...")
        df = self.engine.get_kpi_data()

        print("Calculating Business Health Score...")
        health_score = self.engine.calculate_business_health_score(df)

        print("Detecting Incidents...")
        incidents = self.engine.detect_incidents(df)

        print(f"Incidents Found: {len(incidents)}")

        print("Saving Incidents...")
        save_incidents(incidents)

        print("Incidents Saved.")

        log_agent_activity(
            self.agent_name,
            f"Detected {len(incidents)} incidents"
        )

        print(f"\nBusiness Health Score: {health_score}")
        print(f"Detected Incidents: {len(incidents)}")

        print(f"\n[{self.agent_name}] Completed")

        return {
            "health_score": health_score,
            "incident_count": len(incidents),
            "incidents": incidents
        }


if __name__ == "__main__":

    response = MonitoringAgent().run()

    print("\nReturned Data\n")

    print(response)