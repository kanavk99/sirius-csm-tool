import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Sirius | Enterprise Customer Intelligence",
    page_icon="⚡",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .sirius-header {
        background: linear-gradient(90deg, #0F172A 0%, #1E293B 100%);
        color: #FFFFFF;
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .sirius-title { font-size: 2.4rem; font-weight: 800; color: #38BDF8; margin: 0; }
    .sirius-subtitle { font-size: 1.05rem; color: #94A3B8; margin-top: 5px; }
    .card-box {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .badge-risk { background-color: #FEE2E2; color: #991B1B; padding: 4px 8px; border-radius: 4px; font-weight: 600; font-size: 0.8rem; }
    .badge-growth { background-color: #DCFCE7; color: #166534; padding: 4px 8px; border-radius: 4px; font-weight: 600; font-size: 0.8rem; }
    .badge-insight { background-color: #E0F2FE; color: #075985; padding: 4px 8px; border-radius: 4px; font-weight: 600; font-size: 0.8rem; }
    .ai-box {
        background-color: #F0FDF4;
        border-left: 4px solid #16A34A;
        padding: 15px;
        border-radius: 6px;
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
        "health": "🟢 88 (Healthy)",
        "renewal": "Nov 2026",
        "stage": "Expansion Phase",
        "stakeholders": {
            "Decision-maker": "ABC (Chief Operating Officer)",
            "Influencer": "XYZ (VP of Product Engineering)",
            "Champion": "PQR (Head of Talent Acquisition)",
            "User": "LMN (Technical Recruiting Lead)",
            "Blocker": "STU (IT Security Compliance Lead)"
        },
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
        "health": "🟡 68 (Stable)",
        "renewal": "Oct 2026",
        "stage": "Adoption Phase",
        "stakeholders": {
            "Decision-maker": "ABC (Chief HR Officer)",
            "Influencer": "XYZ (Director of Franchise Operations)",
            "Champion": "PQR (Learning & Development Specialist)",
            "User": "LMN (Store Operations Manager)",
            "Blocker": "STU (Procurement Specialist)"
        },
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
        "health": "🔴 52 (At-Risk)",
        "renewal": "Dec 2026",
        "stage": "Renewal at Risk",
        "stakeholders": {
            "Decision-maker": "ABC (Managing Director - Supply Chain)",
            "Influencer": "XYZ (VP of Manufacturing)",
            "Champion": "PQR (Corporate Training Lead)",
            "User": "LMN (Factory HR Manager)",
            "Blocker": "STU (Enterprise Software Auditor)"
        },
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

# SECTION 1: CUSTOMER OVERVIEW & HEALTH
st.markdown("### 📊 1. Customer Overview & Health Status")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Customer Name", selected_customer)
col2.metric("Annual Contract Value", cust["acv"])
col3.metric("Health Score", cust["health"])
col4.metric("Renewal / Stage", f"{cust['renewal']} | {cust['stage']}")

st.divider()

# SECTION 2: ENTERPRISE STAKEHOLDER MATRIX
st.markdown("### 👥 2. Enterprise Stakeholder Mapping")
st.caption("Mapped roles and internal influence structure")

stk = cust["stakeholders"]
s_col1, s_col2, s_col3, s_col4, s_col5 = st.columns(5)
s_col1.info(f"**Decision-Maker**\n\n{stk['Decision-maker']}")
s_col2.success(f"**Influencer**\n\n{stk['Influencer']}")
s_col3.warning(f"**Champion**\n\n{stk['Champion']}")
s_col4.metric("Users", stk['User'])
s_col5.error(f"**Blocker**\n\n{stk['Blocker']}")

st.divider()

# SECTION 3: ORGANIZATIONAL SIGNALS & TELEMETRY
st.markdown("### 📡 3. Recent Company & Organizational Signals")

grid_col1, grid_col2 = st.columns(2)

with grid_col1:
    st.markdown("""
        <div class="card-box">
            <h4>🏢 Recent Company Events & News</h4>
            <p>{}</p>
            <p><strong>Strategic Developments:</strong> {}</p>
        </div>
    """.format(cust["events"], cust["news"]), unsafe_allow_html=True)

    st.markdown("""
        <div class="card-box">
            <h4>👔 Leadership Changes & Hiring</h4>
            <p><strong>Leadership Shifts:</strong> {}</p>
            <p><strong>Hiring Signals:</strong> {}</p>
        </div>
    """.format(cust["leadership"], cust["hiring"]), unsafe_allow_html=True)

with grid_col2:
    st.markdown("""
        <div class="card-box">
            <h4>📈 Product & Customer Usage Signals</h4>
            <p>{}</p>
        </div>
    """.format(cust["usage"]), unsafe_allow_html=True)

    st.markdown("""
        <div class="card-box" style="border-left: 4px solid #EF4444;">
            <h4>⚠️ Risks & Growth Opportunities</h4>
            <p>{}</p>
        </div>
    """.format(cust["risks_opps"]), unsafe_allow_html=True)

st.divider()

# SECTION 4: AI INSIGHT ENGINE
st.markdown("### 🤖 4. AI Insight Engine")
st.caption("Actionable recommendations derived from signal intelligence")

ai = cust["ai_analysis"]

st.markdown(f"""
    <div class="ai-box">
        <span class="badge-insight">STRATEGIC ACTIONABLE INSIGHT</span>
        <h3 style="color: #15803D; margin-top: 10px; margin-bottom: 10px;">Signal Briefing: {selected_customer}</h3>
        <p><strong>1. What Happened:</strong> {ai['what']}</p>
        <p><strong>2. Why It Matters:</strong> {ai['why']}</p>
        <p><strong>3. Recommended CSM Action:</strong> {ai['action']}</p>
        <div style="background-color: #FFFFFF; padding: 12px; border-radius: 6px; border: 1px dashed #16A34A; margin-top: 10px;">
            <p style="margin: 0; color: #166534;"><strong>💬 Suggested Talking Point / Outreach Draft:</strong></p>
            <p style="margin: 5px 0 0 0; font-style: italic; color: #334155;">{ai['talking_point']}</p>
        </div>
    </div>
""", unsafe_allow_html=True)

st.divider()
st.caption("Sirius Customer Intelligence Tool — Built for Hunar.AI CSM Assessment | Kanav Kundra")
