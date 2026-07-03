import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from services.analytics_engine import AnalyticsEngine
from services.incident_service import (
    clear_previous_workflow,
    save_incidents
)
from services.audit_logger import log_agent_activity
from services.logger import get_logger


class MonitoringAgent:

    def __init__(self):

        self.agent_name = "Monitoring Agent"

        self.logger = get_logger("monitoring")

        self.engine = AnalyticsEngine()

    def run(self):

        print(f"\n[{self.agent_name}] Started")

        self.logger.info("=" * 60)
        self.logger.info("Monitoring Agent Started")

        log_agent_activity(
            self.agent_name,
            "Monitoring Started"
        )

        print("Clearing previous workflow data...")
        clear_previous_workflow()
        print("Workflow tables cleared.")

        self.logger.info("Previous workflow data cleared")

        print("\nLoading KPI data...")
        self.logger.info("Loading KPI data from Snowflake")

        df = self.engine.get_kpi_data()

        self.logger.info(f"Loaded {len(df)} KPI records")

        print("Calculating Business Health Score...")
        health_score = self.engine.calculate_business_health_score(df)

        self.logger.info(
            f"Business Health Score: {health_score}"
        )

        print("Detecting Incidents...")

        incidents = self.engine.detect_incidents(df)

        self.logger.info(
            f"Detected {len(incidents)} incidents"
        )

        print(f"Incidents Found: {len(incidents)}")

        print("Saving Incidents...")

        save_incidents(incidents)

        self.logger.info(
            f"Saved {len(incidents)} incidents to Snowflake"
        )

        print("Incidents Saved.")

        log_agent_activity(
            self.agent_name,
            f"Detected {len(incidents)} incidents"
        )

        print(f"\nBusiness Health Score: {health_score}")
        print(f"Detected Incidents: {len(incidents)}")

        print(f"\n[{self.agent_name}] Completed")

        self.logger.info("Monitoring Agent Completed")
        self.logger.info("=" * 60)

        return {
            "health_score": health_score,
            "incident_count": len(incidents),
            "incidents": incidents
        }


if __name__ == "__main__":

    response = MonitoringAgent().run()

    print("\nReturned Data\n")

    print(response)