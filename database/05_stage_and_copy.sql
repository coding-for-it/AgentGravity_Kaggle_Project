-- =====================================================
-- AgentGravity
-- Stage + File Format + COPY INTO
-- =====================================================

USE DATABASE AGENTGRAVITY;

USE SCHEMA BUSINESS;

--------------------------------------------------------
-- FILE FORMAT
--------------------------------------------------------

CREATE OR REPLACE FILE FORMAT KPI_CSV_FORMAT

TYPE = CSV

FIELD_DELIMITER = ','

SKIP_HEADER = 1

FIELD_OPTIONALLY_ENCLOSED_BY = '"'

NULL_IF = ('NULL','');

--------------------------------------------------------
-- INTERNAL STAGE
--------------------------------------------------------

CREATE OR REPLACE STAGE KPI_STAGE

FILE_FORMAT = KPI_CSV_FORMAT;

--------------------------------------------------------
-- Upload CSV through Snowsight
--------------------------------------------------------

LIST @KPI_STAGE;

--------------------------------------------------------
-- Load CSV
--------------------------------------------------------

COPY INTO BUSINESS.KPI_METRICS
(
    KPI_DATE,
    REVENUE,
    ORDERS,
    CUSTOMERS,
    INVENTORY,
    CHURN_RATE
)
FROM @KPI_STAGE;

--------------------------------------------------------
-- Verify
--------------------------------------------------------

SELECT COUNT(*)

FROM BUSINESS.KPI_METRICS;