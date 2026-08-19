import logging

import google.generativeai as genai
from google.generativeai import protos
from dotenv import load_dotenv
import os

from tools.calculator import calculate
from tools.text_utility import text_utility
from tools.weather import get_weather
from tools.unit_converter import convert_units

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")

log = logging.getLogger("agent")

# --- Tool schemas using protos ---

SCHEMA = protos.Schema
TYPE = protos.Type

CALCULATOR_DECL = protos.FunctionDeclaration(
    name="calculate",
    description="Evaluate a math expression. Supports +, -, *, /, %, ** (power). No variables or functions.",
    parameters=SCHEMA(
        type_=TYPE.OBJECT,
        properties={
            "expression": SCHEMA(type_=TYPE.STRING, description="The math expression to evaluate, e.g. '2 + 3 * 4'"),
        },
        required=["expression"],
    ),
)

TEXT_UTILITY_DECL = protos.FunctionDeclaration(
    name="text_utility",
    description="Perform a text operation on a string.",
    parameters=SCHEMA(
        type_=TYPE.OBJECT,
        properties={
            "text": SCHEMA(type_=TYPE.STRING, description="The input text."),
            "operation": SCHEMA(
                type_=TYPE.STRING,
                enum=["word_count", "char_count", "uppercase", "lowercase", "reverse"],
                description="The operation to perform.",
            ),
        },
        required=["text", "operation"],
    ),
)

WEATHER_DECL = protos.FunctionDeclaration(
    name="get_weather",
    description="Look up the current weather for a city using the Open-Meteo API.",
    parameters=SCHEMA(
        type_=TYPE.OBJECT,
        properties={
            "city": SCHEMA(type_=TYPE.STRING, description="City name, e.g. 'London' or 'Tokyo'."),
        },
        required=["city"],
    ),
)

CONVERT_UNITS_DECL = protos.FunctionDeclaration(
    name="convert_units",
    description="Convert a value between units. Supports length (m, km, cm, mm, mi, yd, in), weight (kg, g, mg, lb, oz), and temperature (C, F, K).",
    parameters=SCHEMA(
        type_=TYPE.OBJECT,
        properties={
            "value": SCHEMA(type_=TYPE.NUMBER, description="The numeric value to convert."),
            "from_unit": SCHEMA(type_=TYPE.STRING, description="The source unit, e.g. 'kg', 'miles', 'Fahrenheit'."),
            "to_unit": SCHEMA(type_=TYPE.STRING, description="The target unit, e.g. 'lb', 'km', 'C'."),
            "category": SCHEMA(
                type_=TYPE.STRING,
                enum=["length", "weight", "temperature"],
                description="The conversion category.",
            ),
        },
        required=["value", "from_unit", "to_unit", "category"],
    ),
)

TOOLS = [protos.Tool(function_declarations=[
    CALCULATOR_DECL,
    TEXT_UTILITY_DECL,
    WEATHER_DECL,
    CONVERT_UNITS_DECL,
])]

# --- Dispatch map: name -> callable ---

TOOL_DISPATCH = {
    "calculate": lambda args: calculate(args["expression"]),
    "text_utility": lambda args: text_utility(args["text"], args["operation"]),
    "get_weather": lambda args: get_weather(args["city"]),
    "convert_units": lambda args: convert_units(
        args["value"], args["from_unit"], args["to_unit"], args["category"]
    ),
}


def _has_function_call(candidate) -> bool:
    if not candidate.content or not candidate.content.parts:
        return False
    return any(hasattr(p, "function_call") and p.function_call for p in candidate.content.parts)


def chat(user_message: str) -> dict:
    log.info("User message: %s", user_message)

    chat_session = model.start_chat(history=[])
    try:
        response = chat_session.send_message(user_message, tools=TOOLS)
    except Exception as e:
        if "429" in str(e) or "Quota exceeded" in str(e) or "ResourceExhausted" in str(e):
            return {
                "reply": "⚠️ Whoops! We hit the free-tier API rate limit (5 requests per minute). Please wait a few seconds and try again!",
                "tool_calls": []
            }
        raise e

    tool_calls_log = []

    while _has_function_call(response.candidates[0]):
        for part in response.candidates[0].content.parts:
            if not (hasattr(part, "function_call") and part.function_call):
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

        try:
            response = chat_session.send_message(
                response.candidates[0].content,
                tools=TOOLS,
            )
        except Exception as e:
            if "429" in str(e) or "Quota exceeded" in str(e) or "ResourceExhausted" in str(e):
                reply = "⚠️ API Rate Limit (5 requests per min) hit mid-conversation. Here are the tools called so far."
                return {
                    "reply": reply,
                    "tool_calls": tool_calls_log
                }
            raise e

    # Extract final text — try response.text first, fall back to parts
    reply = ""
    try:
        reply = response.text or ""
    except (ValueError, AttributeError):
        pass

    if not reply and response.candidates and response.candidates[0].content:
        for part in response.candidates[0].content.parts:
            if hasattr(part, "text") and part.text:
                reply += part.text

    # If the model returned no text but did call tools, build a summary
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
