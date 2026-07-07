import os
import sys

os.system("chcp 65001 > nul")

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
from agents.adk.monitoring_adk import MonitoringADKAgent
from agents.adk.rootcause_adk import RootCauseADKAgent
from agents.adk.impact_adk import ImpactADKAgent
from agents.adk.executive_adk import ExecutiveADKAgent
from agents.adk.recovery_adk import RecoveryADKAgent

from services.logger import get_logger

logger = get_logger("pipeline")


def main():

    logger.info("=" * 60)
    logger.info("AgentGravity Pipeline Started")
    logger.info("=" * 60)

    print("\n" + "=" * 60)
    print("AGENTGRAVITY COMMAND CENTER")
    print("=" * 60)

    try:

        # -------------------------------------------------
        # STEP 1
        # -------------------------------------------------
        print("\nSTEP 1: Monitoring Agent", flush=True)
        logger.info("STEP 1 : Monitoring Agent Started")

        monitoring_agent = MonitoringADKAgent()
        monitoring_result = monitoring_agent.execute()

        logger.info("Monitoring Agent Completed")

        # -------------------------------------------------
        # STEP 2
        # -------------------------------------------------
        print("\nSTEP 2: Root Cause Agent", flush=True)
        logger.info("STEP 2 : Root Cause Agent Started")

        root_cause_agent = RootCauseADKAgent()
        root_cause_agent.execute()

        logger.info("Root Cause Agent Completed")

        # -------------------------------------------------
        # STEP 3
        # -------------------------------------------------
        print("\nSTEP 3: Impact Agent", flush=True)
        logger.info("STEP 3 : Impact Agent Started")

        impact_agent = ImpactADKAgent()
        impact_agent.execute()

        logger.info("Impact Agent Completed")

        # -------------------------------------------------
        # STEP 4
        # -------------------------------------------------
        print("\nSTEP 4: Executive Agent", flush=True)
        logger.info("STEP 4 : Executive Agent Started")

        executive_agent = ExecutiveADKAgent()
        executive_agent.execute()

        logger.info("Executive Agent Completed")

        # -------------------------------------------------
        # STEP 5
        # -------------------------------------------------
        print("\nSTEP 5: Recovery Agent", flush=True)
        logger.info("STEP 5 : Recovery Agent Started")

        recovery_agent = RecoveryADKAgent()
        recovery_agent.execute()

        logger.info("Recovery Agent Completed")

        print("\n" + "=" * 60)
        print("WORKFLOW COMPLETED", flush=True)
        print("=" * 60)

        logger.info("Pipeline Completed Successfully")
        logger.info("=" * 60)

        return monitoring_result

    except Exception as e:

        logger.exception("Pipeline Failed")

        print("\n" + "=" * 60)
        print("PIPELINE FAILED")
        print("=" * 60)
        print(str(e))

        raise


if __name__ == "__main__":
    main()
