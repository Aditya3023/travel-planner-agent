from google.adk.agents import Agent


def estimate_trip_budget(
    days: int,
    budget_inr: float,
    travel_style: str = "mid-range",
) -> str:
    """Estimate a simple travel budget allocation."""

    if days < 1:
        return "Number of days must be at least 1."

    if budget_inr <= 0:
        return "Budget must be greater than zero."

    style = travel_style.lower()

    if style == "budget":
        hotel = 0.25
        food = 0.20
        transport = 0.15
        activities = 0.20
        buffer = 0.20

    elif style == "comfortable":
        hotel = 0.40
        food = 0.20
        transport = 0.10
        activities = 0.20
        buffer = 0.10

    else:
        hotel = 0.35
        food = 0.20
        transport = 0.15
        activities = 0.20
        buffer = 0.10

    return f"""
Total Budget: ₹{budget_inr:,.0f}
Trip Duration: {days} days
Average Daily Budget: ₹{budget_inr / days:,.0f}

Estimated Allocation:
- Accommodation: ₹{budget_inr * hotel:,.0f}
- Food: ₹{budget_inr * food:,.0f}
- Local Transport: ₹{budget_inr * transport:,.0f}
- Activities & Entry Fees: ₹{budget_inr * activities:,.0f}
- Emergency/Miscellaneous: ₹{budget_inr * buffer:,.0f}

This is an estimated budget. Actual prices may vary.
"""


root_agent = Agent(
    name="personal_travel_planner",
    model="gemini-3.5-flash-lite",
    description="A personal travel planner that creates budget-friendly itineraries.",
    instruction="""
You are a Personal Travel Planner Agent.

Your job is to understand the user's travel requirements
and create a practical travel itinerary.

Identify:
- Destination
- Number of days
- Budget
- Interests
- Travel style
- Special preferences

For each travel request:

1. Summarize the user's requirements.
2. Recommend important places to visit.
3. Recommend local food and experiences.
4. Use the estimate_trip_budget tool to estimate the budget.
5. Create a clear day-wise itinerary.
6. Organize nearby places together when possible.
7. Divide each day into Morning, Afternoon and Evening.
8. Compare the estimated budget with the user's budget.
9. Give practical travel tips.
10. Finish with a section called "Final Plan".

Do not claim live hotel availability or exact current prices.

Use Indian Rupees (₹) for the budget.

Keep the response clear, practical and easy to read.
""",
    tools=[estimate_trip_budget],
)