from services.snowflake_connection import get_connection


def clear_previous_workflow():

    conn = get_connection()

    cursor = conn.cursor()

    print("Clearing previous workflow data...")

    cursor.execute("DELETE FROM AGENTGRAVITY.INCIDENTS.RECOVERY_PLAN")

    cursor.execute("DELETE FROM AGENTGRAVITY.INCIDENTS.EXECUTIVE_REPORTS")

    cursor.execute("DELETE FROM AGENTGRAVITY.INCIDENTS.IMPACT_ANALYSIS")

    cursor.execute("DELETE FROM AGENTGRAVITY.INCIDENTS.ROOT_CAUSES")

    cursor.execute("DELETE FROM AGENTGRAVITY.INCIDENTS.INCIDENTS")

    conn.commit()

    cursor.close()

    conn.close()

    print("Workflow tables cleared.\n")


def save_incidents(incidents):

    if len(incidents) == 0:
        return

    conn = get_connection()

    cursor = conn.cursor()

    query = """
    INSERT INTO AGENTGRAVITY.INCIDENTS.INCIDENTS
    (
        KPI_ID,
        INCIDENT_DATE,
        INCIDENT_TYPE,
        SEVERITY,
        STATUS,
        DESCRIPTION
    )
    VALUES
    (
        %s,
        CURRENT_TIMESTAMP(),
        %s,
        %s,
        'OPEN',
        %s
    )
    """

    values = []

    for incident in incidents:

        values.append(
            (
                incident["kpi_id"],
                incident["incident_type"],
                incident["severity"],
                incident["description"]
            )
        )

    cursor.executemany(query, values)

    conn.commit()

    cursor.close()

    conn.close()

    print(f"Saved {len(values)} incidents.")