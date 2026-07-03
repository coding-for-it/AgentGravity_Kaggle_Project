import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from collections import Counter

from services.audit_logger import log_agent_activity
from services.impact_service import ImpactService


class ImpactAgent:

    def __init__(self):

        self.agent_name = "Impact Agent"

        self.service = ImpactService()

    def calculate_loss(
        self,
        row,
        average_revenue
    ):

        revenue_gap = max(
            0,
            average_revenue - row["REVENUE"]
        )

        inventory_penalty = 0

        churn_penalty = 0

        if row["INVENTORY"] < 250:

            inventory_penalty = 1000

        if row["CHURN_RATE"] > 5:

            churn_penalty = 500

        return round(

            revenue_gap

            + inventory_penalty

            + churn_penalty,

            2

        )

    def calculate_severity(self, loss):

        if loss > 7000:

            return "CRITICAL"

        elif loss > 3000:

            return "HIGH"

        elif loss > 1000:

            return "MEDIUM"

        else:

            return "LOW"

    def run(self):

        print(f"\n[{self.agent_name}] Started")

        log_agent_activity(

            self.agent_name,

            "Started Impact Analysis"

        )

        incidents = self.service.get_open_incidents()

        kpis = self.service.get_all_kpis()

        average_revenue = self.service.get_average_revenue()

        existing = self.service.get_existing_impacts()

        results = []

        processed = 0

        skipped = 0

        severity_counter = Counter()

        total_loss = 0

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

            loss = self.calculate_loss(
                row,
                average_revenue
            )

            severity = self.calculate_severity(
                loss
            )

            severity_counter[severity] += 1

            total_loss += loss

            results.append({

                "incident_id": incident["INCIDENT_ID"],

                "estimated_loss": loss,

                "severity": severity

            })

            processed += 1

        self.service.save_impacts(results)

        self.service.close()

        average_loss = 0

        if processed > 0:

            average_loss = round(
                total_loss / processed,
                2
            )

        log_agent_activity(

            self.agent_name,

            f"Processed {processed} incidents"

        )

        print()

        print("=" * 60)

        print("Impact Analysis Completed")

        print("=" * 60)

        print(f"Open Incidents : {len(incidents)}")

        print(f"Processed      : {processed}")

        print(f"Skipped        : {skipped}")

        print(f"Inserted       : {len(results)}")

        print(f"Average Loss   : {average_loss}")

        print()

        print("Severity Distribution")

        print("----------------------")

        for level in [

            "CRITICAL",

            "HIGH",

            "MEDIUM",

            "LOW"

        ]:

            print(f"{level:<10}: {severity_counter[level]}")

        print("=" * 60)

        return results


if __name__ == "__main__":

    ImpactAgent().run()