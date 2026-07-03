import os
import sys
import traceback

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from services.executive_service import ExecutiveService
from services.antigravity_service import AntigravityService
from services.audit_logger import log_agent_activity


class ExecutiveAgent:

    def __init__(self):

        self.agent_name = "Executive Agent"

        self.service = ExecutiveService()

        self.ai = AntigravityService()

    def build_business_summary(self, df):

        total_incidents = len(df)

        incident_counts = (
            df["INCIDENT_TYPE"]
            .value_counts()
            .to_dict()
        )

        root_causes = (
            df["CAUSE_NAME"]
            .value_counts()
            .to_dict()
        )

        severity_counts = (
            df["BUSINESS_SEVERITY"]
            .value_counts()
            .to_dict()
        )

        avg_loss = round(
            df["ESTIMATED_REVENUE_LOSS"].mean(),
            2
        )

        total_loss = round(
            df["ESTIMATED_REVENUE_LOSS"].sum(),
            2
        )

        max_loss = round(
            df["ESTIMATED_REVENUE_LOSS"].max(),
            2
        )

        summary = f"""
BUSINESS SUMMARY

Total Incidents:
{total_incidents}

Incident Distribution:
{incident_counts}

Root Cause Distribution:
{root_causes}

Business Severity:
{severity_counts}

Average Revenue Loss:
${avg_loss}

Maximum Revenue Loss:
${max_loss}

Total Estimated Revenue Loss:
${total_loss}
"""

        return summary

    def determine_priority(self, df):

        critical = (
            df["BUSINESS_SEVERITY"] == "CRITICAL"
        ).sum()

        if critical >= 100:
            return "CRITICAL"

        if critical >= 50:
            return "HIGH"

        return "MEDIUM"

    def run(self):

        try:

            print("\n" + "=" * 70)
            print("EXECUTIVE AGENT STARTED")
            print("=" * 70)

            log_agent_activity(
                self.agent_name,
                "Executive Report Started"
            )

            print("\nFetching business summary from Snowflake...")

            df = self.service.get_business_summary()

            print(f"Rows fetched: {len(df)}")

            if df.empty:
                print("\nNo business data found.")
                self.service.close()
                return

            print("\nPreview:")
            print(df.head())

            business_summary = self.build_business_summary(df)

            print("\nSending Business Summary to Gemini...")

            try:

                executive_briefing = self.ai.generate_executive_briefing(
                    business_summary
                )

            except Exception:

                print("\nGemini API failed.\n")
                traceback.print_exc()
                self.service.close()
                return

            if executive_briefing is None:

                print("\nERROR: Gemini returned None.")
                self.service.close()
                return

            executive_briefing = str(executive_briefing).strip()

            if executive_briefing == "":

                print("\nERROR: Gemini returned an empty response.")
                self.service.close()
                return

            print("\nGemini Response Received Successfully.")
            print("\n" + "=" * 70)
            print("EXECUTIVE BRIEFING")
            print("=" * 70)
            print(executive_briefing)
            print("=" * 70)

            priority = self.determine_priority(df)

            print(f"\nBusiness Priority : {priority}")

            incident_id = self.service.get_master_incident_id()

            print(f"Master Incident ID : {incident_id}")

            print("\nSaving Executive Report to Snowflake...")

            try:

                self.service.save_executive_report(
                    executive_briefing,
                    "Refer Executive Summary",
                    priority
                )

                print("\nExecutive Report saved successfully.")

            except Exception:

                print("\nSnowflake INSERT failed.\n")
                traceback.print_exc()
                self.service.close()
                return

            log_agent_activity(
                self.agent_name,
                "Executive Report Generated"
            )

            self.service.close()

            print("\n" + "=" * 70)
            print("EXECUTIVE AGENT COMPLETED SUCCESSFULLY")
            print("=" * 70)

        except Exception:

            print("\nUnexpected Executive Agent Error\n")
            traceback.print_exc()

            try:
                self.service.close()
            except:
                pass


if __name__ == "__main__":

    ExecutiveAgent().run()