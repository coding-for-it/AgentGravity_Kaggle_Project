import os
import sys
import traceback

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from services.recovery_service import RecoveryService
from services.audit_logger import log_agent_activity
from services.logger import get_logger


class RecoveryAgent:

    def __init__(self):

        self.agent_name = "Recovery Agent"

        self.logger = get_logger("recovery")

        self.service = RecoveryService()

    def build_recovery_plan(self, priority):

        if priority == "CRITICAL":

            return {

                "immediate_actions":
                "Establish a crisis response team immediately, restore inventory availability, investigate high-churn customers, and notify executive leadership.",

                "short_term_actions":
                "Optimize inventory planning, strengthen customer retention campaigns, improve supplier coordination, and monitor KPIs daily.",

                "long_term_actions":
                "Implement AI-driven demand forecasting, automated inventory replenishment, customer experience improvements, and predictive monitoring.",

                "expected_business_outcome":
                "Reduce revenue loss, stabilize customer churn, improve inventory health, and restore operational performance.",

                "success_metrics":
                "Revenue Growth, Customer Retention, Inventory Availability, Reduced Critical Incidents.",

                "risk_level":
                "CRITICAL"
            }

        elif priority == "HIGH":

            return {

                "immediate_actions":
                "Investigate major business risks and assign responsible business teams.",

                "short_term_actions":
                "Improve forecasting accuracy and optimize inventory allocation.",

                "long_term_actions":
                "Implement predictive analytics and proactive business monitoring.",

                "expected_business_outcome":
                "Lower revenue loss and improved operational efficiency.",

                "success_metrics":
                "Reduced Incident Count, Higher Revenue, Lower Churn.",

                "risk_level":
                "HIGH"
            }

        elif priority == "MEDIUM":

            return {

                "immediate_actions":
                "Monitor KPIs closely and investigate recurring incidents.",

                "short_term_actions":
                "Improve reporting and business process efficiency.",

                "long_term_actions":
                "Increase automation and strengthen business intelligence capabilities.",

                "expected_business_outcome":
                "Improved KPI stability and operational consistency.",

                "success_metrics":
                "Improved KPI Trends and Customer Satisfaction.",

                "risk_level":
                "MEDIUM"
            }

        else:

            return {

                "immediate_actions":
                "Continue routine KPI monitoring.",

                "short_term_actions":
                "Review business performance monthly.",

                "long_term_actions":
                "Expand AI monitoring capabilities.",

                "expected_business_outcome":
                "Stable business operations.",

                "success_metrics":
                "Consistent KPI Performance.",

                "risk_level":
                "LOW"
            }

    def run(self):

        try:

            print("\n" + "=" * 60)
            print("Recovery Agent Started")
            print("=" * 60)

            self.logger.info("=" * 60)
            self.logger.info("Recovery Agent Started")

            log_agent_activity(
                self.agent_name,
                "Recovery Strategy Started"
            )

            self.logger.info("Loading executive report")

            print("\nFetching latest executive report...")

            df = self.service.get_executive_report()

            self.logger.info(
                f"Loaded {len(df)} executive report(s)"
            )

            print("\nExecutive Report Data:")
            print(df)

            if df.empty:

                self.logger.warning(
                    "No Executive Report Found"
                )

                print("\nNo Executive Report Found.")

                self.service.close()

                return

            print("\nExecutive report loaded successfully.")

            executive_summary = df.iloc[0]["EXECUTIVE_SUMMARY"]

            priority = df.iloc[0]["BUSINESS_PRIORITY"]

            self.logger.info(
                f"Business Priority: {priority}"
            )

            print(f"\nBusiness Priority : {priority}")

            self.logger.info(
                "Generating recovery strategy"
            )

            plan = self.build_recovery_plan(priority)

            print("\nRecovery plan generated successfully.")

            self.logger.info(
                "Saving recovery plan to Snowflake"
            )

            self.service.save_recovery_plan(

                executive_summary,

                plan["immediate_actions"],

                plan["short_term_actions"],

                plan["long_term_actions"],

                plan["expected_business_outcome"],

                plan["success_metrics"],

                plan["risk_level"]

            )

            self.logger.info(
                "Recovery plan saved successfully"
            )

            print("\nRecovery plan saved into Snowflake.")

            log_agent_activity(
                self.agent_name,
                "Recovery Strategy Generated"
            )

            self.service.close()

            print("\n" + "=" * 60)
            print("RECOVERY PLAN")
            print("=" * 60)

            print("\nPriority :", priority)

            print("\nImmediate Actions")
            print(plan["immediate_actions"])

            print("\nShort Term Actions")
            print(plan["short_term_actions"])

            print("\nLong Term Actions")
            print(plan["long_term_actions"])

            print("\nExpected Outcome")
            print(plan["expected_business_outcome"])

            print("\nSuccess Metrics")
            print(plan["success_metrics"])

            print("\nRisk Level")
            print(plan["risk_level"])

            print("\nRecovery plan saved successfully.")

            print("\n" + "=" * 60)

            self.logger.info("Recovery Agent Completed")
            self.logger.info("=" * 60)

        except Exception:

            self.logger.exception(
                "Unexpected Recovery Agent Error"
            )

            print("\nUnexpected Recovery Agent Error\n")

            traceback.print_exc()

            try:
                self.service.close()
            except:
                pass


if __name__ == "__main__":

    RecoveryAgent().run()