# ai_analysis.py — Gemini does parsing, macros, status, recommendations
import re
import json
import google.generativeai as genai

# -------------------------
# PUT YOUR DIRECT API KEY HERE (replace the string)
# -------------------------
genai.configure(api_key="AIzaSyDEWS2dgfCw0nH73piStWdrDVCxySsvaZs")   # <-- replace with your key

MODEL_NAME = "gemini-2.5-flash"


def generate_ai_analysis(meals, water, snacks):
    """
    Sends raw user input to Gemini and returns a structured result.
    Gemini is asked to:
      - parse messy input into foods
      - estimate macros (carbs/protein/fat that sum to ~100)
      - classify as Balanced / Under Consumed / Over Consumed
      - give 3 recommendations and a short reward line
    The function extracts STATUS, MACROS (JSON), RECOMMENDATIONS, REWARD, and the full explanation text.
    """

    prompt = f"""
You are an expert AI Nutrition Coach and a careful parser.

User input:
Meals: {meals}
Snacks: {snacks}
Water: {water}

Task (do all of the following exactly):
1) Parse the above messy text into a clean list of foods (singular names).
2) Estimate daily macros for the total intake as percentages that SUM to ~100 (carbs, protein, fat). Round to 1 decimal.
3) Decide a single STATUS: Balanced, Under Consumed, or Over Consumed, with a one-sentence justification.
4) Provide exactly three clear, actionable recommendations.
5) Provide a short motivational reward sentence.

Return output EXACTLY in this format (no extra commentary):
STATUS: <Balanced / Under Consumed / Over Consumed>

MACROS:
{{
    "carbs": <number>,
    "protein": <number>,
    "fat": <number>
}}

RECOMMENDATIONS:
- <first recommendation>
- <second recommendation>
- <third recommendation>

REWARD: <short motivational sentence>

Important: macros must be numeric and the JSON block must be valid JSON. Keep the format identical to the above so it can be parsed programmatically.
"""

    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)
    text = response.text or ""

    # Extract STATUS
    status_match = re.search(r"STATUS:\s*(.*)", text)
    status = status_match.group(1).strip() if status_match else "Balanced"

    # Extract MACROS block (first {...} group)
    macro_match = re.search(r"\{[\s\S]*?\}", text)
    macros = {"carbs": 55.0, "protein": 20.0, "fat": 25.0}  # safe default
    if macro_match:
        macro_text = macro_match.group()
        try:
            # load JSON; allow single quotes -> replace with double quotes if needed
            macros = json.loads(macro_text)
            # normalize numeric types
            for k in ("carbs", "protein", "fat"):
                if k in macros:
                    try:
                        macros[k] = float(macros[k])
                    except:
                        macros[k] = float(macros.get(k, 0) or 0)
        except Exception:
            # try quick sanitization then reparse
            try:
                sanitized = macro_text.replace("'", '"')
                macros = json.loads(sanitized)
                for k in ("carbs", "protein", "fat"):
                    if k in macros:
                        macros[k] = float(macros[k])
            except Exception:
                macros = {"carbs": 55.0, "protein": 20.0, "fat": 25.0}

    # Extract recommendations (lines starting with "-")
    recs = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("-"):
            recs.append(line.lstrip("- ").strip())

    # Extract reward line
    reward_match = re.search(r"REWARD:\s*(.*)", text)
    reward = reward_match.group(1).strip() if reward_match else "Great job tracking today!"

    return {
        "status": status,
        "visual_data": macros,
        "recommendations": recs[:3],
        "reward": reward,
        "explanation": text
    }
