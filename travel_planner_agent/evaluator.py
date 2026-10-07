import asyncio
import json
import os
import re

from google import genai
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agent import root_agent


# -----------------------------
# Configuration
# -----------------------------

MODEL = "gemini-3.5-flash-lite"
APP_NAME = "travel_planner_evaluation"
USER_ID = "evaluation_user"

api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "API key not found. Set GOOGLE_API_KEY or GEMINI_API_KEY."
    )

judge_client = genai.Client(api_key=api_key)


# -----------------------------
# Load Dataset
# -----------------------------

with open("eval_dataset.json", "r", encoding="utf-8") as file:
    test_cases = json.load(file)


# -----------------------------
# Run Travel Planner Agent
# -----------------------------

async def run_agent(user_input, session_id):

    session_service = InMemorySessionService()

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id,
    )

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    message = types.Content(
        role="user",
        parts=[
            types.Part(text=user_input)
        ],
    )

    response_parts = []
    tool_used = False

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=message,
    ):

        # Check whether a tool/function was called
        try:
            if event.get_function_calls():
                tool_used = True
        except Exception:
            pass

        # Capture final text response
        if event.is_final_response():

            if event.content and event.content.parts:

                for part in event.content.parts:

                    if part.text:
                        response_parts.append(part.text)

    actual_response = "\n".join(response_parts)

    return actual_response, tool_used


# -----------------------------
# LLM-as-a-Judge
# -----------------------------

def evaluate_response(test_case, actual_response, tool_used):

    expected = "\n".join(
        f"- {item}"
        for item in test_case["expected_behavior"]
    )

    prompt = f"""
You are an evaluator for a Personal Travel Planner AI Agent.

Evaluate the actual agent response against the expected behavior.

Test Case:
{test_case["id"]}

User Input:
{test_case["input"]}

Expected Behavior:
{expected}

Actual Agent Response:
{actual_response}

Tool Used By Agent:
{tool_used}

Score these four metrics from 0.0 to 1.0:

1. Correctness
Does the response correctly handle the user's request?

2. Relevance
Does the response stay relevant to the user's request?

3. Completeness
Does the response contain the important information required by the expected behavior?

4. Tool Usage
Was the travel budget tool used appropriately?
- If the request requires budget estimation, tool usage should normally be 1.0 when the tool was used.
- If the request is invalid or outside the travel-planning scope and no tool is required, appropriate non-use should receive 1.0.
- Incorrect tool usage should reduce the score.

Calculate:

overall_score = average of the four metrics * 100

Return ONLY valid JSON.

Format:

{{
    "correctness": 0.0,
    "relevance": 0.0,
    "completeness": 0.0,
    "tool_usage": 0.0,
    "overall_score": 0.0,
    "reason": "Short explanation"
}}
"""

    response = judge_client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )

    text = response.text.strip()

    # Remove markdown code fences if Gemini adds them
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```\s*", "", text)

    return json.loads(text)


# -----------------------------
# Main Evaluation
# -----------------------------

async def main():

    print("\n")
    print("=" * 60)
    print("PERSONAL TRAVEL PLANNER - AUTOMATIC EVALUATION")
    print("=" * 60)

    results = []

    for test_case in test_cases:

        test_id = test_case["id"]

        print(f"\nRunning {test_id}...")
        print(f"Input: {test_case['input']}")

        try:

            actual_response, tool_used = await run_agent(
                test_case["input"],
                f"session_{test_id}",
            )

            print("Agent response generated successfully.")

            evaluation = evaluate_response(
                test_case,
                actual_response,
                tool_used,
            )

            result = {
                "test_case": test_id,
                "input": test_case["input"],
                "actual_response": actual_response,
                "tool_used": tool_used,
                "correctness": evaluation["correctness"],
                "relevance": evaluation["relevance"],
                "completeness": evaluation["completeness"],
                "tool_usage": evaluation["tool_usage"],
                "overall_score": evaluation["overall_score"],
                "reason": evaluation["reason"],
            }

            results.append(result)

            print(
                f"Score: {evaluation['overall_score']}%"
            )

        except Exception as error:

            print(f"FAILED: {error}")

            results.append({
                "test_case": test_id,
                "input": test_case["input"],
                "actual_response": "",
                "tool_used": False,
                "correctness": 0,
                "relevance": 0,
                "completeness": 0,
                "tool_usage": 0,
                "overall_score": 0,
                "reason": f"Evaluation failed: {error}",
            })


    # -----------------------------
    # Overall Score
    # -----------------------------

    if results:

        overall_score = sum(
            result["overall_score"]
            for result in results
        ) / len(results)

    else:

        overall_score = 0


    # -----------------------------
    # Failed Test Cases
    # -----------------------------

    failed_tests = []

    for result in results:

        if result["overall_score"] < 70:

            failed_tests.append({
                "test_case": result["test_case"],
                "score": result["overall_score"],
                "reason": result["reason"],
            })


    # -----------------------------
    # Final Results
    # -----------------------------

    final_results = {
        "total_test_cases": len(test_cases),
        "evaluated_test_cases": len(results),
        "overall_score": round(overall_score, 2),
        "failed_test_cases": failed_tests,
        "results": results,
    }


    with open(
        "evaluation_results.json",
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            final_results,
            file,
            indent=4,
            ensure_ascii=False,
        )


    print("\n")
    print("=" * 60)
    print("EVALUATION COMPLETED")
    print("=" * 60)
    print(f"Test Cases: {len(results)}")
    print(f"Overall Score: {overall_score:.2f}%")
    print(f"Failed Cases: {len(failed_tests)}")
    print("\nResults saved to evaluation_results.json")


# -----------------------------
# Start Program
# -----------------------------

if __name__ == "__main__":
    asyncio.run(main())