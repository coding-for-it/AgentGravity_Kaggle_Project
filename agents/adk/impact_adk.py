import time

from agents.impact_agent import ImpactAgent


class ImpactADKAgent:

    def __init__(self):

        self.name = "Impact ADK Agent"

    def execute(self):

        print("\n" + "=" * 60)
        print("ADK -> Impact Agent")
        print("=" * 60)

        start = time.time()

        try:

            ImpactAgent().run()

            elapsed = round(time.time() - start, 2)

            return {

                "agent": self.name,

                "status": "SUCCESS",

                "execution_time": elapsed

            }

        except Exception as e:

            return {

                "agent": self.name,

                "status": "FAILED",

                "error": str(e)

            }
