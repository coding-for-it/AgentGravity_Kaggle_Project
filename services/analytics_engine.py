import time

from mcp.snowflake_mcp import SnowflakeMCP


class AnalyticsEngine:

    def __init__(self):

        self.mcp = SnowflakeMCP()

    def get_kpi_data(self):

        start = time.time()

        query = """
        SELECT
            KPI_ID,
            KPI_DATE,
            REVENUE,
            CHURN_RATE,
            INVENTORY
        FROM AGENTGRAVITY.BUSINESS.KPI_METRICS
        ORDER BY KPI_DATE
        """

        df = self.mcp.execute_query(query)

        df["HEALTH_SCORE"] = df.apply(
            self.calculate_daily_health,
            axis=1
        )

        print(
            f"KPI data loaded in {time.time() - start:.2f} sec"
        )

        return df

    # ----------------------------------------------------
    # Daily Health Score
    # ----------------------------------------------------

    def calculate_daily_health(self, row):

        revenue_score = min(
            (row["REVENUE"] / 10000) * 100,
            100
        )

        churn_score = max(
            0,
            100 - (row["CHURN_RATE"] * 10)
        )

        inventory_score = min(
            (row["INVENTORY"] / 1000) * 100,
            100
        )

        health_score = (

            revenue_score * 0.50 +

            churn_score * 0.30 +

            inventory_score * 0.20

        )

        return round(
            health_score,
            2
        )

    # ----------------------------------------------------

    def calculate_business_health_score(self, df):

        return round(

            df["HEALTH_SCORE"].mean(),

            2

        )

    # ----------------------------------------------------

    def detect_incidents(self, df):

        incidents = []

        avg_revenue = df["REVENUE"].mean()

        revenue_df = df[
            df["REVENUE"] < avg_revenue * 0.75
        ]

        churn_df = df[
            df["CHURN_RATE"] > 5
        ]

        inventory_df = df[
            df["INVENTORY"] < 250
        ]

        for _, row in revenue_df.iterrows():

            incidents.append({

                "kpi_id": int(row["KPI_ID"]),

                "incident_type": "Revenue Drop",

                "severity": "HIGH",

                "description":
                    f"Revenue dropped to {row['REVENUE']}"

            })

        for _, row in churn_df.iterrows():

            incidents.append({

                "kpi_id": int(row["KPI_ID"]),

                "incident_type": "High Churn",

                "severity": "HIGH",

                "description":
                    f"Churn increased to {row['CHURN_RATE']}%"

            })

        for _, row in inventory_df.iterrows():

            incidents.append({

                "kpi_id": int(row["KPI_ID"]),

                "incident_type": "Inventory Risk",

                "severity": "MEDIUM",

                "description":
                    f"Inventory reduced to {row['INVENTORY']}"

            })

        return incidents