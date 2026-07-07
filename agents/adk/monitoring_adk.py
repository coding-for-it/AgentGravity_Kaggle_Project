import time

from agents.monitoring_agent import MonitoringAgent


class MonitoringADKAgent:

    def __init__(self):

        self.name = "Monitoring ADK Agent"

    def execute(self):

        print("\n" + "=" * 60)
        print("ADK -> Monitoring Agent")
        print("=" * 60)

        start = time.time()

        try:

            result = MonitoringAgent().run()

            elapsed = round(time.time() - start, 2)

            return {

                "agent": self.name,

                "status": "SUCCESS",

                "execution_time": elapsed,

                "result": result

            }

        except Exception as e:

            return {

                "agent": self.name,

                "status": "FAILED",

                "error": str(e)

            }
