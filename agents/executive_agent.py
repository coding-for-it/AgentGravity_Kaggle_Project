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

        print("\n" + "=" * 60)
        print("Executive Agent Started")
        print("=" * 60)

        log_agent_activity(
            self.agent_name,
            "Executive Report Started"
        )

        df = self.service.get_business_summary()

        if df.empty:

            print("\nNo business data found.")

            self.service.close()

            return

        business_summary = self.build_business_summary(df)

        print("\nSending Business Summary to Gemini...\n")

        executive_briefing = (
            self.ai.generate_executive_briefing(
                business_summary
            )
        )

        priority = self.determine_priority(df)

        self.service.save_executive_report(
            executive_briefing,
            "Refer Executive Summary",
            priority
        )

        log_agent_activity(
            self.agent_name,
            "Executive Report Generated"
        )

        self.service.close()

        print("\n" + "=" * 60)
        print("EXECUTIVE BRIEFING")
        print("=" * 60)

        print(executive_briefing)

        print("\nPriority :", priority)

        print("\nExecutive report saved successfully.")

        print("\n" + "=" * 60)


if __name__ == "__main__":

    ExecutiveAgent().run()