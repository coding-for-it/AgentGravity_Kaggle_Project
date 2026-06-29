from services.snowflake_connection import get_connection
import pandas as pd


class AnalyticsEngine:

    def __init__(self):
        pass

    def get_kpi_data(self):

        conn = get_connection()

        query = """
        SELECT *
        FROM AGENTGRAVITY.BUSINESS.KPI_METRICS
        ORDER BY KPI_DATE
        """

        df = pd.read_sql(query, conn)

        conn.close()

        return df

    def calculate_business_health_score(self, df):

        revenue_score = min(
            (df["REVENUE"].mean() / 20000) * 100,
            100
        )

        churn_score = max(
            100 - (df["CHURN_RATE"].mean() * 10),
            0
        )

        inventory_score = min(
            (df["INVENTORY"].mean() / 500) * 100,
            100
        )

        return round(
            revenue_score * 0.4 +
            churn_score * 0.3 +
            inventory_score * 0.3,
            2
        )

    def detect_incidents(self, df):

        incidents = []

        avg_revenue = df["REVENUE"].mean()

        for _, row in df.iterrows():

            if row["REVENUE"] < avg_revenue * 0.75:

                incidents.append({

                    "kpi_id": int(row["KPI_ID"]),

                    "incident_type": "Revenue Drop",

                    "severity": "HIGH",

                    "description":
                    f"Revenue dropped to {row['REVENUE']}"

                })

            if row["CHURN_RATE"] > 5:

                incidents.append({

                    "kpi_id": int(row["KPI_ID"]),

                    "incident_type": "High Churn",

                    "severity": "HIGH",

                    "description":
                    f"Churn increased to {row['CHURN_RATE']}%"

                })

            if row["INVENTORY"] < 250:

                incidents.append({

                    "kpi_id": int(row["KPI_ID"]),

                    "incident_type": "Inventory Risk",

                    "severity": "MEDIUM",

                    "description":
                    f"Inventory reduced to {row['INVENTORY']}"

                })

        return incidents