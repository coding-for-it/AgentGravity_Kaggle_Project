from agents.monitoring_agent import MonitoringAgent


class MonitoringADKAgent:

    def __init__(self):

        self.name = "Monitoring ADK Agent"

    def execute(self):

        print("\n[ADK] Running Monitoring Agent")

        agent = MonitoringAgent()

        result = agent.run()

        return result