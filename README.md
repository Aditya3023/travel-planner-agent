# Personal Travel Planner Agent

A simple **Travel Planner Agent built with Google ADK**. It accepts a natural-language travel request and creates a practical day-wise itinerary with recommendations and an estimated budget.

## Features

- Understands destination, duration, budget, interests and travel style.
- Recommends attractions and local experiences.
- Estimates and allocates the trip budget.
- Creates a day-by-day itinerary.
- Suggests local food and practical travel tips.
- Uses a custom ADK tool (`estimate_trip_budget`).
- Works with the Google ADK local web playground.

## Project Files

```text
personal_travel_planner_agent/
├── agent.py
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.11+
- A Gemini API key **or** Google Cloud/Vertex AI authentication.
- Internet access for the Gemini model.

Google's current ADK documentation lists Python 3.11+ and supports local ADK playground workflows. The current ADK project examples use `google-adk` and the `Gemini` model class.

## 1. Create a virtual environment

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 3. Configure Gemini authentication

For a Gemini API key, set your key as an environment variable.

### Windows PowerShell

```powershell
$env:GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
```

### macOS/Linux

```bash
export GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
```

Do **not** put your API key inside `agent.py`, `README.md`, screenshots, GitHub, or the submission ZIP.

If your class/lab uses Google Cloud Vertex AI authentication instead, follow the authentication method provided by your instructor.

## 4. Run the agent

From the folder containing `agent.py`, run:

```bash
adk web
```

Open the local address printed by ADK in your browser.

Select the `personal_travel_planner` agent and enter a request such as:

```text
I want to visit Jaipur for 3 days with a budget of ₹15,000. I like history and local food.
```

The agent should return:
- requirement summary
- recommended places
- budget estimate
- Day 1 / Day 2 / Day 3 plan
- food suggestions
- practical tips
- final plan

## 5. Screenshot / video for submission

The assignment asks for a screenshot or video of the agent running.

After starting:

```bash
adk web
```

take a screenshot showing:
1. The ADK web interface.
2. Your user prompt.
3. The agent's generated itinerary.

For a stronger submission, record a short 30-60 second screen recording showing the prompt being entered and the final itinerary being generated.

**Important:** the screenshot/video should be captured from your own local running ADK environment. I have not included a fake "running" screenshot because that would not prove that the agent actually ran on your machine.

Suggested screenshot filename:

```text
travel_planner_running.png
```

Suggested video filename:

```text
travel_planner_demo.mp4
```

## 3 Example Conversations

### Example 1 — Jaipur

**User**

```text
I want to visit Jaipur for 3 days with a budget of ₹15,000. I like history and local food.
```

**Agent — expected style**

```text
Trip Summary
- Destination: Jaipur
- Duration: 3 days
- Budget: ₹15,000
- Interests: History + local food

Recommended places:
- Amber Fort
- City Palace
- Jantar Mantar
- Hawa Mahal
- Johari/Bapu Bazaar
- Local Rajasthani food experiences

Day 1
Morning: Amber Fort
Afternoon: Jaigarh/nearby heritage area
Evening: Hawa Mahal area and local market

Day 2
Morning: City Palace + Jantar Mantar
Afternoon: Old Jaipur exploration
Evening: Rajasthani dinner

Day 3
Morning: Albert Hall Museum
Afternoon: Local shopping and food
Evening: Relax / departure

Budget
- Accommodation
- Food
- Local transport
- Entry fees/activities
- Emergency buffer

The exact amounts are estimates and should be checked before booking.
```

### Example 2 — Goa

**User**

```text
Plan a 4-day Goa trip for two people under ₹25,000. We like beaches, cafés and sunset places. Keep it relaxed.
```

**Agent — expected behavior**

The agent should prioritize beaches, cafés and sunset spots, avoid overloading each day, estimate the ₹25,000 budget, and produce a relaxed four-day plan.

### Example 3 — Delhi

**User**

```text
I have ₹12,000 for a 3-day Delhi trip. I am interested in history, street food and museums. I prefer using public transport.
```

**Agent — expected behavior**

The agent should prioritize historical monuments, museums and street-food areas, use public transport in the plan, estimate the budget, and provide a practical three-day itinerary.

## Troubleshooting

### `adk` command not found

Make sure the virtual environment is activated and `google-adk` installed:

```bash
pip install -r requirements.txt
```

You can also verify:

```bash
pip show google-adk
```

### Authentication error

Check that `GOOGLE_API_KEY` is set correctly, or configure Google Cloud authentication if your environment uses Vertex AI.

### Port already in use

Stop another ADK/local server process, or use the port option supported by your installed ADK version.

## Notes

This is an educational itinerary-planning agent. It does not make bookings and does not provide guaranteed live prices or availability. Users should verify opening hours, ticket prices, transport schedules, weather and accommodation availability before travelling.

## References

Google ADK documentation:
https://google.github.io/adk-docs/

Google Agents CLI / ADK local workflow:
https://google.github.io/agents-cli/guide/hands-on-tutorial/

The current Google agent examples use an ADK `Agent`, a Gemini model, optional Python tool functions, and an `App` wrapper for serving.
