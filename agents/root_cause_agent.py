import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from services.root_cause_service import RootCauseService
from services.audit_logger import log_agent_activity
from services.logger import get_logger


class RootCauseAgent:

    def __init__(self):

        self.agent_name = "Root Cause Agent"

        self.logger = get_logger("rootcause")

        self.service = RootCauseService()

    def identify_root_cause(
        self,
        row,
        averages
    ):

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

        self.logger.info("=" * 60)
        self.logger.info("Root Cause Agent Started")

        log_agent_activity(
            self.agent_name,
            "Started Root Cause Analysis"
        )

        self.logger.info("Loading open incidents")
        incidents = self.service.get_open_incidents()

        self.logger.info(f"Loaded {len(incidents)} open incidents")

        self.logger.info("Loading KPI dataset")
        kpis = self.service.get_all_kpis()

        self.logger.info(f"Loaded {len(kpis)} KPI records")

        averages = self.service.get_historical_averages()

        existing = self.service.get_existing_root_causes()

        results = []

        processed = 0

        skipped = 0

        for _, incident in incidents.iterrows():

            if incident["INCIDENT_ID"] in existing:

                skipped += 1

                continue

            kpi = kpis.loc[
                kpis["KPI_ID"] == incident["KPI_ID"]
            ]

            if kpi.empty:
                continue

            row = kpi.iloc[0]

            cause, confidence = self.identify_root_cause(
                row,
                averages
            )

            results.append({

                "incident_id": incident["INCIDENT_ID"],

                "cause": cause,

                "confidence": confidence

            })

            processed += 1

        self.logger.info(
            f"Processed {processed} incidents"
        )

        self.service.save_root_causes(results)

        self.logger.info(
            f"Inserted {len(results)} root causes into Snowflake"
        )

        self.service.close()

        log_agent_activity(

            self.agent_name,

            f"Processed {processed} incidents"

        )

        print()

        print("=" * 60)

        print("Root Cause Analysis Completed")

        print("=" * 60)

        print(f"Open Incidents      : {len(incidents)}")

        print(f"Processed           : {processed}")

        print(f"Skipped             : {skipped}")

        print(f"Inserted            : {len(results)}")

        print("=" * 60)

        print()

        self.logger.info("Root Cause Agent Completed")
        self.logger.info("=" * 60)

        return results


if __name__ == "__main__":

    RootCauseAgent().run()