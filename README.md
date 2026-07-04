# ⚡ AgentGravity
### AI-Powered Enterprise Business Operations Intelligence Platform

> Multi-Agent Business Intelligence System built using **Google ADK**, **Python**, **Snowflake**, **SQL**, **Gemini AI**, and **Streamlit**.

---

# Overview

AgentGravity is an enterprise-grade AI Operations Intelligence platform that continuously monitors business KPIs, detects anomalies, diagnoses root causes, estimates business impact, generates executive reports, and recommends recovery strategies using multiple AI agents.

Instead of dashboards that only visualize historical data, AgentGravity autonomously investigates business issues and delivers actionable business decisions.

The platform simulates an enterprise AI Control Tower where specialized agents collaborate to monitor organizational health.

---

# Problem Statement

Modern organizations monitor hundreds of KPIs every day.

When KPIs suddenly change, analysts typically spend hours answering questions such as:

- Which KPI failed?
- Why did it fail?
- How severe is the impact?
- Which business function is responsible?
- What actions should leadership take?

This manual investigation delays decision making.

AgentGravity automates the complete investigation lifecycle using AI agents.

---

# Solution

AgentGravity consists of multiple specialized AI agents working together.

```
Telemetry Data
        │
        ▼
Monitoring Agent
        │
        ▼
Root Cause Agent
        │
        ▼
Business Impact Agent
        │
        ▼
Executive Agent
        │
        ▼
Recovery Agent
```

Each agent performs one business responsibility before passing structured outputs to the next agent.

---

# Key Features

## 📊 Telemetry Data Upload

- Upload KPI dataset
- Automatic schema validation
- Data preview
- Snowflake ingestion

---

## 🤖 Monitoring Agent

Responsibilities

- Monitor KPI metrics
- Detect anomalies
- Identify abnormal business behavior
- Create Incident records

Outputs

- Incident Type
- Severity
- Status
- Confidence Score

---

## 🔍 Root Cause Agent

Responsibilities

- Diagnose business incidents
- Identify probable causes
- Calculate confidence score
- Map business domains

Outputs

- Cause Name
- Cause Category
- AI Confidence

---

## 💰 Business Impact Agent

Responsibilities

- Estimate financial loss
- Estimate customer impact
- Estimate inventory impact
- Estimate operational risk

Outputs

- Revenue Loss
- Business Severity
- Risk Category

---

## 👔 Executive Agent

Powered by Google Gemini

Responsibilities

- Read complete investigation
- Generate executive briefing
- Prioritize incidents
- Summarize risks

Outputs

- Executive Summary
- Strategic Recommendations
- Business Priority

---

## 🛠 Recovery Agent

Responsibilities

Generate

- Immediate actions
- Short-term strategy
- Long-term strategy
- Success metrics
- Expected business outcome

Outputs

- Recovery Playbook
- Risk Level
- Business Mitigation Strategy

---

## 🚀 Operations Center

Execute the complete multi-agent pipeline using a single click.

The Operations Center automatically runs:

Monitoring →
Root Cause →
Business Impact →
Executive →
Recovery

---

# Technology Stack

| Category | Technology |
|-----------|------------|
| Programming | Python |
| AI Framework | Google ADK |
| LLM | Google Gemini |
| Data Warehouse | Snowflake |
| Database | SQL |
| Dashboard | Streamlit |
| Visualization | Plotly |
| Data Processing | Pandas |
| Logging | Python Logging |
| Version Control | Git |

---

# Architecture

```
CSV Dataset
      │
      ▼
Snowflake Data Warehouse
      │
      ▼
Monitoring Agent
      │
      ▼
Root Cause Agent
      │
      ▼
Business Impact Agent
      │
      ▼
Executive Agent (Gemini)
      │
      ▼
Recovery Agent
      │
      ▼
Streamlit Enterprise Dashboard
```

---

# Folder Structure

```
AgentGravity/

│

├── agents/
│     monitoring_agent.py
│     root_cause_agent.py
│     impact_agent.py
│     executive_agent.py
│     recovery_agent.py
│
├── dashboard/
│     app.py
│
├── services/
│     monitoring_service.py
│     root_cause_service.py
│     impact_service.py
│     executive_service.py
│     recovery_service.py
│     antigravity_service.py
│
├── sql/
│
├── logs/
│
├── data/
│
├── requirements.txt
│
├── main.py
│
└── README.md
```

---

# AI Agent Workflow

## Step 1

Monitoring Agent

↓

Detect KPI anomalies

↓

Create Incident

---

## Step 2

Root Cause Agent

↓

Analyze Incident

↓

Generate Cause Analysis

---

## Step 3

Business Impact Agent

↓

Estimate Business Damage

↓

Calculate Revenue Loss

---

## Step 4

Executive Agent

↓

Generate Executive Briefing

↓

Assign Business Priority

---

## Step 5

Recovery Agent

↓

Generate Recovery Strategy

↓

Save Recovery Plan

---

# Dashboard Modules

- Data Upload
- Monitoring
- Root Cause Analysis
- Business Impact
- Executive Dashboard
- Recovery Strategy
- Operations Center

---

# Setup Instructions

## Clone Repository

```bash
git clone https://github.com/<username>/AgentGravity.git
```

---

## Install Requirements

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file

```text
SNOWFLAKE_ACCOUNT=
SNOWFLAKE_USER=
SNOWFLAKE_PASSWORD=
SNOWFLAKE_DATABASE=
SNOWFLAKE_SCHEMA=
SNOWFLAKE_WAREHOUSE=

GEMINI_API_KEY=
```

---

## Run Dashboard

```bash
streamlit run dashboard/app.py
```

---

## Run Complete Pipeline

```bash
python main.py
```

---

# Security

Sensitive credentials are stored using environment variables.

No API keys or passwords are committed to GitHub.

---

# Future Improvements

- MCP Tool Integration
- Live Streaming Data
- Predictive Forecasting
- Multi-user Authentication
- Slack / Teams Alerts
- Email Notification Agent
- Explainable AI Reports

---

# Project Highlights

✔ Multi-Agent Architecture

✔ Enterprise Dashboard

✔ Snowflake Data Warehouse

✔ AI Executive Reporting

✔ Business Impact Analysis

✔ Recovery Strategy Generation

✔ Google Gemini Integration

✔ Resume Ready

✔ Kaggle Capstone Ready

---

# Author

**Nimisha Rajendra**

Data Analytics | AI Agents | Snowflake | SQL | Python | Streamlit

---

# License

This project is created for educational, research, and portfolio purposes.
