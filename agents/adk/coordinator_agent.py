from agents.adk.monitoring_adk import MonitoringADKAgent
from agents.adk.rootcause_adk import RootCauseADKAgent
from agents.adk.impact_adk import ImpactADKAgent
from agents.adk.executive_adk import ExecutiveADKAgent


class AgentGravityCoordinator:

    def __init__(self):

        self.monitoring = MonitoringADKAgent()

        self.rootcause = RootCauseADKAgent()

        self.impact = ImpactADKAgent()

        self.executive = ExecutiveADKAgent()

    def run(self):

        print("\n" + "=" * 60)
        print("AGENTGRAVITY ADK WORKFLOW")
        print("=" * 60)

        monitoring_result = self.monitoring.execute()

        self.rootcause.execute()

        self.impact.execute()

        self.executive.execute()

        print("\nWORKFLOW COMPLETED")

        return monitoring_result


if __name__ == "__main__":

    AgentGravityCoordinator().run()