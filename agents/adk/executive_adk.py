from agents.executive_agent import ExecutiveAgent


class ExecutiveADKAgent:

    def __init__(self):

        self.name = "Executive ADK Agent"

    def execute(self):

        print("\n[ADK] Running Executive Agent")

        agent = ExecutiveAgent()

        agent.run()

        return {
            "status": "completed"
        }