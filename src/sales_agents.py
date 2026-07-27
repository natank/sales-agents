"""CLI entry point for the Sales Agents system.

Collects prospect details, runs the three cold-email agents plus the sales
picker, and prints the results. Run as: uv run python src/sales_agents.py
"""

import asyncio
import sys

from dotenv import load_dotenv

from agents_def import (
    concise_agent,
    generate_email,
    pick_best_email,
    professional_agent,
    witty_agent,
)
from utils import (
    format_email_output,
    format_picker_output,
    get_prospect_input,
    log_error,
    user_error_message,
    validate_prospect_input,
)

EMAIL_AGENTS = [
    ("professional", professional_agent),
    ("witty", witty_agent),
    ("concise", concise_agent),
]


async def orchestrate_emails(prospect_context: dict[str, str]) -> dict[str, str | None]:
    """Run all three email-generation agents sequentially.

    A failure in one agent is caught and logged; the other agents still run.

    Args:
        prospect_context: Dict with keys 'company', 'industry', 'pain_point', 'outcome'.

    Returns:
        Dict mapping 'professional' | 'witty' | 'concise' to email text, or None
        for any agent that failed.
    """
    emails: dict[str, str | None] = {}
    for agent_key, agent in EMAIL_AGENTS:
        try:
            emails[agent_key] = await generate_email(agent, prospect_context)
        except RuntimeError as exc:
            log_error(f"Email generation failed for {agent_key}", exc)
            print(user_error_message(f"generating the {agent.name} email", exc))
            emails[agent_key] = None
    return emails


async def orchestrate_picker(
    emails: dict[str, str | None], prospect_context: dict[str, str]
) -> tuple[str | None, str]:
    """Run the sales picker agent against the generated emails.

    Args:
        emails: Output of orchestrate_emails().
        prospect_context: Same shape as passed to orchestrate_emails().

    Returns:
        (chosen_agent_name, reasoning) — chosen_agent_name is None if the
        picker could not be run or produced no usable result.
    """
    try:
        return await pick_best_email(emails, prospect_context)
    except RuntimeError as exc:
        log_error("Sales picker failed", exc)
        return None, user_error_message("selecting the best email", exc)


async def run(prospect_context: dict[str, str]) -> int:
    """Run the full email-generation and picker workflow, printing results.

    Returns:
        Process exit code: 0 on success, 1 if no emails could be generated.
    """
    emails = await orchestrate_emails(prospect_context)

    print("\n=== GENERATED SALES EMAILS ===\n")
    for agent_key, _agent in EMAIL_AGENTS:
        email = emails[agent_key]
        if email:
            print(format_email_output(agent_key, email))
        else:
            print(f"[{agent_key} email generation failed]\n")

    if not any(emails.values()):
        print("No emails could be generated. Please check the error messages above.")
        return 1

    chosen_agent, reasoning = await orchestrate_picker(emails, prospect_context)
    print(format_picker_output(chosen_agent, reasoning))
    return 0


def main() -> None:
    """CLI entry point: collect input, run the workflow, exit with the result code."""
    load_dotenv()

    prospect_context = get_prospect_input()
    try:
        validate_prospect_input(**prospect_context)
    except ValueError as exc:
        print(f"Invalid input: {exc}")
        sys.exit(1)

    exit_code = asyncio.run(run(prospect_context))
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
