import logging
import json

from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

from tools.calculator import calculate
from tools.text_utility import text_utility
from tools.weather import get_weather
from tools.unit_converter import convert_units

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

log = logging.getLogger("agent")

# --- Tool function declarations ---

CALCULATOR_FUNC = types.FunctionDeclaration(
    name="calculate",
    description="Evaluate a math expression. Supports +, -, *, /, %, ** (power). No variables or functions.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "expression": types.Schema(type=types.Type.STRING, description="The math expression to evaluate, e.g. '2 + 3 * 4'"),
        },
        required=["expression"],
    ),
)

TEXT_UTILITY_FUNC = types.FunctionDeclaration(
    name="text_utility",
    description="Perform a text operation on a string.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "text": types.Schema(type=types.Type.STRING, description="The input text."),
            "operation": types.Schema(
                type=types.Type.STRING,
                enum=["word_count", "char_count", "uppercase", "lowercase", "reverse"],
                description="The operation to perform.",
            ),
        },
        required=["text", "operation"],
    ),
)

WEATHER_FUNC = types.FunctionDeclaration(
    name="get_weather",
    description="Look up the current weather for a city using the Open-Meteo API.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "city": types.Schema(type=types.Type.STRING, description="City name, e.g. 'London' or 'Tokyo'."),
        },
        required=["city"],
    ),
)

CONVERT_UNITS_FUNC = types.FunctionDeclaration(
    name="convert_units",
    description="Convert a value between units. Supports length (m, km, cm, mm, mi, yd, in), weight (kg, g, mg, lb, oz), and temperature (C, F, K).",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "value": types.Schema(type=types.Type.NUMBER, description="The numeric value to convert."),
            "from_unit": types.Schema(type=types.Type.STRING, description="The source unit, e.g. 'kg', 'miles', 'Fahrenheit'."),
            "to_unit": types.Schema(type=types.Type.STRING, description="The target unit, e.g. 'lb', 'km', 'C'."),
            "category": types.Schema(
                type=types.Type.STRING,
                enum=["length", "weight", "temperature"],
                description="The conversion category.",
            ),
        },
        required=["value", "from_unit", "to_unit", "category"],
    ),
)

TOOLS = types.Tool(function_declarations=[
    CALCULATOR_FUNC,
    TEXT_UTILITY_FUNC,
    WEATHER_FUNC,
    CONVERT_UNITS_FUNC,
])

TOOL_DISPATCH = {
    "calculate": lambda args: calculate(args["expression"]),
    "text_utility": lambda args: text_utility(args["text"], args["operation"]),
    "get_weather": lambda args: get_weather(args["city"]),
    "convert_units": lambda args: convert_units(
        args["value"], args["from_unit"], args["to_unit"], args["category"]
    ),
}


def _has_function_call(response) -> bool:
    if not response.candidates:
        return False
    candidate = response.candidates[0]
    if not candidate.content or not candidate.content.parts:
        return False
    return any(p.function_call for p in candidate.content.parts if p.function_call)


def chat(user_message: str) -> dict:
    log.info("User message: %s", user_message)

    contents = [types.Content(role="user", parts=[types.Part(text=user_message)])]

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(tools=[TOOLS]),
        )
    except Exception as e:
        if "429" in str(e) or "Quota exceeded" in str(e) or "ResourceExhausted" in str(e):
            return {
                "reply": "API Rate limit (5 requests per minute) hit. Please wait a few seconds and try again!",
                "tool_calls": []
            }
        raise e

    tool_calls_log = []

    while _has_function_call(response):
        function_response_parts = []

        for part in response.candidates[0].content.parts:
            if not part.function_call:
                continue

            fc = part.function_call
            fn_name = fc.name
            fn_args = dict(fc.args)

            log.info("Tool call: %s(%s)", fn_name, fn_args)

            if fn_name not in TOOL_DISPATCH:
                result = f"Error: unknown tool '{fn_name}'"
                log.warning("Unknown tool requested: %s", fn_name)
            else:
                try:
                    result = TOOL_DISPATCH[fn_name](fn_args)
                except Exception:
                    log.exception("Tool '%s' raised an exception", fn_name)
                    result = f"Error: tool '{fn_name}' failed unexpectedly"

            log.info("Tool result: %s", result)

            tool_calls_log.append({
                "tool": fn_name,
                "args": fn_args,
                "result": result,
            })

            function_response_parts.append(
                types.Part.from_function_response(
                    name=fn_name,
                    response={"result": result},
                )
            )

        contents.append(response.candidates[0].content)
        contents.append(types.Content(role="user", parts=function_response_parts))

        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=contents,
                config=types.GenerateContentConfig(tools=[TOOLS]),
            )
        except Exception as e:
            if "429" in str(e) or "Quota exceeded" in str(e) or "ResourceExhausted" in str(e):
                reply = "API Rate limit hit mid-conversation. Here are the tools called so far."
                return {
                    "reply": reply,
                    "tool_calls": tool_calls_log
                }
            raise e

    reply = ""
    if response.text:
        reply = response.text

    if not reply.strip() and tool_calls_log:
        summaries = []
        for tc in tool_calls_log:
            summaries.append(f"{tc['tool']} returned: {tc['result']}")
        reply = " | ".join(summaries)

    log.info("Final reply (%d chars)", len(reply))
    return {
        "reply": reply,
        "tool_calls": tool_calls_log,
    }
