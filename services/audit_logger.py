from services.snowflake_connection import get_connection


def log_agent_activity(
        agent_name,
        action):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO
        AGENTGRAVITY.SECURITY.AGENT_AUDIT_LOG
        (
            AGENT_NAME,
            ACTION_PERFORMED,
            EXECUTION_TIME
        )
        VALUES
        (
            %s,
            %s,
            CURRENT_TIMESTAMP()
        )
        """,
        (
            agent_name,
            action
        )
    )

    conn.commit()

    cursor.close()

    conn.close()