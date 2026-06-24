from agents.root_cause_agent import RootCauseAgent


class RootCauseADKAgent:

    def __init__(self):

        self.name = "Root Cause ADK Agent"

    def execute(self):

        print("\n[ADK] Running Root Cause Agent")

        agent = RootCauseAgent()

        agent.run()

        return {
            "status": "completed"
        }