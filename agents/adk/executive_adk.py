import time

from agents.executive_agent import ExecutiveAgent


class ExecutiveADKAgent:

    def __init__(self):

        self.name = "Executive ADK Agent"

    def execute(self):

        print("\n" + "=" * 60)
        print("ADK → Executive Agent")
        print("=" * 60)

        start = time.time()

        try:

            ExecutiveAgent().run()

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