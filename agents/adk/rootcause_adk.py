import time

from agents.root_cause_agent import RootCauseAgent


class RootCauseADKAgent:

    def __init__(self):

        self.name = "Root Cause ADK Agent"

    def execute(self):

        print("\n" + "=" * 60)
        print("ADK → Root Cause Agent")
        print("=" * 60)

        start = time.time()

        try:

            RootCauseAgent().run()

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