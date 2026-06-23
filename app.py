import os
import streamlit as st
import pandas as pd
import json
import logging
from core.config import validate_profile_inputs, load_api_key, ValidationError
from core.workflow import ADKOrchestrator

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Dream2BusinessApp")

# Page Configuration
st.set_page_config(
    page_title="Dream2Business AI Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium CSS Styling for Sleek Dark Mode & Glassmorphism
st.markdown("""
<style>
    /* Import modern Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    /* Apply globally */
    * {
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3, .main-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        color: #ffffff;
    }
    
    /* Background gradient for main area */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(15, 19, 28) 0%, rgb(11, 13, 18) 100%);
    }
    
    /* Premium Title Accent */
    .main-title {
        background: linear-gradient(135deg, #a78bfa 0%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        margin-bottom: 0.2rem;
    }
    .tagline {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-style: italic;
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
        margin-bottom: 1.5rem;
    }
    .glass-header {
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 10px;
        margin-bottom: 15px;
        font-weight: 600;
        color: #38bdf8;
    }
    
    /* Metric Score Badge */
    .score-circle {
        background: conic-gradient(#8b5cf6 0% 80%, #334155 80% 100%);
        width: 100px;
        height: 100px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: auto;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3);
    }
    .score-inner {
        background: #0f172a;
        width: 84px;
        height: 84px;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .score-val {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
    }
    .score-label {
        font-size: 0.7rem;
        color: #94a3b8;
    }
    
    /* Actionable Timelines */
    .timeline-week {
        border-left: 3px solid #8b5cf6;
        padding-left: 20px;
        position: relative;
        margin-bottom: 25px;
    }
    .timeline-week::before {
        content: '';
        position: absolute;
        left: -8px;
        top: 0;
        width: 13px;
        height: 13px;
        border-radius: 50%;
        background: #38bdf8;
        box-shadow: 0 0 8px #38bdf8;
    }
    
    /* Badge Severity Colors */
    .badge {
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
    }
    .badge-high { background-color: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); }
    .badge-medium { background-color: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); }
    .badge-low { background-color: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); }
    
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "results" not in st.session_state:
    st.session_state.results = {}
if "execution_status" not in st.session_state:
    st.session_state.execution_status = "idle"  # idle, running, completed, failed
if "status_steps" not in st.session_state:
    st.session_state.status_steps = []
if "api_key" not in st.session_state:
    st.session_state.api_key = load_api_key()

# Sidebar: Inputs & Configurations
st.sidebar.markdown("<h2 style='text-align: center;'>📋 User Profile</h2>", unsafe_allow_html=True)

# API Key configuration
api_key_input = st.sidebar.text_input(
    "🔑 Gemini API Key",
    type="password",
    value=st.session_state.api_key,
    placeholder="Enter your Gemini API key...",
    help="Required to run the Gemini agent analysis."
)

if api_key_input:
    st.session_state.api_key = api_key_input
    os.environ["GEMINI_API_KEY"] = api_key_input
    os.environ["GOOGLE_API_KEY"] = api_key_input

st.sidebar.markdown("---")

# Profile input form
st.sidebar.markdown("### Tell us about yourself")
skills_in = st.sidebar.text_area("🔧 Skills", placeholder="e.g. Python, Web Development, Copywriting, Sales")
budget_in = st.sidebar.text_input("💵 Startup Budget ($)", placeholder="e.g. 5000", value="5000")
education_in = st.sidebar.selectbox("🎓 Education Level", [
    "High School Diploma",
    "Associate Degree",
    "Bachelor's Degree",
    "Master's Degree",
    "Ph.D. / Doctorate",
    "Self-Taught / Alternative Path"
])
location_in = st.sidebar.text_input("📍 Location", placeholder="e.g. Austin, Texas, USA")
interests_in = st.sidebar.text_area("💡 Interests / Passions", placeholder="e.g. AI technology, Sustainability, Coffee, E-learning")

run_button = st.sidebar.button(
    "🚀 Orchestrate System", 
    use_container_width=True,
    type="primary"
)

# Header Section
st.markdown("<h1 class='main-title'>Dream2Business AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='tagline'>\"From Dream to Business — One AI Agent Away.\"</p>", unsafe_allow_html=True)

# Orchestration logic execution
if run_button:
    if not st.session_state.api_key:
        st.error("🔑 Please provide a valid Gemini API Key in the sidebar to run the multi-agent analysis.")
    else:
        try:
            # 1. Input validation
            cleaned_inputs = validate_profile_inputs(
                skills=skills_in,
                budget=budget_in,
                education=education_in,
                location=location_in,
                interests=interests_in
            )
            
            # Reset results and set running state
            st.session_state.results = {}
            st.session_state.execution_status = "running"
            st.session_state.status_steps = []
            
            # Run agents sequentially
            orchestrator = ADKOrchestrator()
            
            # Show a progress panel
            with st.status("🤖 AI Agents Orchestrating...", expanded=True) as status_box:
                progress_generator = orchestrator.execute_full_analysis(
                    profile=cleaned_inputs,
                    user_id="streamlit_user",
                    session_id="session_db_1"
                )
                
                for agent_name, status, data in progress_generator:
                    step_key = f"{agent_name}_{status}"
                    if status == "running":
                        status_box.update(label=f"⏳ {agent_name} is analyzing...", state="running")
                    elif status == "completed":
                        status_box.write(f"✅ {agent_name} successfully finished!")
                        st.session_state.results[agent_name] = data
                    elif status == "failed":
                        status_box.update(label=f"❌ {agent_name} failed!", state="error")
                        st.session_state.execution_status = "failed"
                        st.error(f"Execution failed on {agent_name}: {data.get('error')}")
                        break
                
                if st.session_state.execution_status != "failed":
                    status_box.update(label="🎉 Orchestration Complete!", state="complete")
                    st.session_state.execution_status = "completed"
                    
        except ValidationError as ve:
            st.error(f"⚠️ Input Validation Error: {ve}")
        except Exception as e:
            st.error(f"💥 An unexpected error occurred: {e}")
            logger.exception("Error in orchestration run")

# Dashboard Content Render
if st.session_state.execution_status == "completed":
    # Render dashboard sections in tabs
    tabs = st.tabs([
        "👤 Profile Analysis", 
        "💡 Business Ideas", 
        "📈 Market Analysis", 
        "💵 Financial Plan", 
        "🏛️ Government Support", 
        "📅 Launch Roadmap", 
        "⚠️ Risk Assessment"
    ])
    
    # --- TAB 1: PROFILE ANALYSIS ---
    with tabs[0]:
        profile_data = st.session_state.results.get("ProfileAnalysisAgent", {})
        if profile_data:
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown("<div class='glass-card' style='text-align: center;'>", unsafe_allow_html=True)
                st.markdown("<p style='font-size:1.1rem; font-weight:600; color:#94a3b8;'>Suitability Index</p>", unsafe_allow_html=True)
                score = profile_data.get("suitability_score", 0)
                st.markdown(f"""
                <div class='score-circle' style='background: conic-gradient(#8b5cf6 0% {score}%, #334155 {score}% 100%);'>
                    <div class='score-inner'>
                        <div class='score-val'>{score}%</div>
                        <div class='score-label'>Feasible</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"<p style='margin-top: 15px; font-weight:600; color:#f87171;'>Budget Review:</p><p style='font-size:0.9rem;'>{profile_data.get('budget_feasibility', '')}</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            with col2:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("<div class='glass-header'>🔑 Core Capabilities & Suitability Analysis</div>", unsafe_allow_html=True)
                
                sc1, sc2 = st.columns(2)
                with sc1:
                    st.markdown("#### 💪 Key Strengths")
                    for strength in profile_data.get("strengths", []):
                        st.markdown(f"✅ {strength}")
                with sc2:
                    st.markdown("#### ⚠️ Experience Gaps")
                    for gap in profile_data.get("weaknesses_or_gaps", []):
                        st.markdown(f"🔸 {gap}")
                
                st.markdown("---")
                st.markdown("#### 🌍 Location & Market Constraints")
                for constr in profile_data.get("local_constraints", []):
                    st.markdown(f"📍 {constr}")
                
                st.markdown("#### 🎯 Suggested Focus Sectors")
                st.write(", ".join(profile_data.get("recommended_focus_areas", [])))
                st.markdown("</div>", unsafe_allow_html=True)

    # --- TAB 2: BUSINESS IDEAS ---
    with tabs[1]:
        ideas_data = st.session_state.results.get("BusinessIdeaAgent", {})
        if ideas_data:
            st.markdown(f"<div class='glass-card'><p style='font-style:italic;'>{ideas_data.get('selection_rationale', '')}</p></div>", unsafe_allow_html=True)
            
            ideas_list = ideas_data.get("ideas", [])
            for idx, idea in enumerate(ideas_list):
                # First idea is highlighted as top choice
                border_color = "border: 1px solid #8b5cf6;" if idx == 0 else "border: 1px solid rgba(255, 255, 255, 0.05);"
                badge_lbl = "🌟 TOP RECOMMENDED CANDIDATE" if idx == 0 else "💡 IDEA PROPOSAL"
                
                st.markdown(f"""
                <div class='glass-card' style='{border_color}'>
                    <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom: 12px;'>
                        <h3 style='margin:0; color:#38bdf8;'>{idea.get('idea_name')}</h3>
                        <span class='badge' style='background-color:#8b5cf6; color:white;'>Match Score: {idea.get('alignment_score')}%</span>
                    </div>
                    <p style='color:#a78bfa; font-weight:600; font-size:0.85rem; margin-top:-8px;'>{badge_lbl} | Industry: {idea.get('target_industry')}</p>
                    <p><strong>Concept:</strong> {idea.get('description')}</p>
                    <p><strong>🎯 Primary Target Audience:</strong> {idea.get('customer_segment')}</p>
                    <p style='background-color:rgba(255,255,255,0.02); padding: 12px; border-radius: 8px;'><strong>Why it fits you:</strong> {idea.get('why_it_fits')}</p>
                </div>
                """, unsafe_allow_html=True)

    # --- TAB 3: MARKET ANALYSIS ---
    with tabs[2]:
        market_data = st.session_state.results.get("MarketResearchAgent", {})
        if market_data:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='glass-header'>📈 Market Demand Validation: {market_data.get('selected_idea')}</div>", unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 2])
            with col1:
                d_idx = market_data.get("demand_index", 0)
                st.markdown(f"""
                <div style='text-align:center;'>
                    <p style='font-size:1.1rem; font-weight:600; color:#94a3b8;'>Demand Index</p>
                    <div class='score-circle' style='background: conic-gradient(#10b981 0% {d_idx}%, #334155 {d_idx}% 100%); margin-bottom: 20px;'>
                        <div class='score-inner'>
                            <div class='score-val' style='color:#34d399;'>{d_idx}/100</div>
                            <div class='score-label'>Hotness</div>
                        </div>
                    </div>
                    <span class='badge badge-low' style='font-size:1rem;'>Verdict: Verified</span>
                    <p style='font-size: 0.9rem; margin-top: 10px; color:#94a3b8;'>{market_data.get('demand_validation_verdict')}</p>
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                st.markdown(f"#### 📊 Target Market Size")
                st.write(market_data.get("market_size_estimation"))
                
                st.markdown(f"#### 🛡️ Local Competitor Density")
                st.markdown(f"Current Competition: **{market_data.get('competitor_density', 'Moderate')}**")
                st.write(market_data.get("competitor_analysis"))
                
                st.markdown("#### ⚡ Trending Keywords & Opportunities")
                for trend in market_data.get("market_trends", []):
                    st.markdown(f"🚀 {trend}")
            st.markdown("</div>", unsafe_allow_html=True)

    # --- TAB 4: FINANCIAL PLAN ---
    with tabs[3]:
        finance_data = st.session_state.results.get("FinancialPlanningAgent", {})
        if finance_data:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='glass-header'>💵 Financial Model: {finance_data.get('selected_idea')}</div>", unsafe_allow_html=True)
            
            # Metrics
            mc1, mc2, mc3 = st.columns(3)
            with mc1:
                st.metric("Total Startup Costs", f"${finance_data.get('total_startup_cost', 0.0):,.2f}")
            with mc2:
                st.metric("Fixed Expenses (Monthly)", f"${finance_data.get('fixed_monthly_expenses', 0.0):,.2f}")
            with mc3:
                st.metric("Break-Even Timeline", f"{finance_data.get('break_even_months', 0.0)} Months")
                
            st.markdown("---")
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### 🧱 Startup Budget Allocation")
                costs_list = finance_data.get("itemized_startup_costs", [])
                if costs_list:
                    df_costs = pd.DataFrame(costs_list)
                    # Clean columns for display
                    df_costs.columns = ["Startup Item", "Cost ($)", "Essential Day 1"]
                    st.table(df_costs)
                else:
                    st.info("No itemized cost data found.")
                    
            with c2:
                st.markdown("#### 🏷️ Recommended Pricing Strategy")
                st.write(finance_data.get("suggested_pricing_strategy", ""))
                st.markdown(f"**Variable Cost Per Unit:** ${finance_data.get('variable_cost_per_unit', 0.0):,.2f}")
                
            st.markdown("---")
            st.markdown("#### 📊 12-Month Profit & Cash Flow Projections")
            projections = finance_data.get("revenue_projections", [])
            if projections:
                df_proj = pd.DataFrame(projections)
                df_proj = df_proj.rename(columns={
                    "month": "Month",
                    "forecasted_revenue": "Revenue ($)",
                    "assumptions": "Assumptions"
                })
                # Check if we have forecasted_profit or cash_flow
                if "forecasted_profit" in df_proj.columns:
                    df_proj = df_proj.rename(columns={"forecasted_profit": "Net Profit ($)"})
                
                # Render clean table and chart
                st.line_chart(df_proj.set_index("Month")[["Revenue ($)", "Net Profit ($)"]] if "Net Profit ($)" in df_proj.columns else df_proj.set_index("Month")[["Revenue ($)"]])
                st.dataframe(df_proj, use_container_width=True)
            else:
                st.info("No revenue projection data found.")
            st.markdown("</div>", unsafe_allow_html=True)

    # --- TAB 5: GOVERNMENT SUPPORT ---
    with tabs[4]:
        gov_data = st.session_state.results.get("GovernmentSchemeAgent", {})
        if gov_data:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<div class='glass-header'>🏛️ Government Support, Grants & Registration</div>", unsafe_allow_html=True)
            
            st.markdown("### 📜 Local Business Registration Checklist")
            for req in gov_data.get("local_business_registration_requirements", []):
                st.markdown(f"⬜ {req}")
                
            st.markdown("---")
            st.markdown("### 🎁 Recommended Grants & Subsidy Schemes")
            for scheme in gov_data.get("applicable_schemes", []):
                with st.expander(f"💰 {scheme.get('scheme_name')} (Provider: {scheme.get('provider')})"):
                    st.markdown(f"**Benefit:** {scheme.get('benefit_description')}")
                    st.markdown(f"**Eligibility:** {scheme.get('eligibility_criteria')}")
                    st.markdown("**Application Guide:**")
                    for step in scheme.get("application_steps", []):
                        st.markdown(f"1. {step}")
            st.markdown("</div>", unsafe_allow_html=True)

    # --- TAB 6: LAUNCH ROADMAP ---
    with tabs[5]:
        roadmap_data = st.session_state.results.get("LaunchStrategyAgent", {})
        if roadmap_data:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<div class='glass-header'>📅 30-Day Tactical Launch Roadmap</div>", unsafe_allow_html=True)
            
            # Timeline styling
            w1 = roadmap_data.get("week_1_setup_and_legal", [])
            w2 = roadmap_data.get("week_2_branding_and_product", [])
            w3 = roadmap_data.get("week_3_marketing_and_sales", [])
            w4 = roadmap_data.get("week_4_launch_and_feedback", [])
            
            st.markdown("<div class='timeline-week'>", unsafe_allow_html=True)
            st.markdown("<h4 style='color:#a78bfa;'>Week 1: Setup & Legal Foundation</h4>", unsafe_allow_html=True)
            for item in w1:
                st.markdown(f"📋 {item}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='timeline-week'>", unsafe_allow_html=True)
            st.markdown("<h4 style='color:#a78bfa;'>Week 2: Branding & Product/Service Definition</h4>", unsafe_allow_html=True)
            for item in w2:
                st.markdown(f"🎨 {item}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='timeline-week'>", unsafe_allow_html=True)
            st.markdown("<h4 style='color:#a78bfa;'>Week 3: Launch Marketing & Client Acquisition</h4>", unsafe_allow_html=True)
            for item in w3:
                st.markdown(f"📣 {item}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='timeline-week'>", unsafe_allow_html=True)
            st.markdown("<h4 style='color:#a78bfa;'>Week 4: Official Launch & Feedback Loop</h4>", unsafe_allow_html=True)
            for item in w4:
                st.markdown(f"🚀 {item}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### 🏆 Milestone Objectives")
            for milestone in roadmap_data.get("key_milestones", []):
                st.markdown(f"🎯 {milestone}")
                
            st.markdown("</div>", unsafe_allow_html=True)

    # --- TAB 7: RISK ASSESSMENT ---
    with tabs[6]:
        risk_data = st.session_state.results.get("RiskAssessmentAgent", {})
        if risk_data:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<div class='glass-header'>⚠️ Risk Mitigation & Compliance Plan</div>", unsafe_allow_html=True)
            
            # Risk table
            risks_list = risk_data.get("identified_risks", [])
            for risk in risks_list:
                severity = risk.get("severity", "Medium")
                prob = risk.get("probability", "Medium")
                
                # Badge selector
                badge_class = "badge-medium"
                if severity.lower() == "high":
                    badge_class = "badge-high"
                elif severity.lower() == "low":
                    badge_class = "badge-low"
                    
                st.markdown(f"""
                <div style='background-color:rgba(255,255,255,0.015); padding: 16px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.03); margin-bottom: 12px;'>
                    <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom: 8px;'>
                        <strong style='color:#f87171;'>[{risk.get('category')}] {risk.get('risk_description')}</strong>
                        <div>
                            <span class='badge {badge_class}' style='margin-right:5px;'>Severity: {severity}</span>
                            <span class='badge' style='background-color:#475569; color:#cbd5e1;'>Probability: {prob}</span>
                        </div>
                    </div>
                    <p style='margin:0; font-size:0.9rem; color:#cbd5e1;'><strong>🛡️ Mitigation Strategy:</strong> {risk.get('mitigation_strategy')}</p>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("---")
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### 🧾 Regulatory Compliance Checklist")
                for comp in risk_data.get("regulatory_compliance_checklist", []):
                    st.markdown(f"⚖️ {comp}")
            with c2:
                st.markdown("#### 🛡️ Recommended Insurances")
                for ins in risk_data.get("insurance_recommendations", []):
                    st.markdown(f"💼 {ins}")
            st.markdown("</div>", unsafe_allow_html=True)
            
else:
    # Warm placeholder UI when st.session_state.results is empty
    st.markdown("<div class='glass-card' style='text-align: center; padding: 50px 20px;'>", unsafe_allow_html=True)
    st.markdown("<h3>👋 Welcome to Dream2Business AI</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size:1.05rem;'>Fill in your profile details in the left sidebar and click <strong>Orchestrate System</strong> to generate your tailored 30-day launch plan, financial forecasts, market research, and risk mitigations, driven by 7 collaborating AI agents.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style='background-color:rgba(255,255,255,0.01); padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.03);'>
            <h4 style='color:#a78bfa; margin-top:0;'>🤖 Multi-Agent Power</h4>
            <p style='font-size:0.9rem; color:#94a3b8;'>Seven specialized AI agents collaborate sequentially, refining ideas and validating details using real tools.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style='background-color:rgba(255,255,255,0.01); padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.03);'>
            <h4 style='color:#a78bfa; margin-top:0;'>⚙️ MCP Analytics Tools</h4>
            <p style='font-size:0.9rem; color:#94a3b8;'>Market validation, financial computations, and policy matches are calculated by standardized Model Context Protocol tools.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style='background-color:rgba(255,255,255,0.01); padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.03);'>
            <h4 style='color:#a78bfa; margin-top:0;'>🗓️ 30-Day Launch Path</h4>
            <p style='font-size:0.9rem; color:#94a3b8;'>Exit the platform with a ready-to-execute daily task list, legal compliance registration steps, and pricing strategies.</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
