-- =====================================================
-- AgentGravity
-- Reporting Views
-- =====================================================

USE DATABASE AGENTGRAVITY;

--------------------------------------------------------
-- KPI SUMMARY
--------------------------------------------------------

CREATE OR REPLACE VIEW BUSINESS.VW_KPI_SUMMARY AS

SELECT

    KPI_DATE,

    AVG(REVENUE) AS AVG_REVENUE,

    AVG(ORDERS) AS AVG_ORDERS,

    AVG(CUSTOMERS) AS AVG_CUSTOMERS,

    AVG(INVENTORY) AS AVG_INVENTORY,

    AVG(CHURN_RATE) AS AVG_CHURN

FROM BUSINESS.KPI_METRICS

GROUP BY KPI_DATE;

--------------------------------------------------------
-- INCIDENT DETAILS
--------------------------------------------------------

CREATE OR REPLACE VIEW INCIDENTS.VW_INCIDENT_DETAILS AS

SELECT

    I.INCIDENT_ID,

    K.KPI_DATE,

    I.INCIDENT_TYPE,

    I.SEVERITY,

    I.STATUS,

    I.DESCRIPTION,

    K.REVENUE,

    K.ORDERS,

    K.CUSTOMERS,

    K.INVENTORY,

    K.CHURN_RATE

FROM INCIDENTS.INCIDENTS I

JOIN BUSINESS.KPI_METRICS K

ON I.KPI_ID = K.KPI_ID;