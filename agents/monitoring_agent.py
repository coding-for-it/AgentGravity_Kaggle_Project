from services.analytics_engine import AnalyticsEngine
from services.audit_logger import log_agent_activity


class MonitoringAgent:

    def __init__(self):

        self.engine = AnalyticsEngine()
        self.agent_name = "Monitoring Agent"

    def run(self):

        print(f"\n[{self.agent_name}] Started")

        # Log start
        log_agent_activity(
            self.agent_name,
            "Started KPI Monitoring"
        )

        df = self.engine.get_kpi_data()

        health_score = self.engine.calculate_business_health_score(df)

        incidents = self.engine.detect_incidents(df)

        result = {
            "health_score": health_score,
            "incident_count": len(incidents),
            "incidents": incidents
        }

        print("\nBusiness Health Score:", health_score)

        print("\nIncidents Found:", len(incidents))

        # Log completion
        log_agent_activity(
            self.agent_name,
            f"Detected {len(incidents)} incidents"
        )

        print("\nMonitoring completed successfully.")

        return result


if __name__ == "__main__":

    agent = MonitoringAgent()

    response = agent.run()

    print("\nResult")

    print(response)