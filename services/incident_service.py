from services.snowflake_connection import get_connection


def save_incidents(incidents):

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

    for incident in incidents:

        cursor.execute(
            query,
            (
                incident["kpi_id"],
                incident["incident_type"],
                incident["severity"],
                incident["description"]
            )
        )

    conn.commit()

    cursor.close()

    conn.close()

    print(f"\nSaved {len(incidents)} incidents.")