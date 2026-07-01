import time

import pandas as pd

from services.snowflake_connection import get_connection


class AnalyticsEngine:

    def get_kpi_data(self):

        start = time.time()

        conn = get_connection()

        query = """
        SELECT
            KPI_ID,
            KPI_DATE,
            REVENUE,
            CHURN_RATE,
            INVENTORY
        FROM AGENTGRAVITY.BUSINESS.KPI_METRICS
        """

        df = pd.read_sql(query, conn)

        conn.close()

        print(f"KPI data loaded in {time.time()-start:.2f} sec")

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

        revenue_df = df[df["REVENUE"] < avg_revenue * 0.75]

        churn_df = df[df["CHURN_RATE"] > 5]

        inventory_df = df[df["INVENTORY"] < 250]

        for _, row in revenue_df.iterrows():

            incidents.append({

                "kpi_id": int(row["KPI_ID"]),

                "incident_type": "Revenue Drop",

                "severity": "HIGH",

                "description": f"Revenue dropped to {row['REVENUE']}"

            })

        for _, row in churn_df.iterrows():

            incidents.append({

                "kpi_id": int(row["KPI_ID"]),

                "incident_type": "High Churn",

                "severity": "HIGH",

                "description": f"Churn increased to {row['CHURN_RATE']}%"

            })

        for _, row in inventory_df.iterrows():

            incidents.append({

                "kpi_id": int(row["KPI_ID"]),

                "incident_type": "Inventory Risk",

                "severity": "MEDIUM",

                "description": f"Inventory reduced to {row['INVENTORY']}"

            })

        return incidents