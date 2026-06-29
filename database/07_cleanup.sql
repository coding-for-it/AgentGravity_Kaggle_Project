-- =====================================================
-- AgentGravity
-- Cleanup Script
-- =====================================================

USE DATABASE AGENTGRAVITY;

--------------------------------------------------------
-- Delete Data Only
--------------------------------------------------------

TRUNCATE TABLE INCIDENTS.EXECUTIVE_REPORTS;

TRUNCATE TABLE INCIDENTS.IMPACT_ANALYSIS;

TRUNCATE TABLE INCIDENTS.RECOVERY_ACTIONS;

TRUNCATE TABLE INCIDENTS.ROOT_CAUSES;

TRUNCATE TABLE INCIDENTS.INCIDENTS;

TRUNCATE TABLE BUSINESS.KPI_METRICS;

TRUNCATE TABLE SECURITY.AGENT_AUDIT_LOG;

--------------------------------------------------------
-- Verify
--------------------------------------------------------

SELECT COUNT(*) KPI_COUNT

FROM BUSINESS.KPI_METRICS;

SELECT COUNT(*) INCIDENT_COUNT

FROM INCIDENTS.INCIDENTS;