import pandas as pd
from services.snowflake_connection import get_connection


def load_business_data():

    df = pd.read_csv("data/raw/business_data.csv")

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        TRUNCATE TABLE AGENTGRAVITY.BUSINESS.KPI_METRICS
    """)

    for _, row in df.iterrows():

        cursor.execute(
            """
            INSERT INTO AGENTGRAVITY.BUSINESS.KPI_METRICS
            (
                KPI_DATE,
                REVENUE,
                ORDERS,
                CUSTOMERS,
                INVENTORY,
                CHURN_RATE
            )
            VALUES (%s,%s,%s,%s,%s,%s)
            """,
            (
                row["kpi_date"],
                row["revenue"],
                row["orders"],
                row["customers"],
                row["inventory"],
                row["churn_rate"]
            )
        )

    conn.commit()

    cursor.close()
    conn.close()

    print("Data Loaded Successfully")


if __name__ == "__main__":
    load_business_data()