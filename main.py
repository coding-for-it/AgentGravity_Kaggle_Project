from agents.monitoring_agent import MonitoringAgent
from agents.root_cause_agent import RootCauseAgent
from agents.impact_agent import ImpactAgent
from agents.executive_agent import ExecutiveAgent


def main():

    print("\n" + "=" * 60)
    print("AGENTGRAVITY COMMAND CENTER")
    print("=" * 60)

    print("\nSTEP 1: Monitoring Agent")
    monitoring_agent = MonitoringAgent()
    monitoring_result = monitoring_agent.run()

    print("\nSTEP 2: Root Cause Agent")
    root_cause_agent = RootCauseAgent()
    root_cause_agent.run()

    print("\nSTEP 3: Impact Agent")
    impact_agent = ImpactAgent()
    impact_agent.run()

    print("\nSTEP 4: Executive Agent")
    executive_agent = ExecutiveAgent()
    executive_agent.run()

    print("\n" + "=" * 60)
    print("WORKFLOW COMPLETED")
    print("=" * 60)

    return monitoring_result


if __name__ == "__main__":
    main()