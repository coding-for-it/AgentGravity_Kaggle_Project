import time

from agents.adk.monitoring_adk import MonitoringADKAgent
from agents.adk.rootcause_adk import RootCauseADKAgent
from agents.adk.impact_adk import ImpactADKAgent
from agents.adk.executive_adk import ExecutiveADKAgent
from agents.adk.recovery_adk import RecoveryADKAgent


class AgentGravityCoordinator:

    def __init__(self):

        self.monitoring = MonitoringADKAgent()

        self.rootcause = RootCauseADKAgent()

        self.impact = ImpactADKAgent()

        self.executive = ExecutiveADKAgent()

        self.recovery = RecoveryADKAgent()

    def run(self):

        print("\n" + "=" * 70)
        print("AGENTGRAVITY AI ORCHESTRATION WORKFLOW")
        print("=" * 70)

        workflow_start = time.time()

        results = []

        agents = [

            self.monitoring,

            self.rootcause,

            self.impact,

            self.executive,

            self.recovery

        ]

        for agent in agents:

            result = agent.execute()

            results.append(result)

        total_time = round(

            time.time() - workflow_start,

            2

        )

        print("\n" + "=" * 70)
        print("WORKFLOW EXECUTION SUMMARY")
        print("=" * 70)

        for result in results:

            print(f"\nAgent : {result['agent']}")

            print(f"Status: {result['status']}")

            if result["status"] == "SUCCESS":

                print(

                    f"Time  : {result['execution_time']} sec"

                )

            else:

                print(

                    f"Error : {result['error']}"

                )

        print("\n" + "-" * 70)

        print(f"Total Workflow Time : {total_time} sec")

        print("Overall Status      : COMPLETED")

        print("=" * 70)

        return results


if __name__ == "__main__":

    AgentGravityCoordinator().run()