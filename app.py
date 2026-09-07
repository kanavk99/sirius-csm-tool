import streamlit as st
import plotly.express as px
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Sirius | Enterprise Customer Intelligence",
    page_icon="⚡",
    layout="wide"
)

# Custom Styling to Fix Overflow and Beautify
st.markdown("""
    <style>
    /* Header Banner */
    .sirius-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        color: #FFFFFF;
        padding: 20px 24px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .sirius-title { font-size: 2.2rem; font-weight: 800; color: #38BDF8; margin: 0; }
    .sirius-subtitle { font-size: 0.95rem; color: #94A3B8; margin-top: 4px; }
    
    /* Overview Cards */
    .overview-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 14px 18px;
        height: 100%;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .overview-label { font-size: 0.8rem; color: #64748B; font-weight: 600; text-transform: uppercase; margin-bottom: 6px; }
    .overview-value { font-size: 1.15rem; font-weight: 700; color: #0F172A; word-break: break-word; }

    /* Stakeholder Cards */
    .stk-card {
        padding: 14px;
        border-radius: 8px;
        border-left: 4px solid;
        min-height: 90px;
        margin-bottom: 10px;
    }
    .stk-title { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px; }
    .stk-name { font-size: 0.95rem; font-weight: 600; word-wrap: break-word; line-height: 1.3; }

    .stk-decision { background-color: #EFF6FF; border-color: #2563EB; color: #1E40AF; }
    .stk-influencer { background-color: #ECFDF5; border-color: #059669; color: #065F46; }
    .stk-champion { background-color: #FEFCE8; border-color: #D97706; color: #92400E; }
    .stk-user { background-color: #F3E8FF; border-color: #7C3AED; color: #5B21B6; }
    .stk-blocker { background-color: #FEF2F2; border-color: #DC2626; color: #991B1B; }

    /* General Cards */
    .card-box {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .ai-box {
        background-color: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-left: 5px solid #16A34A;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Main Banner Header
st.markdown("""
    <div class="sirius-header">
        <div class="sirius-title">⚡ SIRIUS</div>
        <div class="sirius-subtitle">Enterprise Customer Intelligence & Stakeholder Mapping Dashboard</div>
    </div>
""", unsafe_allow_html=True)

# Sidebar Controls
st.sidebar.title("🏢 Select Account")
selected_customer = st.sidebar.selectbox(
    "Choose Enterprise Customer",
    ["Zomato", "McDonald's", "Honda"]
)

# Comprehensive Dataset
DATA = {
    "Zomato": {
        "acv": "$350,000",
        "health_score": 88,
        "health_status": "🟢 88 (Healthy)",
        "renewal": "Nov 2026",
        "stage": "Expansion Phase",
        "stakeholders": {
            "Decision-maker": "ABC (Chief Operating Officer)",
            "Influencer": "XYZ (VP of Product Engineering)",
            "Champion": "PQR (Head of Talent Acquisition)",
            "User": "LMN (Technical Recruiting Lead)",
            "Blocker": "STU (IT Security Compliance Lead)"
        },
        "stakeholder_counts": {"Decision-makers": 2, "Influencers": 5, "Champions": 4, "Users": 18, "Blockers": 1},
        "usage_months": ["May", "Jun", "Jul", "Aug", "Sep"],
        "usage_scores": [65, 72, 78, 85, 94],
        "events": "Q2 earnings revealed 28% growth in quick-commerce segment (Blinkit).",
        "hiring": "Massive hiring spree across NCR & Bengaluru for logistics automation roles.",
        "leadership": "XYZ promoted to VP of Product Engineering; previous Head of Talent ABC transitioned out.",
        "news": "Launching fresh quick-delivery dark stores in 15 new tier-2 cities.",
        "usage": "Assessment volume increased by 42% YoY; high adoption in tech screening.",
        "risks_opps": "Opportunity: Upsell Hunar.AI automated candidate evaluation for regional logistics staff.",
        "ai_analysis": {
            "what": "Zomato expands quick-commerce delivery network to 15 tier-2 cities.",
            "why": "Requires rapid onboarding of local operations and technical fleet leads.",
            "action": "Propose an automated regional assessment framework to scale hiring quality.",
            "talking_point": "'Congratulations on the expansion into tier-2 markets! To support this speed, we can deploy pre-configured evaluation templates so your team screens candidate cohorts in under 24 hours.'"
        }
    },
    "McDonald's": {
        "acv": "$220,000",
        "health_score": 68,
        "health_status": "🟡 68 (Stable)",
        "renewal": "Oct 2026",
        "stage": "Adoption Phase",
        "stakeholders": {
            "Decision-maker": "ABC (Chief HR Officer)",
            "Influencer": "XYZ (Director of Franchise Operations)",
            "Champion": "PQR (Learning & Development Specialist)",
            "User": "LMN (Store Operations Manager)",
            "Blocker": "STU (Procurement Specialist)"
        },
        "stakeholder_counts": {"Decision-makers": 1, "Influencers": 3, "Champions": 2, "Users": 12, "Blockers": 2},
        "usage_months": ["May", "Jun", "Jul", "Aug", "Sep"],
        "usage_scores": [80, 78, 75, 70, 64],
        "events": "Announced nationwide digital drive-thru and self-ordering kiosk upgrades.",
        "hiring": "Frontline digital literacy upskilling drives across regional franchises.",
        "leadership": "ABC appointed as CHRO to lead franchise digital workforce capability.",
        "news": "Strategic partnership announced to integrate automated drive-thru ordering.",
        "usage": "Platform login activity down 18% over the last 45 days in west zone.",
        "risks_opps": "Risk: Low manager engagement; Opportunity: Align Hunar.AI with digital kiosk upskilling.",
        "ai_analysis": {
            "what": "Manager platform engagement dropped 18% during store digital upgrades.",
            "why": "Store leads are overloaded with kiosk rollouts and neglecting routine assessments.",
            "action": "Schedule a 15-minute executive review with CHRO ABC to streamline store manager workflows.",
            "talking_point": "'We noticed store teams are focused on kiosk upgrades. We created a 3-minute mobile assessment model so managers can verify team digital skills without taking time away from store operations.'"
        }
    },
    "Honda": {
        "acv": "$410,000",
        "health_score": 52,
        "health_status": "🔴 52 (At-Risk)",
        "renewal": "Dec 2026",
        "stage": "Renewal at Risk",
        "stakeholders": {
            "Decision-maker": "ABC (Managing Director - Supply Chain)",
            "Influencer": "XYZ (VP of Manufacturing)",
            "Champion": "PQR (Corporate Training Lead)",
            "User": "LMN (Factory HR Manager)",
            "Blocker": "STU (Enterprise Software Auditor)"
        },
        "stakeholder_counts": {"Decision-makers": 3, "Influencers": 2, "Champions": 1, "Users": 8, "Blockers": 3},
        "usage_months": ["May", "Jun", "Jul", "Aug", "Sep"],
        "usage_scores": [70, 65, 58, 50, 42],
        "events": "EV shift mandate initiated across R&D and assembly plants.",
        "hiring": "Hiring freeze on traditional IC engine roles; hiring surge for EV software engineers.",
        "leadership": "Primary Champion PQR departed; interim HR team evaluating software vendors.",
        "news": "Pivoting $1B manufacturing budget to electric vehicle and battery plant assembly.",
        "usage": "License utilization at 45%; platform usage restricted to assembly divisions.",
        "risks_opps": "Risk: Champion loss + low utilization; Opportunity: Re-align platform to EV software team.",
        "ai_analysis": {
            "what": "Primary champion PQR departed amidst company pivot to EV manufacturing.",
            "why": "Risk of non-renewal due to lack of central ownership and low usage.",
            "action": "Reach out to Decision-maker ABC to align Hunar.AI with the new EV software hiring mandate.",
            "talking_point": "'With Honda's shift to EV production, we want to ensure Hunar.AI directly supports your new EV software engineering hiring goals. Let's align on a refreshed skill taxonomy for your R&D teams.'"
        }
    }
}

cust = DATA[selected_customer]

# SECTION 1: CUSTOMER OVERVIEW & HEALTH (Custom Responsive Layout)
st.markdown("### 📊 1. Customer Overview & Health Status")

c1, c2, c3, c4 = st.columns([1, 1, 1, 1.3])
with c1:
    st.markdown(f"""
        <div class="overview-card">
            <div class="overview-label">Customer Name</div>
            <div class="overview-value">{selected_customer}</div>
        </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"""
        <div class="overview-card">
            <div class="overview-label">Annual Contract Value</div>
            <div class="overview-value">{cust['acv']}</div>
        </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown(f"""
        <div class="overview-card">
            <div class="overview-label">Health Score</div>
            <div class="overview-value">{cust['health_status']}</div>
        </div>
    """, unsafe_allow_html=True)
with c4:
    st.markdown(f"""
        <div class="overview-card">
            <div class="overview-label">Renewal / Stage</div>
            <div class="overview-value">{cust['renewal']} <span style="font-size:0.85rem; color:#64748B;">({cust['stage']})</span></div>
        </div>
    """, unsafe_allow_html=True)

st.write("")
st.divider()

# SECTION 2: ENTERPRISE STAKEHOLDER MATRIX (Responsive Cards)
st.markdown("### 👥 2. Enterprise Stakeholder Mapping")
st.caption("Mapped roles and internal influence structure")

stk = cust["stakeholders"]
s1, s2, s3, s4, s5 = st.columns(5)

with s1:
    st.markdown(f"""
        <div class="stk-card stk-decision">
            <div class="stk-title">Decision-Maker</div>
            <div class="stk-name">{stk['Decision-maker']}</div>
        </div>
    """, unsafe_allow_html=True)
with s2:
    st.markdown(f"""
        <div class="stk-card stk-influencer">
            <div class="stk-title">Influencer</div>
            <div class="stk-name">{stk['Influencer']}</div>
        </div>
    """, unsafe_allow_html=True)
with s3:
    st.markdown(f"""
        <div class="stk-card stk-champion">
            <div class="stk-title">Champion</div>
            <div class="stk-name">{stk['Champion']}</div>
        </div>
    """, unsafe_allow_html=True)
with s4:
    st.markdown(f"""
        <div class="stk-card stk-user">
            <div class="stk-title">User Lead</div>
            <div class="stk-name">{stk['User']}</div>
        </div>
    """, unsafe_allow_html=True)
with s5:
    st.markdown(f"""
        <div class="stk-card stk-blocker">
            <div class="stk-title">Blocker</div>
            <div class="stk-name">{stk['Blocker']}</div>
        </div>
    """, unsafe_allow_html=True)

st.write("")
st.divider()

# SECTION 3: VISUAL ANALYTICS (PIE & BAR CHARTS)
st.markdown("### 📈 3. Customer Intelligence Analytics")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("#### 🥧 Stakeholder Distribution")
    stk_counts = cust["stakeholder_counts"]
    pie_df = pd.DataFrame({
        "Category": list(stk_counts.keys()),
        "Count": list(stk_counts.values())
    })
    
    fig_pie = px.pie(
        pie_df, 
        names="Category", 
        values="Count", 
        color="Category",
        color_discrete_map={
            "Decision-makers": "#2563EB",
            "Influencers": "#059669",
            "Champions": "#D97706",
            "Users": "#7C3AED",
            "Blockers": "#DC2626"
        },
        hole=0.4
    )
    fig_pie.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=280)
    st.plotly_chart(fig_pie, use_container_width=True)

with chart_col2:
    st.markdown("#### 📊 5-Month Usage Trend")
    bar_df = pd.DataFrame({
        "Month": cust["usage_months"],
        "Engagement Score": cust["usage_scores"]
    })
    
    bar_color = "#059669" if cust["health_score"] >= 75 else ("#D97706" if cust["health_score"] >= 60 else "#DC2626")
    
    fig_bar = px.bar(
        bar_df, 
        x="Month", 
        y="Engagement Score", 
        text="Engagement Score",
        color_discrete_sequence=[bar_color]
    )
    fig_bar.update_traces(textposition='outside')
    fig_bar.update_layout(yaxis_range=[0, 100], margin=dict(t=20, b=20, l=20, r=20), height=280)
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# SECTION 4: ORGANIZATIONAL SIGNALS & TELEMETRY
st.markdown("### 📡 4. Company Insights & Telemetry Signals")

grid_col1, grid_col2 = st.columns(2)

with grid_col1:
    st.markdown(f"""
        <div class="card-box">
            <h4 style="margin-top:0; color:#0F172A;">🏢 Company Events & Strategic Developments</h4>
            <p><strong>Recent Events:</strong> {cust['events']}</p>
            <p style="margin-bottom:0;"><strong>News & Strategy:</strong> {cust['news']}</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="card-box">
            <h4 style="margin-top:0; color:#0F172A;">👔 Hiring Signals & Leadership Changes</h4>
            <p><strong>Leadership Shifts:</strong> {cust['leadership']}</p>
            <p style="margin-bottom:0;"><strong>Hiring Signals:</strong> {cust['hiring']}</p>
        </div>
    """, unsafe_allow_html=True)

with grid_col2:
    st.markdown(f"""
        <div class="card-box">
            <h4 style="margin-top:0; color:#0F172A;">📈 Product & Usage Signals</h4>
            <p style="margin-bottom:0;">{cust['usage']}</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="card-box" style="border-left: 4px solid #DC2626;">
            <h4 style="margin-top:0; color:#991B1B;">⚠️ Strategic Risks & Growth Opportunities</h4>
            <p style="margin-bottom:0;">{cust['risks_opps']}</p>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# SECTION 5: AI INSIGHT ENGINE
st.markdown("### 🤖 5. AI Insight Engine")
st.caption("Actionable recommendations derived from signal intelligence")

ai = cust["ai_analysis"]

st.markdown(f"""
    <div class="ai-box">
        <div style="font-size:0.75rem; font-weight:700; color:#15803D; letter-spacing:0.5px; text-transform:uppercase;">STRATEGIC ACTIONABLE INSIGHT</div>
        <h3 style="color: #15803D; margin-top: 6px; margin-bottom: 12px;">Signal Briefing: {selected_customer}</h3>
        <p><strong>1. What Happened:</strong> {ai['what']}</p>
        <p><strong>2. Why It Matters:</strong> {ai['why']}</p>
        <p><strong>3. Recommended CSM Action:</strong> {ai['action']}</p>
        <div style="background-color: #FFFFFF; padding: 14px; border-radius: 8px; border: 1px dashed #16A34A; margin-top: 12px;">
            <p style="margin: 0; color: #166534; font-weight:600;">💬 Suggested Talking Point / Executive Outreach Draft:</p>
            <p style="margin: 6px 0 0 0; font-style: italic; color: #334155;">{ai['talking_point']}</p>
        </div>
    </div>
""", unsafe_allow_html=True)

st.divider()
st.caption("Sirius Customer Intelligence Tool — Built for Hunar.AI CSM Assessment | Kanav Kundra")
