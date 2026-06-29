-- =====================================================
-- AgentGravity
-- Stored Procedures
-- =====================================================

USE DATABASE AGENTGRAVITY;

USE SCHEMA BUSINESS;

--------------------------------------------------------
-- KPI SUMMARY PROCEDURE
--------------------------------------------------------

CREATE OR REPLACE PROCEDURE SP_GET_KPI_SUMMARY()

RETURNS STRING

LANGUAGE SQL

AS

$$

BEGIN

SELECT

AVG(REVENUE),

AVG(ORDERS),

AVG(CUSTOMERS),

AVG(INVENTORY),

AVG(CHURN_RATE)

FROM KPI_METRICS;

RETURN 'Business KPI Summary Generated';

END;

$$;