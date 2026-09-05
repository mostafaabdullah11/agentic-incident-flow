import json

from google import genai
from google.genai import types
from pydantic import ValidationError

from config import GEMINI_API_KEY, GEMINI_MODEL
from knowledge_base import load_kb_articles, format_kb_articles
from models import DecisionResult, IncidentPayload
from prompt_builder import build_prompt


# Temporary HTTP errors that are safe to retry.
RETRY_STATUS_CODES = [
    408,  # Request timeout
    429,  # Too many requests
    500,  # Internal server error
    502,  # Bad gateway
    503,  # Service unavailable
    504,  # Gateway timeout
]


def get_gemini_client():

    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    if not GEMINI_MODEL:
        raise RuntimeError("GEMINI_MODEL is not configured.")

    retry_options = types.HttpRetryOptions(
        attempts=3,
        initial_delay=1.0,
        max_delay=4.0,
        http_status_codes=RETRY_STATUS_CODES,
    )

    http_options = types.HttpOptions(
        retry_options=retry_options
    )

    return genai.Client(
        api_key=GEMINI_API_KEY,
        http_options=http_options,
    )


def parse_decision_response(response_text: str) -> DecisionResult:
    

    try:
        data = json.loads(response_text)

    except json.JSONDecodeError as exc:
        raise ValueError(
            "Gemini returned invalid JSON."
        ) from exc

    try:
        return DecisionResult.model_validate(data)

    except ValidationError as exc:
        raise ValueError(
            "Gemini returned JSON that does not match "
            "the required decision format."
        ) from exc


def decide_incident(
    incident: IncidentPayload
) -> DecisionResult:
    

    articles = load_kb_articles()

  
    knowledge_base = format_kb_articles(articles)

 
    prompt = build_prompt(
        knowledge_base=knowledge_base,
        number=incident.number,
        short_description=incident.short_description,
        description=incident.description,
        priority=incident.priority,
    )
    client = get_gemini_client()

  
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )

    if not response.text:
        raise ValueError(
            "Gemini returned an empty response."
        )

   
    return parse_decision_response(response.text)