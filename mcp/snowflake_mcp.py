from services.snowflake_connection import get_connection
import pandas as pd


class SnowflakeMCP:

    def __init__(self):

        self.conn = get_connection()

    def execute_query(self, query):

        return pd.read_sql(query, self.conn)

    def get_kpi_data(self):

        query = """
        SELECT *
        FROM AGENTGRAVITY.BUSINESS.KPI_METRICS
        ORDER BY KPI_DATE
        """

        return self.execute_query(query)

    def get_incidents(self):

        query = """
        SELECT *
        FROM AGENTGRAVITY.INCIDENTS.INCIDENTS
        ORDER BY INCIDENT_ID
        """

        return self.execute_query(query)

    def get_root_causes(self):

        query = """
        SELECT *
        FROM AGENTGRAVITY.INCIDENTS.ROOT_CAUSES
        ORDER BY ID
        """

        return self.execute_query(query)

    def get_audit_logs(self):

        query = """
        SELECT *
        FROM AGENTGRAVITY.SECURITY.AGENT_AUDIT_LOG
        ORDER BY ID
        """

        return self.execute_query(query)