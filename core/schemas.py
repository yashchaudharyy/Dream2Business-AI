from pydantic import BaseModel, Field
from typing import List, Optional

# --- 1. Profile Analysis Agent Output ---
class ProfileAnalysisOutput(BaseModel):
    suitability_score: int = Field(..., description="Overall business readiness suitability score out of 100")
    strengths: List[str] = Field(..., description="Key professional and personal strengths identified from user profile")
    weaknesses_or_gaps: List[str] = Field(..., description="Potential gaps in experience, education, or skills for business startup")
    budget_feasibility: str = Field(..., description="Detailed feasibility analysis of the user's budget")
    local_constraints: List[str] = Field(..., description="Geographical or local market constraints based on location")
    recommended_focus_areas: List[str] = Field(..., description="Core industries or focus areas the user should target")

# --- 2. Business Ideas Agent Output ---
class BusinessIdea(BaseModel):
    idea_name: str = Field(..., description="Name of the business idea")
    description: str = Field(..., description="Brief concept description")
    target_industry: str = Field(..., description="The industry this business belongs to")
    alignment_score: int = Field(..., description="How well this idea aligns with the user's profile (1-100)")
    why_it_fits: str = Field(..., description="Explanation of why this idea fits the user's skills and interests")
    customer_segment: str = Field(..., description="Primary target customer segment")

class BusinessIdeasOutput(BaseModel):
    ideas: List[BusinessIdea] = Field(..., description="Top 3 business ideas aligned with the user profile")
    selection_rationale: str = Field(..., description="Summary of why these three ideas were chosen")

# --- 3. Market Research Agent Output ---
class MarketAnalysisOutput(BaseModel):
    selected_idea: str = Field(..., description="The name of the business idea being researched")
    demand_index: int = Field(..., description="Estimated market demand score (1-100)")
    market_size_estimation: str = Field(..., description="Overview of target market size (Local / National)")
    competitor_analysis: str = Field(..., description="Analysis of primary competitors (direct and indirect)")
    market_trends: List[str] = Field(..., description="Current trends driving demand in this industry")
    demand_validation_verdict: str = Field(..., description="Final verdict on whether the market is validated")

# --- 4. Financial Planning Agent Output ---
class StartupCostItem(BaseModel):
    item: str = Field(..., description="Item or category (e.g., equipment, licensing, marketing)")
    cost: float = Field(..., description="Estimated cost in USD")
    is_essential: bool = Field(..., description="Whether this cost is absolutely essential for day 1")

class RevenueProjection(BaseModel):
    month: int = Field(..., description="Month number (1-12)")
    forecasted_revenue: float = Field(..., description="Forecasted revenue in USD")
    assumptions: str = Field(..., description="Underlying assumptions for this forecast")

class FinancialPlanOutput(BaseModel):
    selected_idea: str = Field(..., description="The name of the business idea")
    itemized_startup_costs: List[StartupCostItem] = Field(..., description="List of startup costs")
    total_startup_cost: float = Field(..., description="Sum of startup costs")
    fixed_monthly_expenses: float = Field(..., description="Fixed expenses (rent, software, utilities)")
    variable_cost_per_unit: float = Field(..., description="Variable cost per unit/service sold")
    suggested_pricing_strategy: str = Field(..., description="Pricing strategy and suggested price point")
    revenue_projections: List[RevenueProjection] = Field(..., description="12-month revenue forecast")
    break_even_months: float = Field(..., description="Calculated break-even point in months")

# --- 5. Government Scheme Agent Output ---
class GovernmentScheme(BaseModel):
    scheme_name: str = Field(..., description="Name of the scheme or grant")
    provider: str = Field(..., description="Providing body (e.g. SBA, local government, ministry)")
    benefit_description: str = Field(..., description="Description of the benefits (funding, mentoring, tax exemption)")
    eligibility_criteria: str = Field(..., description="Eligibility criteria matching the user")
    application_steps: List[str] = Field(..., description="Step-by-step instructions to apply")

class GovernmentSupportOutput(BaseModel):
    applicable_schemes: List[GovernmentScheme] = Field(..., description="List of relevant government schemes and grants")
    local_business_registration_requirements: List[str] = Field(..., description="Basic business registration tasks for the user's location")

# --- 6. Launch Strategy Agent Output ---
class LaunchRoadmapOutput(BaseModel):
    week_1_setup_and_legal: List[str] = Field(..., description="Week 1 tasks: business registration, licensing, bank account setup")
    week_2_branding_and_product: List[str] = Field(..., description="Week 2 tasks: logo, website/landing page, defining MVP service/product")
    week_3_marketing_and_sales: List[str] = Field(..., description="Week 3 tasks: social media setup, initial cold outreach, ads launch")
    week_4_launch_and_feedback: List[str] = Field(..., description="Week 4 tasks: grand opening, gathering customer reviews, refining MVP")
    key_milestones: List[str] = Field(..., description="Primary success metrics for the first 30 days")

# --- 7. Risk Assessment Agent Output ---
class RiskItem(BaseModel):
    category: str = Field(..., description="Category: Financial, Operational, Market, or Legal")
    risk_description: str = Field(..., description="Description of the specific risk")
    severity: str = Field(..., description="Risk severity (Low / Medium / High)")
    probability: str = Field(..., description="Probability of occurrence (Low / Medium / High)")
    mitigation_strategy: str = Field(..., description="Actionable plan to mitigate the risk")

class RiskAssessmentOutput(BaseModel):
    identified_risks: List[RiskItem] = Field(..., description="Identified risks for the business")
    insurance_recommendations: List[str] = Field(..., description="Recommended insurances (e.g., general liability, professional indemnity)")
    regulatory_compliance_checklist: List[str] = Field(..., description="Checklist of regulatory and compliance requirements")
