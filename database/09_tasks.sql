-- =====================================================
-- AgentGravity
-- Scheduled Tasks
-- =====================================================

USE DATABASE AGENTGRAVITY;

USE SCHEMA BUSINESS;

--------------------------------------------------------
-- DAILY KPI REFRESH
--------------------------------------------------------

CREATE OR REPLACE TASK DAILY_KPI_REFRESH

WAREHOUSE = COMPUTE_WH

SCHEDULE = 'USING CRON 0 9 * * * UTC'

AS

CALL SP_GET_KPI_SUMMARY();