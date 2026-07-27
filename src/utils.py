"""Formatting, validation, and error-handling helpers for the Sales Agents CLI."""

import logging
import sys

logger = logging.getLogger("sales_agents")
logging.basicConfig(
    level=logging.INFO, stream=sys.stderr, format="%(levelname)s: %(message)s"
)

DIVIDER = "─" * 65
HEADER_RULE = "═" * 65

AGENT_DISPLAY_NAMES = {
    "professional": "The Professional",
    "witty": "The Witty",
    "concise": "The Concise",
}

AGENT_PERSONAS = {
    "professional": "Formal, credentials-focused, B2B expert",
    "witty": "Clever, conversational, personality-driven",
    "concise": "Direct, scannable, data-driven",
}

REQUIRED_FIELDS = ("company", "industry", "pain_point", "outcome")


def validate_prospect_input(
    company: str, industry: str, pain_point: str, outcome: str
) -> bool:
    """Validate that all prospect fields are non-empty strings.

    Args:
        company: Prospect company name.
        industry: Prospect industry.
        pain_point: The problem the prospect is facing.
        outcome: The desired outcome for the prospect.

    Returns:
        True if all fields are present and non-blank.

    Raises:
        ValueError: If any field is missing or blank.
    """
    fields = {
        "company": company,
        "industry": industry,
        "pain_point": pain_point,
        "outcome": outcome,
    }
    missing = [name for name, value in fields.items() if not value or not value.strip()]
    if missing:
        raise ValueError(f"Missing required field(s): {', '.join(missing)}")
    return True


def get_prospect_input() -> dict[str, str]:
    """Prompt the user interactively for prospect details.

    Returns:
        Dict with keys 'company', 'industry', 'pain_point', 'outcome'.
    """
    print("Enter prospect details:\n")
    company = input("Company name: ").strip()
    industry = input("Industry: ").strip()
    pain_point = input("Pain point: ").strip()
    outcome = input("Desired outcome: ").strip()
    return {
        "company": company,
        "industry": industry,
        "pain_point": pain_point,
        "outcome": outcome,
    }


def format_email_output(agent_key: str, email_text: str) -> str:
    """Pretty-print a single generated email with a labeled header.

    Args:
        agent_key: One of 'professional', 'witty', 'concise'.
        email_text: The generated email body (subject line + body).

    Returns:
        A formatted, ready-to-print string block.
    """
    display_name = AGENT_DISPLAY_NAMES.get(agent_key, agent_key)
    persona = AGENT_PERSONAS.get(agent_key, "")
    return (
        f"{HEADER_RULE}\n"
        f"AGENT: {display_name}\n"
        f"PERSONA: {persona}\n"
        f"{HEADER_RULE}\n\n"
        f"{email_text}\n"
    )


def format_picker_output(chosen_agent: str | None, reasoning: str) -> str:
    """Pretty-print the sales picker's recommendation.

    Args:
        chosen_agent: The agent name the picker selected (e.g. "The Professional"),
            or None if the picker failed.
        reasoning: The picker's explanation for its choice.

    Returns:
        A formatted, ready-to-print string block.
    """
    if not chosen_agent:
        body = f"Best Email: (unavailable)\n\nReasoning: {reasoning}\n"
    else:
        body = f"Best Email: {chosen_agent}\n\nReasoning: {reasoning}\n"
    return f"{HEADER_RULE}\nSALES PICKER RECOMMENDATION\n{HEADER_RULE}\n\n{body}"


def log_error(message: str, exc: Exception | None = None) -> None:
    """Log an error for debugging without exposing internals to the user.

    Args:
        message: Human-readable context for the error.
        exc: The underlying exception, if any (logged with traceback).
    """
    logger.error(message, exc_info=exc is not None)


def user_error_message(context: str, exc: Exception) -> str:
    """Translate an exception into a short, friendly, user-facing message.

    Args:
        context: What was being attempted (e.g. "generating the Professional email").
        exc: The exception raised.

    Returns:
        A one-line, non-technical error message safe to print to the user.
    """
    text = str(exc).lower()
    if "api key" in text or "unauthorized" in text or "401" in text:
        detail = "Invalid API key. Check the OPENAI_API_KEY environment variable."
    elif "rate limit" in text or "429" in text:
        detail = "Rate limit reached. Please retry in a moment."
    elif "connection" in text or "timeout" in text or "network" in text:
        detail = "Network error. Please check your connection and retry."
    else:
        detail = "Something went wrong. Please try again."
    return f"Error {context}: {detail}"
