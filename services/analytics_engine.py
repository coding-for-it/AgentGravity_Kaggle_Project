from services.snowflake_connection import get_connection
from services.incident_service import save_incident
import pandas as pd


class AnalyticsEngine:

    def __init__(self):
        self.conn = get_connection()

    def get_kpi_data(self):

        query = """
        SELECT *
        FROM AGENTGRAVITY.BUSINESS.KPI_METRICS
        ORDER BY KPI_DATE
        """

        return pd.read_sql(query, self.conn)

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

        health_score = round(
            (revenue_score * 0.4)
            + (churn_score * 0.3)
            + (inventory_score * 0.3),
            2
        )

        return health_score

    def detect_incidents(self, df):

        incidents = []

        avg_revenue = df["REVENUE"].mean()

        for _, row in df.iterrows():

            if row["REVENUE"] < avg_revenue * 0.75:

                incidents.append({
                    "kpi_date": row["KPI_DATE"],
                    "incident_type": "Revenue Drop",
                    "severity": "HIGH",
                    "description":
                    f"Revenue dropped to {row['REVENUE']}"
                    })

            if row["CHURN_RATE"] > 5:
                incidents.append({
                    "kpi_date": row["KPI_DATE"],
                    "incident_type": "High Churn",
                    "severity": "HIGH",
                    "description":
                    f"Churn increased to {row['CHURN_RATE']}%"
                    })

            if row["INVENTORY"] < 250:

                incidents.append({
                    "kpi_date": row["KPI_DATE"],
                    "incident_type": "Inventory Risk",
                    "severity": "MEDIUM",
                    "description":
                    f"Inventory reduced to {row['INVENTORY']}"
                })

        return incidents


if __name__ == "__main__":

    engine = AnalyticsEngine()

    df = engine.get_kpi_data()

    print("\n===== KPI DATA =====")
    print(df)

    score = engine.calculate_business_health_score(df)

    print("\n===== BUSINESS HEALTH SCORE =====")
    print(score)

    incidents = engine.detect_incidents(df)

    print("\n===== INCIDENTS =====")
    
    for incident in incidents:
        print(incident)
        
        save_incident(
            incident["kpi_date"],
            incident["incident_type"],
            incident["severity"],
            incident["description"]
        )
    
    print("\nAll incidents saved successfully.")

    