import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import date

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="Sirius | Enterprise Customer Intelligence",
    page_icon="⚡",
    layout="wide"
)

TODAY = date(2026, 9, 8)  # "Data as of" reference point

# =============================================================================
# STYLING
# =============================================================================
st.markdown("""
    <style>
    .sirius-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        color: #FFFFFF;
        padding: 20px 24px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
    }
    .sirius-title { font-size: 2.2rem; font-weight: 800; color: #38BDF8; margin: 0; }
    .sirius-subtitle { font-size: 0.95rem; color: #94A3B8; margin-top: 4px; }
    .sirius-asof { font-size: 0.8rem; color: #64748B; text-align: right; }

    .overview-card, .card-box {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 14px 18px;
        height: 100%;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .card-box { padding: 18px; margin-bottom: 15px; height: auto; }
    .overview-label { font-size: 0.8rem; color: #64748B; font-weight: 600; text-transform: uppercase; margin-bottom: 6px; }
    .overview-value { font-size: 1.15rem; font-weight: 700; color: #0F172A; word-break: break-word; }

    .stk-card {
        padding: 14px;
        border-radius: 8px;
        border-left: 4px solid;
        min-height: 100px;
        margin-bottom: 10px;
    }
    .stk-title { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px; }
    .stk-name { font-size: 0.95rem; font-weight: 600; line-height: 1.3; }
    .stk-count { font-size: 0.75rem; opacity: 0.8; margin-top: 4px; }

    .stk-decision { background-color: #EFF6FF; border-color: #2563EB; color: #1E40AF; }
    .stk-influencer { background-color: #ECFDF5; border-color: #059669; color: #065F46; }
    .stk-champion { background-color: #FEFCE8; border-color: #D97706; color: #92400E; }
    .stk-user { background-color: #F3E8FF; border-color: #7C3AED; color: #5B21B6; }
    .stk-blocker { background-color: #FEF2F2; border-color: #DC2626; color: #991B1B; }

    .ai-box {
        background-color: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-left: 5px solid #16A34A;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
    }

    .progress-track {
        background-color: #E2E8F0;
        border-radius: 6px;
        height: 10px;
        width: 100%;
        overflow: hidden;
        margin-top: 6px;
    }
    .progress-fill { height: 100%; border-radius: 6px; }

    .sidebar-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 4px;
    }
    .badge-red { background-color: #FEF2F2; color: #991B1B; }
    .badge-yellow { background-color: #FFFBEB; color: #92400E; }
    .badge-green { background-color: #F0FDF4; color: #166534; }
    .badge-neutral { background-color: #F1F5F9; color: #334155; }
    </style>
""", unsafe_allow_html=True)

# =============================================================================
# HELPER FUNCTIONS (avoid repeating raw HTML f-strings everywhere)
# =============================================================================

def overview_card(label, value, sub=None):
    sub_html = f'<span style="font-size:0.85rem; color:#64748B;"> {sub}</span>' if sub else ""
    st.markdown(f"""
        <div class="overview-card">
            <div class="overview-label">{label}</div>
            <div class="overview-value">{value}{sub_html}</div>
        </div>
    """, unsafe_allow_html=True)


def stakeholder_card(role_class, title, name, count=None):
    count_html = f'<div class="stk-count">{count} in this category</div>' if count else ""
    st.markdown(f"""
        <div class="stk-card {role_class}">
            <div class="stk-title">{title}</div>
            <div class="stk-name">{name}</div>
            {count_html}
        </div>
    """, unsafe_allow_html=True)


def card_box(title, body_html, border_color=None, title_color=None):
    style = f'border-left: 4px solid {border_color};' if border_color else ""
    tcolor = f'color:{title_color};' if title_color else ""
    st.markdown(f"""
        <div class="card-box" style="{style}">
            <h4 style="margin-top:0; {tcolor}">{title}</h4>
            {body_html}
        </div>
    """, unsafe_allow_html=True)


def progress_bar(pct, color, label=None):
    pct_display = min(pct, 100)
    label_html = f'<div style="font-size:0.8rem; color:#64748B; margin-top:4px;">{label}</div>' if label else ""
    st.markdown(f"""
        <div class="progress-track">
            <div class="progress-fill" style="width:{pct_display}%; background-color:{color};"></div>
        </div>
        {label_html}
    """, unsafe_allow_html=True)


def health_color(score):
    if score >= 75:
        return "#059669"
    elif score >= 60:
        return "#D97706"
    return "#DC2626"


def badge(text, level):
    return f'<span class="sidebar-badge badge-{level}">{text}</span>'


def kpi_performance_pct(value_num, target_num, lower_is_better=False):
    if lower_is_better:
        return round(min(target_num / value_num * 100, 150), 1)
    return round(min(value_num / target_num * 100, 150), 1)


# =============================================================================
# DATA
# =============================================================================
DATA = {
    "Zomato": {
        "acv": "$350,000",
        "health_score": 88,
        "health_status": "Healthy",
        "renewal_date": date(2026, 11, 15),
        "stage": "Expansion Phase",
        "adoption_rate": "84%",
        "active_licenses": "420 / 500",
        "license_utilization": "84.0%",
        "stakeholders": {
            "Decision-maker": "Rajesh Menon (Chief Operating Officer)",
            "Influencer": "Priya Sharma (VP of Product Engineering)",
            "Champion": "Ananya Iyer (Head of Talent Acquisition)",
            "User": "Karan Verma (Technical Recruiting Lead)",
            "Blocker": "Suresh Nair (IT Security Compliance Lead)"
        },
        "stakeholder_counts": {"Decision-makers": 2, "Influencers": 5, "Champions": 4, "Users": 18, "Blockers": 1},
        "usage_months": ["May", "Jun", "Jul", "Aug", "Sep"],
        "usage_scores": [65, 72, 78, 85, 94],
        "kpis": [
            {"metric": "Candidate Assessment Time", "value": "1.2 Days", "target": "< 2.0 Days",
             "status": "🟢 Exceeding Target", "value_num": 1.2, "target_num": 2.0, "lower_is_better": True},
            {"metric": "Monthly Active Recruiters", "value": "142 Active Leads", "target": "120 Leads",
             "status": "🟢 Exceeding Target", "value_num": 142, "target_num": 120, "lower_is_better": False},
            {"metric": "Assessment Completion Rate", "value": "91.4%", "target": "85.0%",
             "status": "🟢 Exceeding Target", "value_num": 91.4, "target_num": 85.0, "lower_is_better": False}
        ],
        "surveys": [
            {"nps": "88 (Promoter)", "csat": "4.8 / 5.0", "feedback": "Automated tech screening reduced our engineering recruiter workload significantly."},
            {"nps": "82 (Promoter)", "csat": "4.6 / 5.0", "feedback": "Smooth UI and easy candidate invite link generation."}
        ],
        "escalations": [
            {"id": "ESC-1092", "priority": "🟡 Medium", "issue": "Bulk ATS candidate export sync delay during peak volume hours.", "status": "In Progress", "owner": "Engineering Lead"},
            {"id": "ESC-1045", "priority": "🟢 Low", "issue": "Custom role taxonomy request for quick-commerce operational leads.", "status": "Resolved", "owner": "CSM Team"},
            {"id": "ESC-1241", "priority": "🟡 Medium", "issue": "Candidates on Safari mobile see a blank screen during the coding assessment step; reproducible on iOS 17, affects ~8% of test-takers.", "status": "In Progress", "owner": "Frontend Team"},
            {"id": "ESC-1296", "priority": "🟡 Medium", "issue": "New hiring managers were not granted platform access after the Q3 org restructure; 12 open reqs have no assigned evaluator.", "status": "In Progress", "owner": "CSM Team"}
        ],
        "events": "Q2 earnings revealed 28% growth in quick-commerce segment (Blinkit).",
        "hiring": "Massive hiring spree across NCR & Bengaluru for logistics automation roles.",
        "leadership": "Priya Sharma promoted to VP of Product Engineering; previous Head of Talent transitioned out.",
        "news": "Launching fresh quick-delivery dark stores in 15 new tier-2 cities.",
        "usage": "Assessment volume increased by 42% YoY; high adoption in tech screening.",
        "risks_opps": "Opportunity: Upsell Hunar.AI automated candidate evaluation for regional logistics staff.",
        "ai_analysis": {
            "what": "Zomato expands quick-commerce delivery network to 15 tier-2 cities.",
            "why": "Requires rapid onboarding of local operations and technical fleet leads.",
            "action": "Propose an automated regional assessment framework to scale hiring quality.",
            "talking_point": "Congratulations on the expansion into tier-2 markets! To support this speed, we can deploy pre-configured evaluation templates so your team screens candidate cohorts in under 24 hours."
        }
    },
    "McDonald's": {
        "acv": "$220,000",
        "health_score": 68,
        "health_status": "Stable",
        "renewal_date": date(2026, 10, 20),
        "stage": "Adoption Phase",
        "adoption_rate": "62%",
        "active_licenses": "186 / 300",
        "license_utilization": "62.0%",
        "stakeholders": {
            "Decision-maker": "Michael Turner (Chief HR Officer)",
            "Influencer": "Sarah Collins (Director of Franchise Operations)",
            "Champion": "David Brooks (Learning & Development Specialist)",
            "User": "Emily Chen (Store Operations Manager)",
            "Blocker": "Robert Hayes (Procurement Specialist)"
        },
        "stakeholder_counts": {"Decision-makers": 1, "Influencers": 3, "Champions": 2, "Users": 12, "Blockers": 2},
        "usage_months": ["May", "Jun", "Jul", "Aug", "Sep"],
        "usage_scores": [80, 78, 75, 70, 64],
        "kpis": [
            {"metric": "Store Manager Engagement", "value": "62%", "target": "80%",
             "status": "🟡 Below Target", "value_num": 62, "target_num": 80, "lower_is_better": False},
            {"metric": "Digital Literacy Pass Rate", "value": "78%", "target": "85%",
             "status": "🟡 Needs Improvement", "value_num": 78, "target_num": 85, "lower_is_better": False},
            {"metric": "Onboarding Completion Time", "value": "4.5 Days", "target": "< 3.0 Days",
             "status": "🔴 Delayed", "value_num": 4.5, "target_num": 3.0, "lower_is_better": True}
        ],
        "surveys": [
            {"nps": "65 (Passive)", "csat": "3.9 / 5.0", "feedback": "Store managers are focused on kiosk upgrades, leaving less time for routine assessments."},
            {"nps": "70 (Passive)", "csat": "4.1 / 5.0", "feedback": "Platform is useful, but mobile workflow needs to be faster for store leads."}
        ],
        "escalations": [
            {"id": "ESC-1120", "priority": "🔴 High", "issue": "Mobile login timeouts reported by regional store leads in West Zone.", "status": "Under Investigation", "owner": "DevOps / Support"},
            {"id": "ESC-1088", "priority": "🟡 Medium", "issue": "Franchise portal reporting mismatch on store completion status.", "status": "In Progress", "owner": "Product Support"},
            {"id": "ESC-1252", "priority": "🔴 High", "issue": "Client was invoiced for 300 licenses but their signed order form specifies 260; finance team is withholding payment pending correction.", "status": "Pending Finance Review", "owner": "Billing / Deal Desk"},
            {"id": "ESC-1307", "priority": "🟢 Low", "issue": "L&D team requested a live re-training session after 3 new regional managers reported confusion navigating the reporting dashboard.", "status": "Scheduled", "owner": "Customer Education"}
        ],
        "events": "Announced nationwide digital drive-thru and self-ordering kiosk upgrades.",
        "hiring": "Frontline digital literacy upskilling drives across regional franchises.",
        "leadership": "Michael Turner appointed as CHRO to lead franchise digital workforce capability.",
        "news": "Strategic partnership announced to integrate automated drive-thru ordering.",
        "usage": "Platform login activity down 18% over the last 45 days in west zone.",
        "risks_opps": "Risk: Low manager engagement; Opportunity: Align Hunar.AI with digital kiosk upskilling.",
        "ai_analysis": {
            "what": "Manager platform engagement dropped 18% during store digital upgrades.",
            "why": "Store leads are overloaded with kiosk rollouts and neglecting routine assessments.",
            "action": "Schedule a 15-minute executive review with CHRO Michael Turner to streamline store manager workflows.",
            "talking_point": "We noticed store teams are focused on kiosk upgrades. We created a 3-minute mobile assessment model so managers can verify team digital skills without taking time away from store operations."
        }
    },
    "Honda": {
        "acv": "$410,000",
        "health_score": 52,
        "health_status": "At-Risk",
        "renewal_date": date(2026, 12, 5),
        "stage": "Renewal at Risk",
        "adoption_rate": "45%",
        "active_licenses": "225 / 500",
        "license_utilization": "45.0%",
        "stakeholders": {
            "Decision-maker": "Hiroshi Tanaka (Managing Director - Supply Chain)",
            "Influencer": "Kenji Watanabe (VP of Manufacturing)",
            "Champion": "Aiko Suzuki (Corporate Training Lead — Departed)",
            "User": "Yuki Sato (Factory HR Manager)",
            "Blocker": "Daichi Kobayashi (Enterprise Software Auditor)"
        },
        "stakeholder_counts": {"Decision-makers": 3, "Influencers": 2, "Champions": 1, "Users": 8, "Blockers": 3},
        "usage_months": ["May", "Jun", "Jul", "Aug", "Sep"],
        "usage_scores": [70, 65, 58, 50, 42],
        "kpis": [
            {"metric": "EV Division Skill Coverage", "value": "35%", "target": "75%",
             "status": "🔴 Critical Gap", "value_num": 35, "target_num": 75, "lower_is_better": False},
            {"metric": "Factory Lead Adoption", "value": "45%", "target": "80%",
             "status": "🔴 Low Engagement", "value_num": 45, "target_num": 80, "lower_is_better": False},
            {"metric": "Assessment Completion Rate", "value": "54%", "target": "85%",
             "status": "🔴 At Risk", "value_num": 54, "target_num": 85, "lower_is_better": False}
        ],
        "surveys": [
            {"nps": "45 (Detractor)", "csat": "3.1 / 5.0", "feedback": "Our main training lead left, and the software needs re-alignment with new EV software roles."},
            {"nps": "50 (Passive)", "csat": "3.4 / 5.0", "feedback": "Need custom EV technical skill modules."}
        ],
        "escalations": [
            {"id": "ESC-1155", "priority": "🔴 Critical", "issue": "Lack of admin access after Champion departure stalled EV module deployment.", "status": "Pending Client Action", "owner": "Account Director"},
            {"id": "ESC-1102", "priority": "🔴 High", "issue": "Security compliance audit flag on multi-tenant deployment model.", "status": "Under Review", "owner": "InfoSec Team"},
            {"id": "ESC-1274", "priority": "🔴 Critical", "issue": "Security team flagged that candidate PII was included in a debug log accessible to internal support staff; requires immediate audit and data purge.", "status": "Under Investigation", "owner": "InfoSec / Legal"},
            {"id": "ESC-1318", "priority": "🔴 High", "issue": "No clear internal owner has stepped in since the Champion's departure; platform usage has dropped 30% in 2 weeks.", "status": "Pending Client Action", "owner": "Account Director"}
        ],
        "events": "EV shift mandate initiated across R&D and assembly plants.",
        "hiring": "Hiring freeze on traditional IC engine roles; hiring surge for EV software engineers.",
        "leadership": "Primary Champion Aiko Suzuki departed; interim HR team evaluating software vendors.",
        "news": "Pivoting $1B manufacturing budget to electric vehicle and battery plant assembly.",
        "usage": "License utilization at 45%; platform usage restricted to assembly divisions.",
        "risks_opps": "Risk: Champion loss + low utilization; Opportunity: Re-align platform to EV software team.",
        "ai_analysis": {
            "what": "Primary champion Aiko Suzuki departed amidst company pivot to EV manufacturing.",
            "why": "Risk of non-renewal due to lack of central ownership and low usage.",
            "action": "Reach out to Decision-maker Hiroshi Tanaka to align Hunar.AI with the new EV software hiring mandate.",
            "talking_point": "With Honda's shift to EV production, we want to ensure Hunar.AI directly supports your new EV software engineering hiring goals. Let's align on a refreshed skill taxonomy for your R&D teams."
        }
    }
}

# =============================================================================
# HEADER
# =============================================================================
st.markdown(f"""
    <div class="sirius-header">
        <div>
            <div class="sirius-title">⚡ SIRIUS</div>
            <div class="sirius-subtitle">Enterprise Customer Intelligence Tool</div>
        </div>
        <div class="sirius-asof">Data as of<br><strong style="color:#E2E8F0;">{TODAY.strftime('%B %d, %Y')}</strong></div>
    </div>
""", unsafe_allow_html=True)

# =============================================================================
# SIDEBAR
# =============================================================================
st.sidebar.title("🏢 Accounts")

# Quick triage badges for every account, always visible
for name, d in DATA.items():
    level = "green" if d["health_score"] >= 75 else ("yellow" if d["health_score"] >= 60 else "red")
    open_escs = sum(1 for e in d["escalations"] if e["status"] not in ("Resolved",))
    days_left = (d["renewal_date"] - TODAY).days
    health_val = d["health_score"]
    esc_level = "red" if open_escs else "green"
    badges_html = (
        badge(str(health_val), level)
        + badge(f"{open_escs} open esc.", esc_level)
        + badge(f"{days_left}d to renewal", "neutral")
    )
    st.sidebar.markdown(f"**{name}** {badges_html}", unsafe_allow_html=True)

st.sidebar.divider()

view_option = st.sidebar.radio(
    "View",
    ["Portfolio Overview", "Executive Overview", "Adoption & Utilization", "KPI Reports", "Surveys & Feedback", "Escalations"]
)

selected_customer = st.sidebar.selectbox("🔽 Jump to Account", list(DATA.keys()))
if view_option != "Portfolio Overview":
    cust = DATA[selected_customer]

# =============================================================================
# VIEW: PORTFOLIO OVERVIEW (landing page across all accounts)
# =============================================================================
if view_option == "Portfolio Overview":
    st.markdown("### 🗂️ Portfolio at a Glance")
    st.caption("All enterprise accounts, ranked by health. Click into an account view from the sidebar for details.")

    total_acv = sum(int(d["acv"].replace("$", "").replace(",", "")) for d in DATA.values())
    avg_health = round(sum(d["health_score"] for d in DATA.values()) / len(DATA))
    total_open_escs = sum(
        1 for d in DATA.values() for e in d["escalations"] if e["status"] != "Resolved"
    )

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Portfolio ACV", f"${total_acv:,}")
    m2.metric("Accounts", len(DATA))
    m3.metric("Avg. Health Score", avg_health)
    m4.metric("Open Escalations", total_open_escs)

    st.divider()

    rows = []
    for name, d in DATA.items():
        open_escs = sum(1 for e in d["escalations"] if e["status"] != "Resolved")
        rows.append({
            "Account": name,
            "Health": d["health_score"],
            "Status": d["health_status"],
            "ACV": d["acv"],
            "Stage": d["stage"],
            "Renewal": d["renewal_date"].strftime("%b %d, %Y"),
            "Days Left": (d["renewal_date"] - TODAY).days,
            "Open Escalations": open_escs
        })
    portfolio_df = pd.DataFrame(rows).sort_values("Health")

    st.dataframe(
        portfolio_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Health": st.column_config.ProgressColumn("Health", min_value=0, max_value=100, format="%d"),
        }
    )

    st.divider()
    st.markdown("#### ⚠️ Accounts Needing Attention First")
    at_risk = [name for name, d in DATA.items() if d["health_score"] < 60]
    if at_risk:
        for name in at_risk:
            d = DATA[name]
            card_box(
                f"🔴 {name} — {d['stage']}",
                f"<p style='margin-bottom:0;'>{d['ai_analysis']['action']}</p>",
                border_color="#DC2626", title_color="#991B1B"
            )
    else:
        st.success("No accounts currently below the health threshold. 🎉")

# =============================================================================
# VIEW: EXECUTIVE OVERVIEW
# =============================================================================
elif view_option == "Executive Overview":
    days_left = (cust["renewal_date"] - TODAY).days
    st.markdown(f"## {selected_customer}")
    st.caption(f"{cust['stage']} · Renews in {days_left} days ({cust['renewal_date'].strftime('%B %d, %Y')})")

    tabs = st.tabs(["📊 Overview", "👥 Stakeholders", "📈 Analytics", "📡 Signals", "🤖 AI Insight"])

    with tabs[0]:
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            overview_card("Customer Name", selected_customer)
        with c2:
            overview_card("Annual Contract Value", cust["acv"])
        with c3:
            color = health_color(cust["health_score"])
            overview_card("Health Score", f'<span style="color:{color};">{cust["health_score"]} · {cust["health_status"]}</span>')
            progress_bar(cust["health_score"], color)
        with c4:
            overview_card("Renewal / Stage", cust["renewal_date"].strftime("%b %Y"), sub=f"({cust['stage']})")

    with tabs[1]:
        stk = cust["stakeholders"]
        counts = cust["stakeholder_counts"]
        s1, s2, s3, s4, s5 = st.columns(5)
        with s1:
            stakeholder_card("stk-decision", "Decision-Maker", stk["Decision-maker"], counts["Decision-makers"])
        with s2:
            stakeholder_card("stk-influencer", "Influencer", stk["Influencer"], counts["Influencers"])
        with s3:
            stakeholder_card("stk-champion", "Champion", stk["Champion"], counts["Champions"])
        with s4:
            stakeholder_card("stk-user", "User Lead", stk["User"], counts["Users"])
        with s5:
            stakeholder_card("stk-blocker", "Blocker", stk["Blocker"], counts["Blockers"])
        st.caption("Named contact shown is the primary point of contact in that category; the count reflects the total number of stakeholders mapped to that role.")

    with tabs[2]:
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            st.markdown("#### 🥧 Stakeholder Distribution")
            stk_counts = cust["stakeholder_counts"]
            pie_df = pd.DataFrame({"Category": list(stk_counts.keys()), "Count": list(stk_counts.values())})
            fig_pie = px.pie(
                pie_df, names="Category", values="Count", color="Category",
                color_discrete_map={"Decision-makers": "#2563EB", "Influencers": "#059669", "Champions": "#D97706", "Users": "#7C3AED", "Blockers": "#DC2626"},
                hole=0.4
            )
            fig_pie.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=280)
            st.plotly_chart(fig_pie, use_container_width=True)

        with chart_col2:
            st.markdown("#### 📊 5-Month Usage Trend")
            bar_df = pd.DataFrame({"Month": cust["usage_months"], "Engagement Score": cust["usage_scores"]})
            bar_color = health_color(cust["health_score"])
            fig_bar = px.bar(bar_df, x="Month", y="Engagement Score", text="Engagement Score", color_discrete_sequence=[bar_color])
            fig_bar.update_traces(textposition='outside')
            fig_bar.update_layout(yaxis_range=[0, 100], margin=dict(t=20, b=20, l=20, r=20), height=280)
            st.plotly_chart(fig_bar, use_container_width=True)

    with tabs[3]:
        grid_col1, grid_col2 = st.columns(2)
        with grid_col1:
            card_box("🏢 Company Events & Strategy", f"<p><strong>Events:</strong> {cust['events']}</p><p style='margin-bottom:0;'><strong>Strategy:</strong> {cust['news']}</p>")
            card_box("👔 Leadership & Hiring", f"<p><strong>Leadership:</strong> {cust['leadership']}</p><p style='margin-bottom:0;'><strong>Hiring:</strong> {cust['hiring']}</p>")
        with grid_col2:
            card_box("📈 Product & Usage Signals", f"<p style='margin-bottom:0;'>{cust['usage']}</p>")
            card_box("⚠️ Risks & Opportunities", f"<p style='margin-bottom:0;'>{cust['risks_opps']}</p>", border_color="#DC2626", title_color="#991B1B")

    with tabs[4]:
        ai = cust["ai_analysis"]
        st.markdown(f"""
            <div class="ai-box">
                <div style="font-size:0.75rem; font-weight:700; color:#15803D; text-transform:uppercase;">STRATEGIC ACTIONABLE INSIGHT</div>
                <h3 style="color: #15803D; margin-top: 6px; margin-bottom: 12px;">Signal Briefing: {selected_customer}</h3>
                <p><strong>1. What Happened:</strong> {ai['what']}</p>
                <p><strong>2. Why It Matters:</strong> {ai['why']}</p>
                <p><strong>3. Recommended CSM Action:</strong> {ai['action']}</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("**💬 Suggested Outreach Draft** (copy button on hover)")
        st.code(ai["talking_point"], language=None)

# =============================================================================
# VIEW: ADOPTION & UTILIZATION
# =============================================================================
elif view_option == "Adoption & Utilization":
    st.markdown(f"### 📈 Platform Adoption & Seat Utilization: {selected_customer}")
    st.caption("Detailed breakdown of account adoption rate, license allocation, and 5-month engagement trends.")

    col1, col2, col3 = st.columns(3)
    col1.metric("Overall Adoption Rate", cust["adoption_rate"])
    col2.metric("Active Seat Licenses", cust["active_licenses"])
    col3.metric("License Utilization Rate", cust["license_utilization"])

    st.divider()

    left, right = st.columns([1.4, 1])
    with left:
        st.markdown("#### 📊 5-Month Usage & Adoption Trend")
        bar_df = pd.DataFrame({"Month": cust["usage_months"], "Engagement Score": cust["usage_scores"]})
        bar_color = health_color(cust["health_score"])
        fig_bar = px.bar(bar_df, x="Month", y="Engagement Score", text="Engagement Score", color_discrete_sequence=[bar_color])
        fig_bar.update_traces(textposition='outside')
        fig_bar.update_layout(yaxis_range=[0, 100], height=340)
        st.plotly_chart(fig_bar, use_container_width=True)

    with right:
        st.markdown("#### 🎯 Licenses In Use")
        used, total = cust["active_licenses"].split(" / ")
        fig_gauge = go.Figure(go.Pie(
            values=[int(used), int(total) - int(used)],
            hole=0.65,
            marker_colors=[health_color(cust["health_score"]), "#E2E8F0"],
            textinfo="none",
            sort=False
        ))
        fig_gauge.update_layout(
            showlegend=False, height=340, margin=dict(t=20, b=20, l=20, r=20),
            annotations=[dict(text=cust["license_utilization"], x=0.5, y=0.5, font_size=24, showarrow=False)]
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    card_box("💡 Adoption Telemetry Brief", f"<p style='margin-bottom:0;'>{cust['usage']}</p>")

# =============================================================================
# VIEW: KPI REPORTS
# =============================================================================
elif view_option == "KPI Reports":
    st.markdown(f"### 🎯 Key Performance Indicator (KPI) Report: {selected_customer}")
    st.caption("Tracking contractually aligned outcome benchmarks and platform health metrics")

    kpi_pcts = [kpi_performance_pct(k["value_num"], k["target_num"], k["lower_is_better"]) for k in cust["kpis"]]
    kpi_names = [k["metric"] for k in cust["kpis"]]
    kpi_colors = ["#059669" if p >= 100 else ("#D97706" if p >= 80 else "#DC2626") for p in kpi_pcts]

    cchart1, cchart2 = st.columns(2)
    with cchart1:
        st.markdown("#### 📊 Performance vs. Target")
        fig_kpi_bar = px.bar(
            x=kpi_pcts, y=kpi_names, orientation="h", text=[f"{p}%" for p in kpi_pcts],
            color=kpi_names, color_discrete_sequence=kpi_colors
        )
        fig_kpi_bar.add_vline(x=100, line_dash="dash", line_color="#64748B")
        fig_kpi_bar.update_traces(textposition="outside")
        fig_kpi_bar.update_layout(showlegend=False, height=300, margin=dict(t=20, b=20, l=20, r=20),
                                   xaxis_title="% of Target", yaxis_title="")
        st.plotly_chart(fig_kpi_bar, use_container_width=True)

    with cchart2:
        st.markdown("#### 🥧 KPI Status Mix")
        status_counts = pd.Series([k["status"].split(" ", 1)[1] for k in cust["kpis"]]).value_counts()
        fig_kpi_pie = px.pie(
            names=status_counts.index, values=status_counts.values, hole=0.4,
            color=status_counts.index, color_discrete_sequence=kpi_colors
        )
        fig_kpi_pie.update_layout(height=300, margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_kpi_pie, use_container_width=True)

    st.divider()
    for kpi in cust["kpis"]:
        pct = kpi_performance_pct(kpi["value_num"], kpi["target_num"], kpi["lower_is_better"])
        bar_color = "#059669" if pct >= 100 else ("#D97706" if pct >= 80 else "#DC2626")
        st.markdown(f"""
            <div class="card-box">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h4 style="margin:0; color:#0F172A;">{kpi['metric']}</h4>
                    <span style="font-weight:700;">{kpi['status']}</span>
                </div>
                <div style="margin-top:10px; font-size:1.05rem;">
                    <strong>Current:</strong> {kpi['value']} &nbsp;|&nbsp; <strong>Target:</strong> {kpi['target']}
                </div>
            </div>
        """, unsafe_allow_html=True)
        progress_bar(pct, bar_color, label=f"{pct}% of target performance")
        st.write("")

# =============================================================================
# VIEW: SURVEYS & FEEDBACK
# =============================================================================
elif view_option == "Surveys & Feedback":
    st.markdown(f"### 📋 Customer Surveys & Voice of Customer (VoC): {selected_customer}")
    st.caption("Aggregated NPS, CSAT, and direct qualitative stakeholder feedback")

    for survey in cust["surveys"]:
        st.markdown(f"""
            <div class="card-box" style="border-left: 5px solid #2563EB;">
                <div style="display:flex; gap:20px; margin-bottom:10px;">
                    <div><strong>Net Promoter Score (NPS):</strong> {survey['nps']}</div>
                    <div><strong>CSAT Rating:</strong> {survey['csat']}</div>
                </div>
                <p style="margin:0; font-style:italic; color:#334155;">"{survey['feedback']}"</p>
            </div>
        """, unsafe_allow_html=True)

# =============================================================================
# VIEW: ESCALATIONS
# =============================================================================
elif view_option == "Escalations":
    st.markdown(f"### 🚨 Active Escalations & Issue Tracking: {selected_customer}")
    st.caption("Log of critical support tickets, product issues, and operational blockers")

    esc_c1, esc_c2 = st.columns(2)
    priority_order = ["🔴 Critical", "🔴 High", "🟡 Medium", "🟢 Low"]
    priority_colors = {"🔴 Critical": "#7F1D1D", "🔴 High": "#DC2626", "🟡 Medium": "#D97706", "🟢 Low": "#059669"}

    with esc_c1:
        st.markdown("#### 🥧 By Priority")
        pr_counts = pd.Series([e["priority"] for e in cust["escalations"]]).value_counts()
        fig_esc_pie = px.pie(
            names=pr_counts.index, values=pr_counts.values, hole=0.4,
            color=pr_counts.index, color_discrete_map=priority_colors
        )
        fig_esc_pie.update_layout(height=280, margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_esc_pie, use_container_width=True)

    with esc_c2:
        st.markdown("#### 📊 By Status")
        st_counts = pd.Series([e["status"] for e in cust["escalations"]]).value_counts()
        fig_esc_bar = px.bar(
            x=st_counts.values, y=st_counts.index, orientation="h", text=st_counts.values,
            color_discrete_sequence=["#2563EB"]
        )
        fig_esc_bar.update_traces(textposition="outside")
        fig_esc_bar.update_layout(height=280, margin=dict(t=20, b=20, l=20, r=20), xaxis_title="Count", yaxis_title="")
        st.plotly_chart(fig_esc_bar, use_container_width=True)

    st.divider()
    esc_view = st.radio("Display as", ["Cards", "Table"], horizontal=True, label_visibility="collapsed")
    st.markdown("<br>", unsafe_allow_html=True)

    if esc_view == "Table":
        esc_df = pd.DataFrame(cust["escalations"])
        st.dataframe(esc_df, use_container_width=True, hide_index=True)
    else:
        for esc in cust["escalations"]:
            border_color = "#DC2626" if ("Critical" in esc['priority'] or "High" in esc['priority']) else "#D97706"
            st.markdown(f"""
                <div class="card-box" style="border-left: 5px solid {border_color};">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <span style="font-weight:700; font-size:1.05rem; color:#0F172A;">Ticket ID: {esc['id']}</span>
                        <span><strong>Priority:</strong> {esc['priority']}</span>
                    </div>
                    <p style="margin:6px 0; font-size:1rem;"><strong>Issue Summary:</strong> {esc['issue']}</p>
                    <div style="display:flex; gap:30px; font-size:0.85rem; color:#64748B; margin-top:8px;">
                        <span><strong>Status:</strong> {esc['status']}</span>
                        <span><strong>Assigned Owner:</strong> {esc['owner']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

st.divider()
st.caption("Sirius Customer Intelligence Tool — Built for Hunar.AI CSM Assessment | Kanav Kundra")
