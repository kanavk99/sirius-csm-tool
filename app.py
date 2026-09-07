import os
import streamlit as st
from google import genai
from google.genai import types

# Page Config
st.set_page_config(
    page_title="Sirius | Enterprise Customer Intelligence",
    page_icon="⚡",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #1E293B; margin-bottom: 0px; }
    .sub-header { font-size: 1rem; color: #64748B; margin-bottom: 25px; }
    .card { background-color: #F8FAFC; padding: 20px; border-radius: 10px; border: 1px solid #E2E8F0; margin-bottom: 15px; }
    .badge-risk { background-color: #FEE2E2; color: #991B1B; padding: 4px 8px; border-radius: 4px; font-weight: 600; font-size: 0.8rem; }
    .badge-growth { background-color: #DCFCE7; color: #166534; padding: 4px 8px; border-radius: 4px; font-weight: 600; font-size: 0.8rem; }
    .badge-insight { background-color: #E0F2FE; color: #075985; padding: 4px 8px; border-radius: 4px; font-weight: 600; font-size: 0.8rem; }
    </style>
""", unsafe_allow_html=True)

# Title & Subtitle
st.markdown('<div class="main-header">⚡ Sirius — Customer Intelligence Tool</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Empowering CSMs with real-time organizational signals and proactive value-add outreach.</div>', unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.title("📌 Navigation & Settings")
account_option = st.sidebar.selectbox(
    "Select Enterprise Account",
    ["TechCorp India (Sample)", "GlobalLogistics Ltd (Sample)", "Custom Account Search"]
)

# Initialize Gemini Client if API key is present
api_key = st.sidebar.text_input("Gemini API Key (Optional for Live Analysis)", type="password")
client = None
if api_key:
    client = genai.Client(api_key=api_key)
elif "GEMINI_API_KEY" in os.environ:
    client = genai.Client()

# Sample Data Store
SAMPLE_DATA = {
    "TechCorp India (Sample)": {
        "domain": "techcorp.in",
        "arr": "$250,000",
        "health_score": "82 (Healthy)",
        "renewal_date": "Nov 15, 2026",
        "internal_updates": [
            {"type": "GROWTH", "title": "Rapid Expansion", "desc": "Opened a new tech hub in Bengaluru, hiring 150+ engineers."},
            {"type": "RISK", "title": "Executive Departure", "desc": "VP of Engineering (Primary Champion) transitioned out last week."},
            {"type": "INSIGHT", "title": "Usage Spike", "desc": "Assessment completions increased by 35% in Q2 across DevOps teams."}
        ],
        "insight_today": "TechCorp is scaling their tech hiring in Bengaluru. Share how Hunar.AI's automated coding evaluations cut candidate screening time by 40% for regional hiring sprees."
    },
    "GlobalLogistics Ltd (Sample)": {
        "domain": "globallogistics.com",
        "arr": "$180,000",
        "health_score": "64 (At-Risk)",
        "renewal_date": "Oct 30, 2026",
        "internal_updates": [
            {"type": "RISK", "title": "Low Platform Engagement", "desc": "Active manager logins dropped by 22% over the last 30 days."},
            {"type": "GROWTH", "title": "Digital Transformation Mandate", "desc": "CEO announced a company-wide shift to AI-driven operations in Q3 earnings call."},
            {"type": "INSIGHT", "title": "Upskilling Need", "desc": "Supply chain team requires rapid re-skilling on warehouse management tools."}
        ],
        "insight_today": "Align with the CEO's AI initiative. Offer a custom skill-gap assessment benchmark tailored to supply chain digital transformation."
    }
}

# Account Details Context
if account_option in SAMPLE_DATA:
    data = SAMPLE_DATA[account_option]
    company_name = account_option.split(" (")[0]
    domain = data["domain"]
    arr = data["arr"]
    health = data["health_score"]
    renewal = data["renewal_date"]
    updates = data["internal_updates"]
    insight_today = data["insight_today"]
else:
    company_name = st.text_input("Enter Enterprise Name", "Infosys")
    domain = st.text_input("Enter Company Domain", "infosys.com")
    arr = "$300,000"
    health = "78 (Stable)"
    renewal = "Dec 31, 2026"
    updates = [
        {"type": "INSIGHT", "title": "Custom Account Mode", "desc": "Enter API key in sidebar to fetch live AI intelligence."}
    ]
    insight_today = f"Analyze public signals for {company_name} to generate proactive value."

# Top Metrics Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Account Name", company_name)
with col2:
    st.metric("Annual Contract Value", arr)
with col3:
    st.metric("Account Health Score", health)
with col4:
    st.metric("Renewal Date", renewal)

st.divider()

# Main Layout: Two Columns
left_col, right_col = st.columns([1, 1])

with left_col:
    st.subheader("🔍 What is happening inside my customer's organization?")
    st.caption("Internal telemetry + External organizational signals")

    for item in updates:
        badge_class = f"badge-{item['type'].lower()}"
        st.markdown(f"""
            <div class="card">
                <span class="{badge_class}">{item['type']}</span>
                <h4 style="margin-top: 8px; margin-bottom: 4px;">{item['title']}</h4>
                <p style="color: #475569; margin-bottom: 0;">{item['desc']}</p>
            </div>
        """, unsafe_allow_html=True)

    if client and st.button("✨ Fetch Live AI Intelligence Signals"):
        with st.spinner(f"Analyzing public signals and news for {company_name}..."):
            try:
                prompt = f"""
                Act as an Enterprise Customer Success Manager intelligence tool.
                Provide 3 concise strategic updates about the company '{company_name}' ({domain}).
                Categorize each update as either RISK, GROWTH, or INSIGHT.
                Focus on hiring trends, executive moves, technology adoption, or strategic shifts.
                Format as bullet points with category titles.
                """
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                st.markdown("### 🌐 Live Web Intelligence Summary")
                st.info(response.text)
            except Exception as e:
                st.error(f"Error fetching live updates: {str(e)}")

with right_col:
    st.subheader("💡 What useful insight can I share today?")
    st.caption("Proactive value-add outreach generator")

    st.markdown(f"""
        <div class="card" style="background-color: #EFF6FF; border-color: #BFDBFE;">
            <h4 style="color: #1E40AF; margin-top: 0;">Strategic Recommendation</h4>
            <p style="color: #1E3A8A; font-size: 0.95rem;">{insight_today}</p>
        </div>
    """, unsafe_allow_html=True)

    st.subheader("📧 Generate Executive Outreach Draft")
    outreach_type = st.selectbox(
        "Select Goal",
        ["Proactive Insight / Value Share", "Champion Departure Re-alignment", "Quarterly Value Review Booking"]
    )

    if st.button("🚀 Draft Personalized Email"):
        if client:
            with st.spinner("Drafting value-focused email..."):
                prompt = f"""
                Write a concise, highly professional executive email from a Customer Success Manager at Hunar.AI to a key decision-maker at {company_name}.
                Goal: {outreach_type}
                Context/Insight: {insight_today}
                Tone: Value-driven, consultative, non-salesy.
                Keep it under 150 words.
                """
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                st.text_area("Generated Outreach", response.text, height=220)
        else:
            # Fallback static draft if no API key provided
            sample_email = f"""Subject: Quick thought on {company_name}'s recent technical scaling

Hi Team,

Noticed {company_name}'s recent initiative around expanding technical teams in region.

When similar enterprise clients scale hiring rapidly, candidate screening bottlenecks often become a key friction point. We recently benchmarked how automated skill assessments reduced evaluation cycles by 40% while keeping quality high.

I put together a brief 2-page benchmark report tailored to your current stack—happy to share it over if useful.

Best regards,
Kanav Kundra
Customer Success Manager | Hunar.AI"""
            st.text_area("Generated Outreach (Sample)", sample_email, height=220)

st.divider()
st.caption("Sirius Customer Intelligence Dashboard — Prepared for Hunar.AI CSM Assessment")
