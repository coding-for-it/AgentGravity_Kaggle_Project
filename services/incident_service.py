from services.snowflake_connection import get_connection


def save_incident(
    kpi_date,
    incident_type,
    severity,
    description
):

    conn = get_connection()

    cursor = conn.cursor()

    query = """
    INSERT INTO AGENTGRAVITY.INCIDENTS.INCIDENTS
    (
        KPI_DATE,
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

    cursor.execute(
        query,
        (
            kpi_date,
            incident_type,
            severity,
            description
        )
    )

    conn.commit()

    cursor.close()
    conn.close()