from agents.impact_agent import ImpactAgent


class ImpactADKAgent:

    def __init__(self):

        self.name = "Impact ADK Agent"

    def execute(self):

        print("\n[ADK] Running Impact Agent")

        agent = ImpactAgent()

        agent.run()

        return {
            "status": "completed"
        }