-- =====================================================
-- AgentGravity
-- Business Queries
-- =====================================================

USE DATABASE AGENTGRAVITY;

--------------------------------------------------------
-- KPI DATA
--------------------------------------------------------

SELECT *

FROM BUSINESS.KPI_METRICS

ORDER BY KPI_DATE;

--------------------------------------------------------
-- BUSINESS HEALTH
--------------------------------------------------------

SELECT

AVG(REVENUE) AVG_REVENUE,

AVG(ORDERS) AVG_ORDERS,

AVG(CUSTOMERS) AVG_CUSTOMERS,

AVG(INVENTORY) AVG_INVENTORY,

AVG(CHURN_RATE) AVG_CHURN

FROM BUSINESS.KPI_METRICS;

--------------------------------------------------------
-- INCIDENTS
--------------------------------------------------------

SELECT *

FROM INCIDENTS.INCIDENTS

ORDER BY INCIDENT_DATE DESC;

--------------------------------------------------------
-- ROOT CAUSES
--------------------------------------------------------

SELECT *

FROM INCIDENTS.ROOT_CAUSES;

--------------------------------------------------------
-- IMPACT
--------------------------------------------------------

SELECT *

FROM INCIDENTS.IMPACT_ANALYSIS;

--------------------------------------------------------
-- EXECUTIVE REPORTS
--------------------------------------------------------

SELECT *

FROM INCIDENTS.EXECUTIVE_REPORTS;

--------------------------------------------------------
-- AUDIT LOG
--------------------------------------------------------

SELECT *

FROM SECURITY.AGENT_AUDIT_LOG

ORDER BY EXECUTION_TIME DESC;

--------------------------------------------------------
-- TOP REVENUE LOSS
--------------------------------------------------------

SELECT

I.INCIDENT_ID,

K.KPI_DATE,

IA.ESTIMATED_REVENUE_LOSS

FROM INCIDENTS.IMPACT_ANALYSIS IA

JOIN INCIDENTS.INCIDENTS I

ON IA.INCIDENT_ID = I.INCIDENT_ID

JOIN BUSINESS.KPI_METRICS K

ON I.KPI_ID = K.KPI_ID

ORDER BY IA.ESTIMATED_REVENUE_LOSS DESC;