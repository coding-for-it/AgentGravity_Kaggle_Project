import time

from agents.recovery_agent import RecoveryAgent


class RecoveryADKAgent:

    def __init__(self):

        self.name = "Recovery ADK Agent"

    def execute(self):

        print("\n" + "=" * 60)
        print("ADK → Recovery Agent")
        print("=" * 60)

        start = time.time()

        try:

            RecoveryAgent().run()

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