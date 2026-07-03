import os
import sys
import subprocess
import time
import re
import datetime
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Add project root directory to path to resolve imports correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.analytics_engine import AnalyticsEngine
from services.snowflake_connection import get_connection

# ===========================================================
# SECTION 1 — PAGE CONFIGURATION
# ===========================================================
st.set_page_config(
    page_title="AgentGravity Command Center",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================================================
# SECTION 2 — PREMIUM CSS / GLASSMORPHISM DARK THEME
# ===========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap');

/* Main CSS overrides */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    font-family: 'Inter', -apple-system, sans-serif;
    background-color: #060810 !important;
    color: #E2E8F0;
}

[data-testid="stHeader"] {
    background-color: rgba(6, 8, 16, 0.7) !important;
    backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

[data-testid="stSidebar"] {
    background-color: #03050A !important;
    border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
}

/* Glassmorphism Card Container */
.glass-card {
    background: rgba(255, 255, 255, 0.02);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.06);
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
    transition: transform 0.2s ease, border-color 0.2s ease;
}
.glass-card:hover {
    border-color: rgba(255, 255, 255, 0.12);
}

/* KPI Custom Grid styling */
.kpi-container {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    margin-bottom: 24px;
    width: 100%;
}
.kpi-card-custom {
    flex: 1;
    min-width: 220px;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.025) 0%, rgba(255, 255, 255, 0.005) 100%);
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.06);
    padding: 20px;
    transition: all 0.2s;
    border-left: 4px solid #3B82F6;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}
.kpi-card-custom:hover {
    transform: translateY(-2px);
    border-color: rgba(255, 255, 255, 0.12);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

.kpi-label {
    font-size: 11px;
    font-weight: 600;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.kpi-value {
    font-size: 32px;
    font-weight: 700;
    font-family: 'Outfit', sans-serif;
    color: #FFFFFF;
    margin-top: 6px;
    margin-bottom: 4px;
}
.kpi-delta {
    font-size: 12px;
    font-weight: 600;
    display: flex;
    align-items: center;
}
.delta-up {
    color: #10B981;
}
.delta-down {
    color: #EF4444;
}

/* Consultation-style report layout */
.briefing-box {
    background: rgba(255, 255, 255, 0.015);
    border-left: 4px solid #8B5CF6;
    border-radius: 8px;
    padding: 20px;
    margin-top: 15px;
    font-size: 14px;
    line-height: 1.6;
    color: #CBD5E1;
}

.briefing-title {
    font-family: 'Outfit', sans-serif;
    font-weight: 600;
    font-size: 16px;
    color: #FFFFFF;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Custom Pills */
.badge {
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    border: 1px solid transparent;
    display: inline-block;
}
.badge-critical {
    background-color: rgba(239, 68, 68, 0.12);
    color: #F87171;
    border-color: rgba(239, 68, 68, 0.25);
}
.badge-high {
    background-color: rgba(249, 115, 22, 0.12);
    color: #FB923C;
    border-color: rgba(249, 115, 22, 0.25);
}
.badge-medium {
    background-color: rgba(245, 158, 11, 0.12);
    color: #FBBF24;
    border-color: rgba(245, 158, 11, 0.25);
}
.badge-low {
    background-color: rgba(16, 185, 129, 0.12);
    color: #34D399;
    border-color: rgba(16, 185, 129, 0.25);
}

.gradient-title {
    background: linear-gradient(135deg, #E2E8F0 0%, #94A3B8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
}
.terminal-window {
    background-color: #030509;
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 10px;
    padding: 18px;
    font-family: 'Courier New', Courier, monospace;
    font-size: 13px;
    color: #38BDF8;
    overflow-y: auto;
    max-height: 380px;
    margin-top: 10px;
    box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.8);
}

/* Empty state */
.empty-state {
    text-align: center;
    padding: 50px 20px;
}
.empty-state-icon {
    font-size: 44px;
    margin-bottom: 16px;
}
.empty-state-title {
    font-family: 'Outfit', sans-serif;
    font-weight: 600;
    font-size: 18px;
    color: #FFFFFF;
    margin-bottom: 8px;
}
.empty-state-message {
    font-size: 13px;
    color: #64748B;
    line-height: 1.6;
}

/* Agent card */
.agent-card {
    background: rgba(255, 255, 255, 0.015);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.agent-name {
    font-weight: 600;
    font-size: 13px;
    color: #FFFFFF;
}
.agent-role {
    font-size: 11px;
    color: #94A3B8;
    margin-top: 3px;
}
</style>
""", unsafe_allow_html=True)

# ===========================================================
# SECTION 3 — SNOWFLAKE HELPERS
# ===========================================================

@st.cache_resource(ttl=60)
def check_connection():
    try:
        conn = get_connection()
        conn.close()
        return True, None
    except Exception as e:
        return False, str(e)

is_connected, conn_error = check_connection()


def execute_query(query):
    """Execute a SQL query and return a DataFrame. Returns empty DataFrame on failure."""
    if not is_connected:
        return pd.DataFrame()
    try:
        conn = get_connection()
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"SQL Execution Error: {e}")
        return pd.DataFrame()


def upload_kpis_to_snowflake(df, truncate=True):
    """Batch-upload KPI DataFrame to Snowflake with progress reporting."""
    if not is_connected:
        return False, "Snowflake connection is offline. Please populate `.env` settings."

    conn = get_connection()
    cursor = conn.cursor()
    try:
        if truncate:
            cursor.execute("TRUNCATE TABLE AGENTGRAVITY.BUSINESS.KPI_METRICS")
            conn.commit()

        query = """
        INSERT INTO AGENTGRAVITY.BUSINESS.KPI_METRICS
        (
            KPI_DATE,
            REVENUE,
            ORDERS,
            CUSTOMERS,
            INVENTORY,
            CHURN_RATE
        )
        VALUES (%s,%s,%s,%s,%s,%s)
        """

        chunk_size = 100
        num_rows = len(df)
        num_chunks = int(np.ceil(num_rows / chunk_size))

        progress_bar = st.progress(0.0)
        status_text = st.empty()

        for i in range(num_chunks):
            chunk = df.iloc[i * chunk_size: (i + 1) * chunk_size]
            values = []
            for _, row in chunk.iterrows():
                val_date = str(row["KPI_DATE"]).split(" ")[0]
                values.append((
                    val_date,
                    float(row["REVENUE"]),
                    int(row["ORDERS"]),
                    int(row["CUSTOMERS"]),
                    int(row["INVENTORY"]),
                    float(row["CHURN_RATE"])
                ))
            cursor.executemany(query, values)
            conn.commit()

            prog = (i + 1) / num_chunks
            progress_bar.progress(prog)
            status_text.text(f"Uploading rows {min((i + 1) * chunk_size, num_rows)} / {num_rows}...")

        status_text.empty()
        progress_bar.empty()
        return True, num_rows
    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()


# ===========================================================
# SECTION 4 — DATA LOADERS
# ===========================================================

def load_kpi_data():
    if is_connected:
        df = execute_query("SELECT * FROM AGENTGRAVITY.BUSINESS.KPI_METRICS ORDER BY KPI_DATE")
        if not df.empty:
            df['KPI_DATE'] = pd.to_datetime(df['KPI_DATE'])
            return df

    # Fallback to local business data
    if os.path.exists("data/kpi_data.csv"):
        df = pd.read_csv("data/kpi_data.csv")
        df['KPI_DATE'] = pd.to_datetime(df['KPI_DATE'])
        return df
    return pd.DataFrame()


def load_incidents_data():
    if is_connected:
        return execute_query("""
            SELECT I.INCIDENT_ID, I.KPI_ID, I.INCIDENT_DATE, I.INCIDENT_TYPE, I.SEVERITY, I.STATUS, I.DESCRIPTION,
                   K.KPI_DATE, K.REVENUE, K.ORDERS, K.CUSTOMERS, K.INVENTORY, K.CHURN_RATE
            FROM AGENTGRAVITY.INCIDENTS.INCIDENTS I
            LEFT JOIN AGENTGRAVITY.BUSINESS.KPI_METRICS K ON I.KPI_ID = K.KPI_ID
            ORDER BY I.INCIDENT_DATE DESC
        """)
    return pd.DataFrame(columns=["INCIDENT_ID", "KPI_ID", "INCIDENT_DATE", "INCIDENT_TYPE", "SEVERITY", "STATUS", "DESCRIPTION"])


def load_root_causes_data():
    if is_connected:
        return execute_query("""
            SELECT RC.ROOT_CAUSE_ID, RC.INCIDENT_ID, RC.CAUSE_NAME, RC.CONFIDENCE_SCORE,
                   I.INCIDENT_TYPE, I.SEVERITY, I.STATUS, I.DESCRIPTION, I.INCIDENT_DATE
            FROM AGENTGRAVITY.INCIDENTS.ROOT_CAUSES RC
            LEFT JOIN AGENTGRAVITY.INCIDENTS.INCIDENTS I ON RC.INCIDENT_ID = I.INCIDENT_ID
            ORDER BY RC.ROOT_CAUSE_ID DESC
        """)
    return pd.DataFrame(columns=["ROOT_CAUSE_ID", "INCIDENT_ID", "CAUSE_NAME", "CONFIDENCE_SCORE"])


def load_impacts_data():
    if is_connected:
        return execute_query("""
            SELECT IA.IMPACT_ID, IA.INCIDENT_ID, IA.ESTIMATED_REVENUE_LOSS, IA.BUSINESS_SEVERITY, IA.CREATED_AT,
                   I.INCIDENT_TYPE, I.STATUS, I.DESCRIPTION
            FROM AGENTGRAVITY.INCIDENTS.IMPACT_ANALYSIS IA
            LEFT JOIN AGENTGRAVITY.INCIDENTS.INCIDENTS I ON IA.INCIDENT_ID = I.INCIDENT_ID
            ORDER BY IA.CREATED_AT DESC
        """)
    return pd.DataFrame(columns=["IMPACT_ID", "INCIDENT_ID", "ESTIMATED_REVENUE_LOSS", "BUSINESS_SEVERITY", "CREATED_AT"])


def load_recovery_plan():
    if is_connected:
        return execute_query("""
            SELECT PLAN_ID, GENERATED_AT, EXECUTIVE_SUMMARY, IMMEDIATE_ACTIONS, SHORT_TERM_ACTIONS, LONG_TERM_ACTIONS,
                   EXPECTED_BUSINESS_OUTCOME, SUCCESS_METRICS, RISK_LEVEL
            FROM AGENTGRAVITY.INCIDENTS.RECOVERY_PLAN
            ORDER BY GENERATED_AT DESC
            LIMIT 1
        """)
    return pd.DataFrame()


def load_executive_reports():
    if is_connected:
        return execute_query("""
            SELECT REPORT_ID, INCIDENT_ID, EXECUTIVE_SUMMARY, RECOMMENDED_ACTION, BUSINESS_PRIORITY, CREATED_AT
            FROM AGENTGRAVITY.INCIDENTS.EXECUTIVE_REPORTS
            ORDER BY CREATED_AT DESC
            LIMIT 1
        """)
    return pd.DataFrame()


def load_audit_logs():
    if is_connected:
        return execute_query("""
            SELECT LOG_ID, AGENT_NAME, ACTION_PERFORMED, EXECUTION_TIME
            FROM AGENTGRAVITY.SECURITY.AGENT_AUDIT_LOG
            ORDER BY EXECUTION_TIME DESC
        """)
    return pd.DataFrame(columns=["LOG_ID", "AGENT_NAME", "ACTION_PERFORMED", "EXECUTION_TIME"])


# ===========================================================
# SECTION 5 — VISUALIZATION & UI HELPERS
# ===========================================================

def render_kpi_card(title, value, delta=None, delta_positive=True, border_color="#3B82F6"):
    """Render a premium KPI card with optional delta indicator."""
    delta_html = ""
    if delta is not None:
        color_class = "delta-up" if delta_positive else "delta-down"
        arrow = "▲" if delta_positive else "▼"
        delta_html = f'<div class="kpi-delta {color_class}">{arrow} {delta}</div>'

    st.markdown(f"""
    <div class="kpi-card-custom" style="border-left-color: {border_color};">
        <div class="kpi-label">{title}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def render_pill(severity):
    """Render a color-coded severity badge pill."""
    severity_lower = str(severity).lower().strip()
    badge_class = "badge-low"
    if "critical" in severity_lower:
        badge_class = "badge-critical"
    elif "high" in severity_lower:
        badge_class = "badge-high"
    elif "medium" in severity_lower:
        badge_class = "badge-medium"
    return f'<span class="badge {badge_class}">{severity}</span>'


def apply_plotly_theme(fig, height=350):
    """Apply the AntiGravity dark theme to any Plotly figure."""
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#94A3B8',
        font_family='Inter, sans-serif',
        title_font_family='Outfit, sans-serif',
        title_font_color='#FFFFFF',
        title_font_size=15,
        height=height,
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.03)',
            zerolinecolor='rgba(255,255,255,0.05)',
            tickfont=dict(color='#64748B')
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.03)',
            zerolinecolor='rgba(255,255,255,0.05)',
            tickfont=dict(color='#64748B')
        ),
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(255,255,255,0.05)',
            font=dict(size=11)
        )
    )

def parse_executive_report(text):
    """Parse Gemini-generated executive report text into keyed sections."""
    sections = {
        "Executive Summary": "No Executive Summary generated.",
        "Top Business Risks": "No Risks identified.",
        "Business Impact": "No Impact details available.",
        "Recommended Actions": "No recommendations recorded.",
        "Priority Level": "UNKNOWN"
    }

    if not text:
        return sections

    current_key = "Executive Summary"
    lines = text.split('\n')
    buffer = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        matched = False
        for sec in sections.keys():
            if sec.lower() in stripped.lower() and len(stripped) < len(sec) + 4:
                sections[current_key] = "\n".join(buffer).strip()
                current_key = sec
                buffer = []
                matched = True
                break

        if not matched:
            buffer.append(line)

    if buffer:
        sections[current_key] = "\n".join(buffer).strip()

    sections["Priority Level"] = sections["Priority Level"].replace("Priority Level", "").replace(":", "").strip()
    return sections


def render_empty_state(icon, title, message):
    """Render a standardized empty-state placeholder."""
    st.markdown(f"""
    <div class="empty-state">
        <div class="empty-state-icon">{icon}</div>
        <div class="empty-state-title">{title}</div>
        <div class="empty-state-message">{message}</div>
    </div>
    """, unsafe_allow_html=True)


def render_agent_console(script_path, button_label, spinner_msg, section_title="Execution Console"):
    """
    Reusable agent launcher with live terminal streaming.
    Runs the given script as a subprocess and streams stdout to the terminal window.
    Refreshes Streamlit on success.
    """
    st.markdown(f'<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(f"### {section_title}")

    if st.button(button_label, type="primary"):
        log_placeholder = st.empty()
        with st.spinner(spinner_msg):
            try:
                # Project root
                project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                # Convert "agents/monitoring_agent.py"
                # into "agents.monitoring_agent"
                module_name = (
                    script_path
                    .replace("/", ".")
                    .replace("\\", ".")
                    .replace(".py", "")
                )
                
                proc = subprocess.Popen(
                    [
                        sys.executable,
                        "-m",
                        module_name
                    ],
                    cwd=project_root,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )
                

                log_content = f"[System] Starting {script_path}...\n"
                log_placeholder.markdown(
                    f'<div class="terminal-window">{log_content}</div>',
                    unsafe_allow_html=True
                )

                while True:
                    line = proc.stdout.readline()
                    if not line:
                        break
                    log_content += line
                    log_placeholder.markdown(
                        f'<div class="terminal-window">{log_content}</div>',
                        unsafe_allow_html=True
                    )

                proc.communicate()

                if proc.returncode == 0:
                    log_content += "\n[System] ✓ Agent completed successfully.\n"
                    log_placeholder.markdown(
                        f'<div class="terminal-window">{log_content}</div>',
                        unsafe_allow_html=True
                    )
                    st.success("Agent completed successfully. Refreshing data...")
                    time.sleep(1.5)
                    st.rerun()
                else:
                    log_content += "\n[System] ✗ Agent exited with errors.\n"
                    log_placeholder.markdown(
                        f'<div class="terminal-window">{log_content}</div>',
                        unsafe_allow_html=True
                    )
                    st.error("Agent execution failed. Review the console output above.")

            except Exception as e:
                st.error(f"Execution Error: {e}")

    st.markdown('</div>', unsafe_allow_html=True)


def render_full_pipeline_console():

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🚀 Full AgentGravity Pipeline")

    if st.button("🚀 Run Full AgentGravity Pipeline", type="primary"):

        log_placeholder = st.empty()

        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        with st.spinner("Executing Full Pipeline..."):

            try:

                log_content = ""

                proc = subprocess.Popen(
                    [sys.executable, os.path.join(project_root, "main.py")],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    cwd=project_root
                )

                while True:

                    line = proc.stdout.readline()

                    if not line:
                        break

                    log_content += line

                    log_placeholder.markdown(
                        f'<div class="terminal-window">{log_content}</div>',
                        unsafe_allow_html=True
                    )

                proc.wait()

                if proc.returncode == 0:

                    st.success("Pipeline completed successfully!")

                    time.sleep(2)

                    st.rerun()

                else:

                    st.error("Pipeline failed. See logs above.")

            except Exception as e:

                st.error(str(e))

    st.markdown("</div>", unsafe_allow_html=True)
# ===========================================================
# SECTION 6 — SIDEBAR
# ===========================================================
st.sidebar.markdown("""
<div style="padding: 10px 0px 20px 0px;">
    <h1 style="font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 24px; color: #FFFFFF; margin: 0px;">
        ⚡ AgentGravity
    </h1>
    <p style="font-size: 11px; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 4px;">
        Enterprise Control Tower
    </p>
</div>
""", unsafe_allow_html=True)

# Connection status badge
if is_connected:
    st.sidebar.markdown("""
    <div style="background-color: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 8px; padding: 12px; margin-bottom: 25px;">
        <span style="color: #10B981; font-weight: 700; font-size: 12px;">● Snowflake Connected</span><br>
    </div>
    """, unsafe_allow_html=True)
else:
    st.sidebar.markdown(f"""
    <div style="background-color: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.2); border-radius: 8px; padding: 12px; margin-bottom: 25px;">
        <span style="color: #F87171; font-weight: 700; font-size: 12px;">● Snowflake Disconnected</span><br>
        <span style="font-size: 10px; color: #94A3B8;">Running in telemetry offline mode.</span>
    </div>
    """, unsafe_allow_html=True)

# Navigation — ordered to match the incident lifecycle workflow
NAVIGATION_PAGES = [
    "📤 Data Upload",
    "📈 Monitoring",
    "🔍 Root Cause Analysis",
    "💰 Business Impact",
    "👔 Executive Dashboard",
    "🛠 Recovery Strategy",
    "⚙ Operations Center",
]

page = st.sidebar.radio(
    "Navigation System",
    options=NAVIGATION_PAGES,
    label_visibility="collapsed"
)

st.sidebar.markdown(
    "<br><hr style='border-top: 1px solid rgba(255,255,255,0.05);'>"
    "<p style='font-size: 11px; font-weight: 600; color: #64748B; text-transform: uppercase;'>Incident Lifecycle</p>",
    unsafe_allow_html=True
)
st.sidebar.markdown("""
<div style="font-size: 11px; color: #475569; line-height: 2.0; padding: 0 4px;">
    📤 Ingest Data<br>
    ↓ 📈 Detect Anomalies<br>
    ↓ 🔍 Diagnose Causes<br>
    ↓ 💰 Estimate Impact<br>
    ↓ 🛠 Recover &amp; Mitigate<br>
    ↓ ⚙ Orchestrate Pipeline<br>
    ↓ 👔 Executive Briefing
</div>
""", unsafe_allow_html=True)

# ===========================================================
# SECTION 7 — SHARED STATE (pre-load all data)
# ===========================================================
df_kpis = load_kpi_data()
if not df_kpis.empty:

    df_kpis["HEALTH_SCORE"] = (
        df_kpis["REVENUE"].clip(upper=20000) / 20000 * 40
        + (100 - df_kpis["CHURN_RATE"] * 10).clip(lower=0) * 0.30
        + (df_kpis["INVENTORY"].clip(upper=500) / 500 * 100) * 0.30
    ).round(2)
df_incidents = load_incidents_data()
df_causes = load_root_causes_data()
df_impacts = load_impacts_data()

# Pre-calculate KPI deltas
latest_kpi = df_kpis.iloc[-1] if not df_kpis.empty else None
prev_kpi = df_kpis.iloc[-2] if len(df_kpis) > 1 else None

# ===========================================================
# SECTION 8 — PAGE ROUTER
# ===========================================================

# ----------------------------------------------------------
# PAGE 1 — 📤 Data Upload
# ----------------------------------------------------------
if page == "📤 Data Upload":
    st.markdown('<h1 class="gradient-title" style="margin-bottom: 5px;">Data Ingestion & Telemetry Upload</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #64748B; margin-bottom: 25px;">Upload business KPI metrics and validate telemetry schema before ingesting into Snowflake.</p>', unsafe_allow_html=True)

    if not is_connected:
        st.info("🔌 Snowflake connection offline. Configure Snowflake credentials in your `.env` file to enable database upload.")

    # — CSV Upload & Validation —
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 1. Upload Telemetry Dataset")
    st.write("Upload a CSV file containing historical business KPI telemetry. The file must conform to the required operational schema.")

    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file is not None:
        try:
            df_upload = pd.read_csv(uploaded_file)

            # Normalize column headers
            original_cols = list(df_upload.columns)
            df_upload.columns = [c.upper().strip() for c in df_upload.columns]

            required_cols = ["KPI_DATE", "REVENUE", "ORDERS", "CUSTOMERS", "INVENTORY", "CHURN_RATE"]
            missing_cols = [col for col in required_cols if col not in df_upload.columns]

            if missing_cols:
                st.error(f"❌ Column Validation Failed. Missing required columns: {', '.join(missing_cols)}")
                st.markdown("**Your CSV Columns:**")
                st.write(original_cols)
                st.markdown(f"**Required Columns:** `{', '.join(required_cols)}`")
            else:
                st.success("✅ Column Validation Passed. Telemetry schema is correct.")

                # — Dataset Preview —
                st.markdown("#### Preview Dataset (First 5 Rows)")
                st.dataframe(df_upload.head(5), use_container_width=True)

                st.markdown('</div>', unsafe_allow_html=True)

                # — Dataset Statistics —
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown("### 2. Dataset Statistics")

                df_upload["KPI_DATE"] = pd.to_datetime(df_upload["KPI_DATE"], errors="coerce")
                missing_vals = df_upload.isnull().sum().sum()
                date_min = df_upload["KPI_DATE"].min()
                date_max = df_upload["KPI_DATE"].max()

                stat_cols = st.columns(4)
                with stat_cols[0]:
                    render_kpi_card("Total Rows", f"{len(df_upload):,}", "Records to upload", True, border_color="#3B82F6")
                with stat_cols[1]:
                    render_kpi_card("Columns", f"{len(df_upload.columns)}", "Schema fields", True, border_color="#8B5CF6")
                with stat_cols[2]:
                    render_kpi_card("Missing Values", f"{missing_vals}", "Null cells detected", missing_vals == 0, border_color="#F59E0B" if missing_vals > 0 else "#10B981")
                with stat_cols[3]:
                    date_range_str = f"{date_min.strftime('%b %d, %Y')} – {date_max.strftime('%b %d, %Y')}" if pd.notna(date_min) and pd.notna(date_max) else "N/A"
                    render_kpi_card("Date Range", date_range_str, "Telemetry window", True, border_color="#10B981")

                st.markdown('</div>', unsafe_allow_html=True)

                # — Snowflake Upload —
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown("### 3. Upload to Snowflake")
                truncate_option = st.checkbox("Replace existing data (truncate BUSINESS.KPI_METRICS before uploading)", value=True)

                if st.button("📤 Upload to Snowflake", type="primary"):
                    if not is_connected:
                        st.error("Cannot upload: Snowflake connection is offline.")
                    else:
                        with st.spinner("Uploading to Snowflake..."):
                            success, result = upload_kpis_to_snowflake(df_upload, truncate=truncate_option)
                            if success:
                                st.success(f"🎉 Successfully uploaded {result:,} records to Snowflake BUSINESS.KPI_METRICS!")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error(f"Upload failed: {result}")

        except Exception as e:
            st.error(f"Error reading uploaded file: {e}")

        finally:
            # Close the upload section if we didn't already close it after stats
            if uploaded_file is not None:
                try:
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception:
                    pass
    else:
        st.markdown('</div>', unsafe_allow_html=True)


# ----------------------------------------------------------
# PAGE 2 — 📈 Monitoring
# ----------------------------------------------------------
elif page == "📈 Monitoring":
    st.markdown('<h1 class="gradient-title" style="margin-bottom: 5px;">Business Metrics & Incident Monitoring</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #64748B; margin-bottom: 25px;">Real-time business telemetry trends and detected incident registry.</p>', unsafe_allow_html=True)

    # — Filters —
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    fcols = st.columns(4)

    unique_types = ["All"] + list(df_incidents["INCIDENT_TYPE"].unique()) if not df_incidents.empty else ["All"]
    unique_sevs = ["All"] + list(df_incidents["SEVERITY"].unique()) if not df_incidents.empty else ["All"]
    unique_stats = ["All"] + list(df_incidents["STATUS"].unique()) if not df_incidents.empty else ["All"]

    with fcols[0]:
        sel_type = st.selectbox("Incident Type", unique_types)
    with fcols[1]:
        sel_sev = st.selectbox("Severity", unique_sevs)
    with fcols[2]:
        sel_stat = st.selectbox("Status", unique_stats)
    with fcols[3]:
        search_desc = st.text_input("Search Description", "")

    st.markdown('</div>', unsafe_allow_html=True)

    # Apply filters
    filtered_df = df_incidents.copy() if not df_incidents.empty else pd.DataFrame()
    if not filtered_df.empty:
        if sel_type != "All":
            filtered_df = filtered_df[filtered_df["INCIDENT_TYPE"] == sel_type]
        if sel_sev != "All":
            filtered_df = filtered_df[filtered_df["SEVERITY"] == sel_sev]
        if sel_stat != "All":
            filtered_df = filtered_df[filtered_df["STATUS"] == sel_stat]
        if search_desc:
            filtered_df = filtered_df[filtered_df["DESCRIPTION"].str.contains(search_desc, case=False, na=False)]

    # — Telemetry Trend Chart —
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### Telemetry Trend & Operational Benchmarks")

    metric_choice = st.segmented_control("Telemetry Metric", ["Revenue", "Churn Rate", "Inventory Level"], default="Revenue")

    if not df_kpis.empty:
        if metric_choice == "Revenue":
            y_col, y_label, color = "REVENUE", "Revenue ($)", "#3B82F6"
        elif metric_choice == "Churn Rate":
            y_col, y_label, color = "CHURN_RATE", "Churn Rate (%)", "#F59E0B"
        else:
            y_col, y_label, color = "INVENTORY", "Inventory Units", "#8B5CF6"

        fig = px.line(df_kpis, x="KPI_DATE", y=y_col, labels={y_col: y_label, "KPI_DATE": "Date"})
        fig.update_traces(line=dict(color=color, width=2.5))

        # Overlay incident markers
        if not df_incidents.empty:
            if metric_choice == "Revenue":
                target_types = ["Revenue Drop"]
            elif metric_choice == "Churn Rate":
                target_types = ["High Churn"]
            else:
                target_types = ["Inventory Risk"]

            inc_points = df_incidents[df_incidents["INCIDENT_TYPE"].isin(target_types)]
            if not inc_points.empty and "KPI_DATE" in inc_points.columns:
                inc_pts = inc_points.dropna(subset=[y_col])
                fig.add_trace(go.Scatter(
                    x=inc_pts["KPI_DATE"],
                    y=inc_pts[y_col],
                    mode='markers',
                    marker=dict(size=12, color='#EF4444', symbol='x-open'),
                    name='Incident Alert',
                    hovertext=inc_pts["DESCRIPTION"]
                ))

        apply_plotly_theme(fig, height=350)
        st.plotly_chart(fig, use_container_width=True)
    else:
        render_empty_state("📉", "No Telemetry Data", "Upload a dataset on the Data Upload page to begin monitoring.")

    st.markdown('</div>', unsafe_allow_html=True)

    # — Incident Registry —
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### Incident Registry Log")
    if not filtered_df.empty:
        display_df = filtered_df[["INCIDENT_ID", "INCIDENT_DATE", "INCIDENT_TYPE", "SEVERITY", "STATUS", "DESCRIPTION"]].copy()
        st.dataframe(
            display_df,
            column_config={
                "INCIDENT_ID": "ID",
                "INCIDENT_DATE": "Timestamp",
                "INCIDENT_TYPE": "Incident Type",
                "SEVERITY": st.column_config.TextColumn("Severity"),
                "STATUS": "Status",
                "DESCRIPTION": "Incident Description",
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        render_empty_state("🔎", "No Incidents Found", "No incidents match the selected filters, or no incidents have been detected yet.")

    st.markdown('</div>', unsafe_allow_html=True)

    # — Run Monitoring Agent (isolated) —
    render_agent_console(
        script_path="agents/monitoring_agent.py",
        button_label="📈 Run Monitoring Agent",
        spinner_msg="Running Monitoring Agent...",
        section_title="Run Monitoring Agent"
    )


# ----------------------------------------------------------
# PAGE 3 — 🔍 Root Cause Analysis
# ----------------------------------------------------------
elif page == "🔍 Root Cause Analysis":
    st.markdown('<h1 class="gradient-title" style="margin-bottom: 5px;">Root Cause Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #64748B; margin-bottom: 25px;">Investigate diagnosed drivers of KPI anomalies and confidence-scored root cause mappings.</p>', unsafe_allow_html=True)

    if not is_connected:
        st.info("ℹ️ Root Cause Analysis requires an active Snowflake connection. Configure credentials in `.env` to enable data loading.")

    # — Summary KPIs —
    avg_conf = df_causes["CONFIDENCE_SCORE"].mean() if not df_causes.empty else 0
    top_cause = df_causes["CAUSE_NAME"].mode().iloc[0] if not df_causes.empty and len(df_causes["CAUSE_NAME"].mode()) > 0 else "N/A"

    cols = st.columns(3)
    with cols[0]:
        render_kpi_card("Identified Root Causes", f"{len(df_causes)}", "Active diagnoses", True, border_color="#8B5CF6")
    with cols[1]:
        render_kpi_card("Average Confidence", f"{avg_conf:.1%}" if avg_conf else "0%", "AI diagnostic accuracy", True, border_color="#10B981")
    with cols[2]:
        render_kpi_card("Primary Diagnostic Cause", f"{top_cause}", "Highest frequency anomaly", True, border_color="#F59E0B")

    # — Charts Row —
    row2 = st.columns([5, 7])

    with row2[0]:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### Root Cause Distribution")
        if not df_causes.empty:
            dist_df = df_causes["CAUSE_NAME"].value_counts().reset_index()
            dist_df.columns = ["Cause Name", "Count"]
            fig = px.pie(
                dist_df,
                names="Cause Name",
                values="Count",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            apply_plotly_theme(fig, height=320)
            st.plotly_chart(fig, use_container_width=True)
        else:
            render_empty_state("🔍", "No Root Cause Data", "Run the Root Cause Agent to populate diagnostic data.")
        st.markdown('</div>', unsafe_allow_html=True)

    with row2[1]:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### Diagnostic Confidence by Incident")
        if not df_causes.empty and "INCIDENT_TYPE" in df_causes.columns:
            fig = px.scatter(
                df_causes,
                x="INCIDENT_DATE",
                y="CONFIDENCE_SCORE",
                color="CAUSE_NAME",
                size="CONFIDENCE_SCORE",
                hover_data=["INCIDENT_TYPE", "DESCRIPTION"],
                labels={"CONFIDENCE_SCORE": "Confidence Score", "INCIDENT_DATE": "Analysis Date"},
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            apply_plotly_theme(fig, height=320)
            st.plotly_chart(fig, use_container_width=True)
        else:
            render_empty_state("📊", "No Diagnostic Data", "Incident mapping unavailable. Run the Root Cause Agent first.")
        st.markdown('</div>', unsafe_allow_html=True)

    # — Confidence Histogram —
    if not df_causes.empty:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### Confidence Score Distribution")
        fig_hist = px.histogram(
            df_causes,
            x="CONFIDENCE_SCORE",
            nbins=20,
            color_discrete_sequence=["#8B5CF6"],
            labels={"CONFIDENCE_SCORE": "Confidence Score"}
        )
        apply_plotly_theme(fig_hist, height=280)
        st.plotly_chart(fig_hist, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # — Root Cause Registry Table —
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### Root Cause Registry")
    if not df_causes.empty:
        display_causes = df_causes.copy()
        if "INCIDENT_TYPE" in display_causes.columns:
            cols_to_show = [c for c in ["ROOT_CAUSE_ID", "INCIDENT_ID", "INCIDENT_TYPE", "CAUSE_NAME", "CONFIDENCE_SCORE", "STATUS"] if c in display_causes.columns]
        else:
            cols_to_show = [c for c in ["ROOT_CAUSE_ID", "INCIDENT_ID", "CAUSE_NAME", "CONFIDENCE_SCORE"] if c in display_causes.columns]
        display_causes = display_causes[cols_to_show].copy()
        display_causes["CONFIDENCE_SCORE"] = display_causes["CONFIDENCE_SCORE"].apply(lambda x: f"{x:.1%}")
        st.dataframe(
            display_causes,
            column_config={
                "ROOT_CAUSE_ID": "ID",
                "INCIDENT_ID": "Incident ID",
                "INCIDENT_TYPE": "Incident Type",
                "CAUSE_NAME": "Identified Cause",
                "CONFIDENCE_SCORE": "Confidence Score",
                "STATUS": "Incident Status"
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        render_empty_state("📋", "No Root Causes Found", "Execute the Root Cause Agent to populate the registry.")
    st.markdown('</div>', unsafe_allow_html=True)

    # — Run Root Cause Agent (isolated) —
    render_agent_console(
        script_path="agents/root_cause_agent.py",
        button_label="🔍 Run Root Cause Agent",
        spinner_msg="Running Root Cause Agent...",
        section_title="Run Root Cause Agent"
    )


# ----------------------------------------------------------
# PAGE 4 — 💰 Business Impact
# ----------------------------------------------------------
elif page == "💰 Business Impact":
    st.markdown('<h1 class="gradient-title" style="margin-bottom: 5px;">Business Impact</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #64748B; margin-bottom: 25px;">Financial loss evaluations, risk severity distributions, and incident cost register.</p>', unsafe_allow_html=True)

    # — KPI Summary Row —
    total_loss = df_impacts["ESTIMATED_REVENUE_LOSS"].sum() if not df_impacts.empty else 0
    avg_loss = df_impacts["ESTIMATED_REVENUE_LOSS"].mean() if not df_impacts.empty else 0
    max_loss = df_impacts["ESTIMATED_REVENUE_LOSS"].max() if not df_impacts.empty else 0

    cols = st.columns(3)
    with cols[0]:
        render_kpi_card("Total Revenue Loss", f"${total_loss:,.2f}", "Estimated financial impact", False, border_color="#EF4444")
    with cols[1]:
        render_kpi_card("Average Loss / Incident", f"${avg_loss:,.2f}", "Financial footprint per anomaly", False, border_color="#F59E0B")
    with cols[2]:
        render_kpi_card("Peak Financial Loss", f"${max_loss:,.2f}", "Maximum single event impact", False, border_color="#3B82F6")

    # — Charts Row —
    row2 = st.columns([5, 7])

    with row2[0]:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### Business Severity Distribution")
        if not df_impacts.empty:
            sev_counts = df_impacts["BUSINESS_SEVERITY"].value_counts().reset_index()
            sev_counts.columns = ["Business Severity", "Count"]
            fig = px.pie(
                sev_counts,
                names="Business Severity",
                values="Count",
                hole=0.4,
                color="Business Severity",
                color_discrete_map={
                    "CRITICAL": "#EF4444",
                    "HIGH": "#F97316",
                    "MEDIUM": "#F59E0B",
                    "LOW": "#10B981"
                }
            )
            apply_plotly_theme(fig, height=320)
            st.plotly_chart(fig, use_container_width=True)
        else:
            render_empty_state("📊", "No Impact Data", "Run the Business Impact Agent to generate severity analysis.")
        st.markdown('</div>', unsafe_allow_html=True)

    with row2[1]:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### Top Incidents by Estimated Revenue Loss")
        if not df_impacts.empty:
            top_losses = df_impacts.sort_values(by="ESTIMATED_REVENUE_LOSS", ascending=False).head(10)
            fig = px.bar(
                top_losses,
                y="ESTIMATED_REVENUE_LOSS",
                x="INCIDENT_ID",
                color="BUSINESS_SEVERITY",
                labels={"ESTIMATED_REVENUE_LOSS": "Loss ($)", "INCIDENT_ID": "Incident ID"},
                color_discrete_map={
                    "CRITICAL": "#EF4444",
                    "HIGH": "#F97316",
                    "MEDIUM": "#F59E0B",
                    "LOW": "#10B981"
                }
            )
            apply_plotly_theme(fig, height=320)
            st.plotly_chart(fig, use_container_width=True)
        else:
            render_empty_state("📉", "No Loss Data", "Run the Business Impact Agent to compute incident loss estimates.")
        st.markdown('</div>', unsafe_allow_html=True)

    # — Financial Impact Register —
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### Financial Impact Register")
    if not df_impacts.empty:
        display_impacts = df_impacts.copy()
        display_impacts["ESTIMATED_REVENUE_LOSS"] = display_impacts["ESTIMATED_REVENUE_LOSS"].apply(lambda x: f"${x:,.2f}")
        cols_to_show = [c for c in ["IMPACT_ID", "INCIDENT_ID", "INCIDENT_TYPE", "ESTIMATED_REVENUE_LOSS", "BUSINESS_SEVERITY", "STATUS"] if c in display_impacts.columns]
        st.dataframe(
            display_impacts[cols_to_show],
            column_config={
                "IMPACT_ID": "ID",
                "INCIDENT_ID": "Incident ID",
                "INCIDENT_TYPE": "Incident Type",
                "ESTIMATED_REVENUE_LOSS": "Estimated Loss",
                "BUSINESS_SEVERITY": "Severity Flag",
                "STATUS": "Incident Status"
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        render_empty_state("📋", "No Impact Records", "No financial assessments found in Snowflake.")
    st.markdown('</div>', unsafe_allow_html=True)

    # — Run Business Impact Agent (isolated) —
    render_agent_console(
        script_path="agents/impact_agent.py",
        button_label="💰 Run Business Impact Agent",
        spinner_msg="Running Business Impact Agent...",
        section_title="Run Business Impact Agent"
    )

# ----------------------------------------------------------
# PAGE 5 — 👔 Executive Dashboard (READ ONLY)
# ----------------------------------------------------------
elif page == "👔 Executive Dashboard":
    st.markdown('<h1 class="gradient-title" style="margin-bottom: 5px;">Executive Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #64748B; margin-bottom: 25px;">Strategic operational briefing — business intelligence summary for executive review.</p>', unsafe_allow_html=True)

    if not is_connected:
        st.info("🔌 Snowflake connection offline. Showing local telemetry metrics. Configure Snowflake credentials in `.env` to enable full database query mode.")

    if not df_incidents.empty:
        open_count = len(df_incidents[df_incidents["STATUS"] == "OPEN"])
    else:
        open_count = 0
        
    # — Top KPI Row —
    cols = st.columns(4)
    
    if latest_kpi is not None:
        latest_kpi = df_kpis.iloc[-1]
        
        # Previous KPI row
        prev_kpi = df_kpis.iloc[-2] if len(df_kpis) > 1 else None

        # Business Health Score
        current_health = latest_kpi["HEALTH_SCORE"]

        prev_health = (
            prev_kpi["HEALTH_SCORE"]
            if prev_kpi is not None
            else current_health
        )

        health_delta = round(current_health - prev_health, 2)

        with cols[0]:
            render_kpi_card(
                "Business Health Index",
                f"{current_health}%",
                f"{health_delta:+.2f}% vs prev day",
                health_delta >= 0,
                border_color="#10B981"
            )

        current_rev = latest_kpi["REVENUE"]
        prev_rev = prev_kpi["REVENUE"] if prev_kpi is not None else current_rev
        rev_delta = round(((current_rev - prev_rev) / prev_rev) * 100, 2) if prev_rev else 0

        with cols[1]:
            render_kpi_card(
                "Latest Revenue",
                f"${current_rev:,.2f}",
                f"{rev_delta:+.2f}% vs prev day",
                rev_delta >= 0,
                border_color="#3B82F6"
            )

        current_churn = latest_kpi["CHURN_RATE"]
        prev_churn = prev_kpi["CHURN_RATE"] if prev_kpi is not None else current_churn
        churn_delta = round(current_churn - prev_churn, 2)

        with cols[2]:
            render_kpi_card(
                "Churn Rate",
                f"{current_churn:.1f}%",
            f"{churn_delta:+.2f}% vs prev day",
            churn_delta <= 0,
            border_color="#F59E0B"
        )

        with cols[3]:
            render_kpi_card(
                "Active Open Incidents",
                f"{open_count}",
                "Requires investigation" if open_count > 0 else "All cleared",
                open_count == 0,
                border_color="#EF4444"
        )

    else:
        render_empty_state(
        "📊",
        "No KPI Data Available",
        "Upload telemetry data via the Data Upload page to populate the executive dashboard."
    )

    # — Business Health Score & Gauge —
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### Business Health Score")

    health_gauge_cols = st.columns([4, 6])

    with health_gauge_cols[0]:
        if latest_kpi is not None:
            health_val = current_health

            # Determine health tier
            if health_val >= 75:
                health_color = "#10B981"
                health_tier = "🟢 HEALTHY"
                health_msg = "Business operations are performing within acceptable thresholds."
            elif health_val >= 50:
                health_color = "#F59E0B"
                health_tier = "🟡 AT RISK"
                health_msg = "Some KPIs are trending negatively. Monitor closely."
            else:
                health_color = "#EF4444"
                health_tier = "🔴 CRITICAL"
                health_msg = "Multiple KPIs below threshold. Immediate action required."

            # Gauge chart
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=health_val,
                number={'suffix': '%', 'font': {'size': 36, 'color': '#FFFFFF', 'family': 'Outfit'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': '#64748B', 'tickfont': {'color': '#64748B'}},
                    'bar': {'color': health_color, 'thickness': 0.25},
                    'bgcolor': 'rgba(0,0,0,0)',
                    'borderwidth': 0,
                    'steps': [
                        {'range': [0, 50], 'color': 'rgba(239,68,68,0.08)'},
                        {'range': [50, 75], 'color': 'rgba(245,158,11,0.08)'},
                        {'range': [75, 100], 'color': 'rgba(16,185,129,0.08)'},
                    ],
                    'threshold': {
                        'line': {'color': health_color, 'width': 3},
                        'thickness': 0.75,
                        'value': health_val
                    }
                }
            ))
            fig_gauge.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#94A3B8',
                height=260,
                margin=dict(l=10, r=10, t=20, b=10)
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

            st.markdown(f"<div style='text-align:center; font-family: Outfit, sans-serif; font-size: 16px; font-weight: 700; color: {health_color}; margin-top: -10px;'>{health_tier}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align:center; font-size: 12px; color: #64748B; margin-top: 8px;'>{health_msg}</div>", unsafe_allow_html=True)
        else:
            render_empty_state("🩺", "Health Score Unavailable", "Upload KPI data to compute business health.")

    with health_gauge_cols[1]:
        st.markdown("#### Health Score Breakdown")
        st.markdown("""
        <div style="font-size: 13px; color: #94A3B8; line-height: 2.0; margin-top: 10px;">
            <div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.04); padding: 8px 0;">
                <span>Revenue Component</span><span style="color: #3B82F6; font-weight: 600;">Weight: 40%</span>
            </div>
            <div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.04); padding: 8px 0;">
                <span>Churn Rate Component</span><span style="color: #F59E0B; font-weight: 600;">Weight: 30%</span>
            </div>
            <div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.04); padding: 8px 0;">
                <span>Inventory Component</span><span style="color: #8B5CF6; font-weight: 600;">Weight: 30%</span>
            </div>
        </div>
        <div style="margin-top: 20px; font-size: 12px; color: #64748B;">
            <div style="margin-bottom: 8px;"><span style="color: #10B981; font-weight: 700;">● HEALTHY</span> — Score ≥ 75%</div>
            <div style="margin-bottom: 8px;"><span style="color: #F59E0B; font-weight: 700;">● AT RISK</span> — Score 50–74%</div>
            <div><span style="color: #EF4444; font-weight: 700;">● CRITICAL</span> — Score &lt; 50%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # — Main Body Panels —
    row2_cols = st.columns([7, 5])

    with row2_cols[0]:
        # Health Trend
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### Business Health Index Trend")
        if not df_kpis.empty:
            fig = px.line(
                df_kpis.tail(30),
                x="KPI_DATE",
                y="HEALTH_SCORE",
                labels={"HEALTH_SCORE": "Health Score (%)", "KPI_DATE": "Date"},
                color_discrete_sequence=["#10B981"]
            )
            fig.update_traces(line=dict(width=3))
            apply_plotly_theme(fig, height=320)
            st.plotly_chart(fig, use_container_width=True)
        else:
            render_empty_state("📈", "No Trend Data", "Upload KPI telemetry to view the health trend chart.")
        st.markdown('</div>', unsafe_allow_html=True)

        # Executive AI Report
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### Latest Executive Report & Strategic Briefing")
        df_reports = load_executive_reports()
        if not df_reports.empty:
            report_text = df_reports.iloc[0]["EXECUTIVE_SUMMARY"]
            priority = df_reports.iloc[0]["BUSINESS_PRIORITY"]
            created = df_reports.iloc[0]["CREATED_AT"]

            p_badge = render_pill(priority)
            st.markdown(f"**Briefing Generated:** {created} | **Priority:** {p_badge}", unsafe_allow_html=True)

            parsed = parse_executive_report(report_text)

            tabs = st.tabs(["Summary", "Risks", "Impact", "Actions"])
            with tabs[0]:
                st.markdown(f'<div class="briefing-box"><div class="briefing-title">Executive Summary</div>{parsed["Executive Summary"]}</div>', unsafe_allow_html=True)
            with tabs[1]:
                st.markdown(f'<div class="briefing-box"><div class="briefing-title">Top Business Risks</div>{parsed["Top Business Risks"]}</div>', unsafe_allow_html=True)
            with tabs[2]:
                st.markdown(f'<div class="briefing-box"><div class="briefing-title">Business Impact</div>{parsed["Business Impact"]}</div>', unsafe_allow_html=True)
            with tabs[3]:
                st.markdown(f'<div class="briefing-box"><div class="briefing-title">Recommended Actions</div>{parsed["Recommended Actions"]}</div>', unsafe_allow_html=True)
        else:
            st.info("ℹ️ No executive report found. Run the full pipeline from the **Operations Center** to auto-generate AI-powered executive briefings.")
        st.markdown('</div>', unsafe_allow_html=True)

        # Revenue Trend
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### Revenue & Churn Trend (30-Day)")
        if not df_kpis.empty:
            fig_rev = px.line(
                df_kpis.tail(30),
                x="KPI_DATE",
                y=["REVENUE", "CHURN_RATE"],
                labels={"value": "Value", "KPI_DATE": "Date", "variable": "Metric"},
                color_discrete_map={"REVENUE": "#3B82F6", "CHURN_RATE": "#F59E0B"}
            )
            fig_rev.update_traces(line=dict(width=2))
            apply_plotly_theme(fig_rev, height=280)
            st.plotly_chart(fig_rev, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with row2_cols[1]:
        # Active Alert Queue
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### Active Alert Incident Queue")

        open_incidents = df_incidents[df_incidents["STATUS"] == "OPEN"] if not df_incidents.empty else pd.DataFrame()
        if not open_incidents.empty:
            for _, inc in open_incidents.head(5).iterrows():
                pill_html = render_pill(inc["SEVERITY"])
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.015); border: 1px solid rgba(255,255,255,0.04); border-radius: 8px; padding: 12px; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 700; color: #FFFFFF; font-size: 13px;">Incident #{inc['INCIDENT_ID']}: {inc['INCIDENT_TYPE']}</span>
                        {pill_html}
                    </div>
                    <div style="font-size: 12px; color: #94A3B8; margin-top: 6px;">{inc['DESCRIPTION']}</div>
                    <div style="font-size: 10px; color: #64748B; margin-top: 4px;">Detected: {inc['INCIDENT_DATE']}</div>
                </div>
                """, unsafe_allow_html=True)

            if len(open_incidents) > 5:
                st.markdown(f"<p style='font-size:12px; color:#64748B; text-align:center;'>+ {len(open_incidents) - 5} more open incidents. View full registry in Monitoring.</p>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 40px 20px;">
                <span style="font-size: 40px;">🟢</span>
                <h4 style="color: #FFFFFF; margin-top: 15px;">All Systems Normal</h4>
                <p style="font-size: 12px; color: #64748B;">No active open incidents detected by the Monitoring Agent.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Financial Impact Summary
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### Financial Impact Summary")
        if not df_impacts.empty:
            total_loss_exec = df_impacts["ESTIMATED_REVENUE_LOSS"].sum()
            critical_count = len(df_impacts[df_impacts["BUSINESS_SEVERITY"] == "CRITICAL"]) if "BUSINESS_SEVERITY" in df_impacts.columns else 0

            st.markdown(f"""
            <div style="padding: 10px 0;">
                <div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.04); padding: 10px 0; font-size: 13px;">
                    <span style="color: #94A3B8;">Total Estimated Loss</span>
                    <span style="color: #EF4444; font-weight: 700;">${total_loss_exec:,.2f}</span>
                </div>
                <div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.04); padding: 10px 0; font-size: 13px;">
                    <span style="color: #94A3B8;">Total Incidents Assessed</span>
                    <span style="color: #FFFFFF; font-weight: 700;">{len(df_impacts)}</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 10px 0; font-size: 13px;">
                    <span style="color: #94A3B8;">Critical Severity Events</span>
                    <span style="color: #F87171; font-weight: 700;">{critical_count}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.caption("No financial impact data available.")
        st.markdown('</div>', unsafe_allow_html=True)

        # Recovery Strategy Summary
        df_plan_exec = load_recovery_plan()
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### Recovery Strategy Status")
        if not df_plan_exec.empty:
            plan_exec = df_plan_exec.iloc[0]
            risk_badge = render_pill(plan_exec["RISK_LEVEL"])
            st.markdown(f"**Risk Level:** {risk_badge}", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:12px; color:#94A3B8; margin-top:10px; line-height:1.6;'>{str(plan_exec['EXECUTIVE_SUMMARY'])[:280]}...</p>", unsafe_allow_html=True)
            st.markdown(f"<span style='font-size:10px; color:#64748B;'>Generated: {plan_exec['GENERATED_AT']}</span>", unsafe_allow_html=True)
        else:
            st.caption("No recovery plan generated. Run the full pipeline in Operations Center.")
        st.markdown('</div>', unsafe_allow_html=True)

        # Recent Agent Activity
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### Recent Agent Activity")
        df_logs = load_audit_logs()
        if not df_logs.empty:
            for _, log in df_logs.head(5).iterrows():
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.03); padding: 8px 0px;">
                    <div>
                        <div style="font-size: 12px; font-weight: 600; color: #FFFFFF;">{log['AGENT_NAME']}</div>
                        <div style="font-size: 11px; color: #94A3B8;">{log['ACTION_PERFORMED']}</div>
                    </div>
                    <div style="font-size: 11px; color: #64748B; text-align: right;">{log['EXECUTION_TIME']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("No agent activity logged yet.")
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------------
# PAGE 6 — 🛠 Recovery Strategy
# ----------------------------------------------------------
elif page == "🛠 Recovery Strategy":
    st.markdown('<h1 class="gradient-title" style="margin-bottom: 5px;">Recovery Strategy</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #64748B; margin-bottom: 25px;">Executive mitigation playbooks and recovery orchestrations generated by AI agents.</p>', unsafe_allow_html=True)

    df_plan = load_recovery_plan()

    if not df_plan.empty:
        plan_row = df_plan.iloc[0]

        # Risk badge & date header
        risk_pill = render_pill(plan_row["RISK_LEVEL"])
        st.markdown(f"**Orchestration Risk Factor:** {risk_pill} | **Generated At:** {plan_row['GENERATED_AT']}", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Executive Summary
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### Executive Plan Summary")
        st.markdown(f"<p style='font-size:15px; line-height:1.6; color:#E2E8F0;'>{plan_row['EXECUTIVE_SUMMARY']}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Action Playbooks (3-column grid)
        cols = st.columns(3)
        with cols[0]:
            st.markdown('<div class="glass-card" style="min-height: 250px;">', unsafe_allow_html=True)
            st.markdown("### 🔴 Immediate Action Playbook")
            st.markdown(f"<p style='font-size:13px; line-height:1.6;'>{plan_row['IMMEDIATE_ACTIONS']}</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with cols[1]:
            st.markdown('<div class="glass-card" style="min-height: 250px;">', unsafe_allow_html=True)
            st.markdown("### 🟡 Short-Term Stabilizations")
            st.markdown(f"<p style='font-size:13px; line-height:1.6;'>{plan_row['SHORT_TERM_ACTIONS']}</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with cols[2]:
            st.markdown('<div class="glass-card" style="min-height: 250px;">', unsafe_allow_html=True)
            st.markdown("### 🟢 Long-Term Preventions")
            st.markdown(f"<p style='font-size:13px; line-height:1.6;'>{plan_row['LONG_TERM_ACTIONS']}</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Outcomes & Metrics (2-column grid)
        cols2 = st.columns(2)
        with cols2[0]:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### Expected Outcomes")
            st.markdown(f"<p style='font-size:14px; line-height:1.6; color:#A7F3D0;'>{plan_row['EXPECTED_BUSINESS_OUTCOME']}</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with cols2[1]:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### Success Metric Benchmarks")
            st.markdown(f"<p style='font-size:14px; line-height:1.6; color:#93C5FD;'>{plan_row['SUCCESS_METRICS']}</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        render_empty_state("🛠", "No Recovery Plan Generated", "Run the Recovery Agent below to formulate an AI-powered mitigation strategy.")

    # — Run Recovery Agent (isolated) —
    render_agent_console(
        script_path="agents/recovery_agent.py",
        button_label="⚡ Run Recovery Agent",
        spinner_msg="Invoking Gemini Recovery Agent...",
        section_title="Recovery Plan Orchestration"
    )


# ----------------------------------------------------------
# PAGE 7 — ⚙ Operations Center
# ----------------------------------------------------------
elif page == "⚙ Operations Center":
    st.markdown('<h1 class="gradient-title" style="margin-bottom: 5px;">Operations Center</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #64748B; margin-bottom: 25px;">AI agent control room — pipeline orchestration, system telemetry, and database health monitoring.</p>', unsafe_allow_html=True)

    # — Status Row —
    status_cols = st.columns(3)

    with status_cols[0]:
        if is_connected:
            render_kpi_card("Snowflake Status", "● Connected", "Database online", True, border_color="#10B981")
        else:
            render_kpi_card("Snowflake Status", "● Offline", "Check .env credentials", False, border_color="#EF4444")

    open_count = len(df_incidents[df_incidents["STATUS"] == "OPEN"]) if not df_incidents.empty else 0
    with status_cols[1]:
        render_kpi_card("Open Incidents", f"{open_count}", "Require investigation" if open_count > 0 else "All cleared", open_count == 0, border_color="#F59E0B" if open_count > 0 else "#10B981")

    total_causes = len(df_causes)
    with status_cols[2]:
        render_kpi_card("Root Causes Diagnosed", f"{total_causes}", "Identified anomaly drivers", True, border_color="#8B5CF6")

    # — Agent Registry —
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### Agent Registry")

    agents_registry = [
        {"icon": "📈", "name": "Monitoring Agent", "role": "KPI anomaly detection & incident logging", "script": "agents/monitoring_agent.py"},
        {"icon": "🔍", "name": "Root Cause Agent", "role": "Diagnostic cause identification & confidence scoring", "script": "agents/root_cause_agent.py"},
        {"icon": "💰", "name": "Business Impact Agent", "role": "Financial revenue loss estimation & severity classification", "script": "agents/impact_agent.py"},
        {"icon": "📋", "name": "Executive Agent", "role": "Gemini-powered McKinsey-style executive report generation", "script": "agents/executive_agent.py"},
        {"icon": "🛠", "name": "Recovery Agent", "role": "AI mitigation strategy & recovery plan formulation", "script": "agents/recovery_agent.py"},
    ]

    for agent in agents_registry:
        st.markdown(f"""
        <div class="agent-card">
            <div>
                <div class="agent-name">{agent['icon']} {agent['name']}</div>
                <div class="agent-role">{agent['role']}</div>
            </div>
            <div style="font-size: 11px; color: #475569; font-family: monospace;">{agent['script']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # — Database Table Telemetry —
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### Snowflake Database Telemetry")

    if is_connected:
        try:
            conn = get_connection()
            cursor = conn.cursor()

            tables = [
                ("BUSINESS.KPI_METRICS", "Historical and current KPI telemetry"),
                ("INCIDENTS.INCIDENTS", "Logged system and business health anomalies"),
                ("INCIDENTS.ROOT_CAUSES", "Diagnosed causes mapped to incidents"),
                ("INCIDENTS.IMPACT_ANALYSIS", "Assessments of financial revenue loss"),
                ("INCIDENTS.RECOVERY_PLAN", "Generated mitigation actions and risk playbooks"),
                ("INCIDENTS.EXECUTIVE_REPORTS", "McKinsey consulting reports generated by Gemini"),
                ("SECURITY.AGENT_AUDIT_LOG", "Background administrative execution audit trails"),
            ]

            row_data = []
            for t_name, desc in tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM AGENTGRAVITY.{t_name}")
                    cnt = cursor.fetchone()[0]
                    row_data.append({"Table Name": t_name, "Row Count": cnt, "Description": desc})
                except Exception as ex:
                    row_data.append({"Table Name": t_name, "Row Count": "Error", "Description": f"Query failed: {ex}"})

            cursor.close()
            conn.close()

            st.dataframe(pd.DataFrame(row_data), hide_index=True, use_container_width=True)

        except Exception as e:
            st.error(f"Error querying Snowflake metadata: {e}")
    else:
        st.warning("🔌 Snowflake Offline. Row counts unavailable. Configure credentials in `.env` to enable telemetry.")

    st.markdown('</div>', unsafe_allow_html=True)

    # — Audit Logs —
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### Agent Audit Log")
    df_logs_all = load_audit_logs()
    if not df_logs_all.empty:
        st.dataframe(
            df_logs_all,
            column_config={
                "LOG_ID": "Log ID",
                "AGENT_NAME": "Agent Name",
                "ACTION_PERFORMED": "Action Performed",
                "EXECUTION_TIME": "Execution Timestamp"
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        render_empty_state("📋", "No Audit Logs Found", "Agent activity logs will appear here after agents have been executed.")
    st.markdown('</div>', unsafe_allow_html=True)

    # — Full Pipeline (the ONLY place in the dashboard that runs the full pipeline) —
    render_full_pipeline_console()

# ===========================================================
# SECTION 9 — FOOTER
# ===========================================================
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
st.markdown(f"""
<div style="text-align: center; margin-top: 50px; padding: 20px; border-top: 1px solid rgba(255,255,255,0.05);">
    <p style="font-size: 11px; color: #64748B;">
        AgentGravity Command Center Platform | AI Operations Intelligence | {current_time}
    </p>
</div>
""", unsafe_allow_html=True)
