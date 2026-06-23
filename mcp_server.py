import sys
import logging
from typing import Dict, Any, List
from fastmcp import FastMCP

# Setup logging to stderr to prevent interference with stdio communication
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("Dream2BusinessMCP")

mcp = FastMCP("Dream2Business AI Toolserver")

@mcp.tool()
def fetch_market_demands(location: str, industry: str) -> Dict[str, Any]:
    """
    Fetches market demand indices, competitor density, and trending keywords for a location and industry.

    Args:
        location (str): The city, state, or country of operation.
        industry (str): The target industry sector (e.g., Tech, Retail, Food, Fitness).
    """
    logger.info(f"Fetching market demand for location={location}, industry={industry}")
    
    # Clean inputs
    loc = location.lower()
    ind = industry.lower()

    # Base values
    demand_index = 65
    competitors = "Moderate"
    trends = ["Digitalization of services", "Eco-friendly operations", "Personalized client experience"]
    
    if "tech" in ind or "ai" in ind or "software" in ind:
        demand_index = 88
        competitors = "High"
        trends = ["AI-agent workflows", "Low-code custom tooling", "Subscription-based pricing models"]
    elif "food" in ind or "restaurant" in ind or "cafe" in ind:
        demand_index = 75
        competitors = "Very High"
        trends = ["Plant-based options", "Contactless delivery integrations", "Local ingredient sourcing"]
    elif "fit" in ind or "gym" in ind or "health" in ind:
        demand_index = 80
        competitors = "Moderate"
        trends = ["Hybrid online/offline training", "Wearable device integration", "Mental wellness packages"]
    elif "sustain" in ind or "eco" in ind or "green" in ind:
        demand_index = 82
        competitors = "Low"
        trends = ["Circular economy models", "Carbon offsetting certifications", "Zero-waste packaging"]

    # Incorporate location factors
    if "austin" in loc or "silicon valley" in loc or "bangalore" in loc or "dallas" in loc:
        demand_index += 5
        competitors = "High" if competitors != "Very High" else "Very High"

    # Clamp demand index between 1 and 100
    demand_index = min(100, max(1, demand_index))

    return {
        "status": "success",
        "location": location,
        "industry": industry,
        "demand_index": demand_index,
        "competitor_density": competitors,
        "market_trends": trends,
        "demand_verdict": "High demand with healthy growth potential." if demand_index >= 75 else "Stable market demand with steady growth."
    }

@mcp.tool()
def calculate_financials(
    startup_costs: float,
    fixed_monthly_expenses: float,
    average_price: float,
    expected_sales: int
) -> Dict[str, Any]:
    """
    Calculates detailed financial forecasts including revenue, profit, break-even unit sales, and break-even timeline.

    Args:
        startup_costs (float): Initial capital investment required in USD.
        fixed_monthly_expenses (float): Fixed overhead costs (rent, utilities, software licenses) in USD.
        average_price (float): Average sale price per unit or service session in USD.
        expected_sales (int): Predicted monthly sales volume (number of units or sessions).
    """
    logger.info(f"Calculating financials: startup={startup_costs}, fixed={fixed_monthly_expenses}, price={average_price}, sales={expected_sales}")

    # Assume a standard 20% variable cost per unit (cost of goods sold, payment processing, packaging)
    variable_cost_per_unit = average_price * 0.20
    contribution_margin = average_price - variable_cost_per_unit

    monthly_revenue = average_price * expected_sales
    monthly_variable_costs = variable_cost_per_unit * expected_sales
    monthly_gross_profit = monthly_revenue - monthly_variable_costs
    monthly_net_profit = monthly_gross_profit - fixed_monthly_expenses

    # Calculate Break-Even Units (monthly)
    if contribution_margin > 0:
        break_even_units = fixed_monthly_expenses / contribution_margin
    else:
        break_even_units = 0.0

    # Calculate Break-Even Months (timeline to recover startup costs)
    if monthly_net_profit > 0:
        break_even_months = startup_costs / monthly_net_profit
    else:
        break_even_months = 999.0  # Represents positive cash flow never reached or infinite break-even

    # Generate 12-month projections (assuming 3% monthly compounding sales growth)
    revenue_projections = []
    current_sales = float(expected_sales)
    for m in range(1, 13):
        m_rev = average_price * current_sales
        m_var = variable_cost_per_unit * current_sales
        m_prof = m_rev - m_var - fixed_monthly_expenses
        revenue_projections.append({
            "month": m,
            "forecasted_revenue": round(m_rev, 2),
            "forecasted_profit": round(m_prof, 2),
            "sales_volume": int(current_sales)
        })
        current_sales *= 1.03  # 3% growth per month

    return {
        "status": "success",
        "monthly_revenue": round(monthly_revenue, 2),
        "monthly_net_profit": round(monthly_net_profit, 2),
        "break_even_units": round(break_even_units, 2),
        "break_even_months": round(break_even_months, 2) if break_even_months != 999.0 else "Infinite (> 10 years)",
        "total_startup_cost": round(startup_costs, 2),
        "variable_cost_per_unit": round(variable_cost_per_unit, 2),
        "twelve_month_forecast": revenue_projections
    }

@mcp.tool()
def search_government_schemes(location: str, industry: str) -> List[Dict[str, Any]]:
    """
    Retrieves government grants, microloans, tax relief, and business assistance schemes based on location and industry.

    Args:
        location (str): The state, region, or country of operation.
        industry (str): The target industry sector.
    """
    logger.info(f"Searching government schemes: location={location}, industry={industry}")
    
    loc = location.lower()
    ind = industry.lower()

    # Pre-defined schemes repository
    schemes = [
        {
            "scheme_name": "SBA Microloan Program",
            "provider": "US Small Business Administration (SBA)",
            "benefit_description": "Provides loans up to $50,000 to help small businesses and certain not-for-profit childcare centers start up and expand.",
            "eligibility_criteria": "Small business owner in the USA requiring startup or working capital.",
            "application_steps": ["Contact an SBA-approved intermediary lender in your state.", "Submit a formal business plan and credit history.", "Complete required business training/mentorship."]
        },
        {
            "scheme_name": "Startup India Seed Fund Scheme (SISFS)",
            "provider": "Department for Promotion of Industry and Internal Trade (DPIIT), India",
            "benefit_description": "Provides financial assistance of up to Rs. 20 Lakhs as grant for proof of concept/prototype development, and up to Rs. 50 Lakhs for market entry/commercialization.",
            "eligibility_criteria": "DPIIT-recognized startups incorporated within 2 years, with an innovative business concept.",
            "application_steps": ["Register startup on Startup India Portal.", "Apply for DPIIT Recognition.", "Submit SISFS application choosing preferred incubators."]
        },
        {
            "scheme_name": "SBA 7(a) Loan Guarantee Program",
            "provider": "US Small Business Administration (SBA)",
            "benefit_description": "Guarantees loans up to $5 million for real estate, equipment, inventory, and working capital with favorable interest rates.",
            "eligibility_criteria": "For-profit small businesses operating in the US, with reasonable owner equity to invest.",
            "application_steps": ["Find an SBA-approved lender using SBA Lender Match.", "Prepare financial statements, tax records, and business profile.", "Apply through the lender."]
        },
        {
            "scheme_name": "Local State Business Development Grant",
            "provider": "State Department of Commerce / State Economic Development",
            "benefit_description": "Grants ranging from $5,000 to $25,000 targeting local business development, technology innovation, or eco-friendly business setups.",
            "eligibility_criteria": "Registered local business committing to local hiring or sustainable business practices.",
            "application_steps": ["Check the state's official commerce website.", "Submit proof of local registration.", "Detail how the business supports the local community."]
        }
    ]

    applicable = []
    # US filter
    is_us = "us" in loc or "united states" in loc or "texas" in loc or "tx" in loc or "california" in loc or "ca" in loc or "dallas" in loc or "austin" in loc
    # India filter
    is_india = "india" in loc or "ind" in loc or "bangalore" in loc or "mumbai" in loc or "delhi" in loc

    for s in schemes:
        if "SBA" in s["scheme_name"] and not is_us:
            # Skip US SBA if user is explicitly in India (and vice versa)
            if is_india:
                continue
        if "SISFS" in s["scheme_name"] and not is_india:
            if is_us:
                continue
        applicable.append(s)

    # Add custom localized/industry grant if matched
    if "tech" in ind or "ai" in ind:
        applicable.append({
            "scheme_name": "Innovation & R&D Tax Incentive",
            "provider": "National Treasury / IRS",
            "benefit_description": "Up to 15-20% tax offset or deduction for qualifying research and development activities in software development and AI engineering.",
            "eligibility_criteria": "Registered company conducting technical research or novel software creation.",
            "application_steps": ["Log R&D project activities and technical challenges.", "File R&D tax claim form along with annual corporate tax return."]
        })

    return applicable

@mcp.tool()
def evaluate_industry_risks(industry: str) -> List[Dict[str, Any]]:
    """
    Retrieves standard risks, probability assessments, and mitigation checklists for a specific industry.

    Args:
        industry (str): The target business industry.
    """
    logger.info(f"Evaluating industry risks: industry={industry}")
    
    ind = industry.lower()

    # Default general risks
    risks = [
        {
            "category": "Financial",
            "risk_description": "Cash flow shortages due to delayed customer payments or higher-than-expected startup expenses.",
            "severity": "High",
            "probability": "Medium",
            "mitigation_strategy": "Maintain at least 3-6 months of operating expenses in reserve. Utilize upfront deposit models."
        },
        {
            "category": "Market",
            "risk_description": "Customer acquisition costs (CAC) exceeding lifetime value (LTV) due to intense local competition.",
            "severity": "Medium",
            "probability": "High",
            "mitigation_strategy": "Leverage organic content marketing, referral programs, and hyper-targeted local SEO rather than expensive broad ads."
        }
    ]

    if "tech" in ind or "software" in ind or "ai" in ind:
        risks.append({
            "category": "Operational",
            "risk_description": "Data breaches, cyberattacks, or system downtime affecting customer trust.",
            "severity": "High",
            "probability": "Medium",
            "mitigation_strategy": "Implement secure hosting (AWS/GCP), enable HTTPS, use OAuth for logins, and get Cyber Liability Insurance."
        })
        risks.append({
            "category": "Legal",
            "risk_description": "Intellectual property infringement disputes or regulatory compliance (GDPR/CCPA/SOC2) breaches.",
            "severity": "High",
            "probability": "Low",
            "mitigation_strategy": "Use open-source dependencies legally, draft strict terms of service, and perform regular data privacy audits."
        })
    elif "food" in ind or "restaurant" in ind or "cafe" in ind:
        risks.append({
            "category": "Operational",
            "risk_description": "Supply chain disruptions or food safety/health code violations causing temporary closure.",
            "severity": "High",
            "probability": "Medium",
            "mitigation_strategy": "Diversify food suppliers, implement rigorous standard operating procedures (SOPs) for kitchen hygiene, and schedule mock inspections."
        })
        risks.append({
            "category": "Legal",
            "risk_description": "Customer slips, trips, or food poisoning lawsuits.",
            "severity": "High",
            "probability": "Low",
            "mitigation_strategy": "Purchase comprehensive General Liability and Product Liability Insurance. Keep detailed logs of kitchen temperatures."
        })
    else:
        risks.append({
            "category": "Operational",
            "risk_description": "Key personnel dependency or service quality inconsistency.",
            "severity": "Medium",
            "probability": "Medium",
            "mitigation_strategy": "Standardize onboarding materials and create documented checklists for all business processes."
        })

    return risks

if __name__ == "__main__":
    # Runs the server using stdio transport by default
    mcp.run()
