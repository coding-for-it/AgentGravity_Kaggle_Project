from mcp.snowflake_mcp import SnowflakeMCP


mcp = SnowflakeMCP()


def clear_previous_workflow():

    print("Clearing previous workflow data...")

    tables = [

        "AGENTGRAVITY.INCIDENTS.RECOVERY_PLAN",

        "AGENTGRAVITY.INCIDENTS.EXECUTIVE_REPORTS",

        "AGENTGRAVITY.INCIDENTS.IMPACT_ANALYSIS",

        "AGENTGRAVITY.INCIDENTS.ROOT_CAUSES",

        "AGENTGRAVITY.INCIDENTS.INCIDENTS"

    ]

    for table in tables:

        mcp.execute_dml(

            f"DELETE FROM {table}"

        )

    print("Workflow tables cleared.\n")

def save_incidents(incidents):

    if len(incidents) == 0:
        return

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

    values = [

        (
            incident["kpi_id"],
            incident["incident_type"],
            incident["severity"],
            incident["description"]
        )

        for incident in incidents

    ]

    mcp.execute_many(
        query,
        values
    )

    print(f"Saved {len(values)} incidents.")