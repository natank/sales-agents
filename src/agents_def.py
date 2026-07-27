"""Agent definitions and orchestration for the Sales Agents system.

Defines the three cold-email-writing personas (Professional, Witty, Concise)
and the sales picker agent that ranks their output, per docs/DESIGN.md § 2.
"""

from agents import Agent, Runner

PROSPECT_CONTEXT_TEMPLATE = """\
Prospect Company: {company}
Industry: {industry}
Pain Point: {pain_point}
Desired Outcome: {outcome}
"""

PROFESSIONAL_INSTRUCTIONS = """\
You are a professional, experienced B2B sales representative for TechFlow Solutions.
Your style is formal, corporate, and credentials-driven.
You emphasize:
- Proven ROI and risk mitigation
- Case studies and established clients
- Technical capabilities and compliance
- Long-term partnership value

When writing a cold sales email:
1. Address the prospect formally (e.g., "Dear [Prospect Title],")
2. Lead with a concrete problem statement or statistic
3. Position TechFlow as a trusted, established solution
4. Highlight relevant credentials, case studies, or industry recognition
5. Include a specific, low-pressure call-to-action (e.g., "book a 15-min discovery call")
6. Close professionally

Ensure the email is 150-250 words, grammatically perfect, and ready to send.
Output only the email (subject line, then body). No preamble or commentary.
"""

WITTY_INSTRUCTIONS = """\
You are a charismatic, witty sales rep for TechFlow Solutions.
Your style is conversational, clever, and personality-driven.
You excel at:
- Breaking through inbox clutter with humor and relatability
- Making technical concepts approachable and fun
- Building rapport quickly
- Standing out from generic corporate emails

When writing a cold sales email:
1. Open with a disarming observation, joke, or clever hook related to the prospect's pain
2. Use conversational language (avoid jargon where possible)
3. Show empathy for the prospect's situation
4. Introduce TechFlow as the solution, with a light touch
5. Use a casual, memorable sign-off
6. Invite the prospect to chat (not a formal "meeting")

Ensure the email is 120-200 words, feels genuine, and isn't trying too hard.
Keep humor tasteful and respectful; avoid anything offensive or off-brand.
Output only the email (subject line, then body). No preamble or commentary.
"""

CONCISE_INSTRUCTIONS = """\
You are a no-nonsense sales rep for TechFlow Solutions.
Your style is direct, scannable, and data-driven.
You assume the reader is busy and distracted.
You focus on:
- Leading with the value proposition (upfront, no fluff)
- Scannable bullet-point structure
- Quantifiable benefits where possible
- Minimal words; maximum impact

When writing a cold sales email:
1. Subject line: Action-oriented and clear (e.g., "Reduce Manual Workflow Time by 40%?")
2. Body: Short opening sentence (1 line)
3. 2-4 bullet points: Key benefits specific to the prospect's industry/pain
4. CTA: Single, specific action (e.g., "Book a 15-min demo here: [link]")
5. Signature: Name, title, company, brief one-liner

Ensure the email is scannable in 30 seconds. No paragraphs longer than 2 lines.
Every word earns its space.
Output only the email (subject line, then body). No preamble or commentary.
"""

SALES_PICKER_INSTRUCTIONS = """\
You are an experienced sales director at TechFlow Solutions.
Your role is to review multiple sales email options and recommend the best one
for a given prospect scenario.

When given three emails and prospect context:
1. Evaluate each email on:
   - Likelihood of opening (subject line strength, sender credibility)
   - Relevance to the prospect's pain point
   - Clarity of the value proposition
   - Persuasiveness of the CTA
   - Tone fit for the industry/persona

2. Select the ONE email most likely to convert for this specific prospect.

3. Respond in exactly this format, with no other text:
Best Email: The [Professional|Witty|Concise]
Reasoning: [1-2 sentences explaining why this email is most likely to convert.]

Do NOT rank all three; pick one and defend it clearly.
"""

professional_agent = Agent(
    name="The Professional",
    instructions=PROFESSIONAL_INSTRUCTIONS,
    model="gpt-4-mini",
)

witty_agent = Agent(
    name="The Witty",
    instructions=WITTY_INSTRUCTIONS,
    model="gpt-4-mini",
)

concise_agent = Agent(
    name="The Concise",
    instructions=CONCISE_INSTRUCTIONS,
    model="gpt-4-mini",
)

sales_picker_agent = Agent(
    name="Sales Picker",
    instructions=SALES_PICKER_INSTRUCTIONS,
    model="gpt-4-mini",
)


async def generate_email(agent: Agent, prospect_context: dict[str, str]) -> str:
    """Run one email-generation agent and return its email text.

    Args:
        agent: One of professional_agent, witty_agent, concise_agent.
        prospect_context: Dict with keys 'company', 'industry', 'pain_point', 'outcome'.

    Returns:
        The generated email text (subject line + body).

    Raises:
        RuntimeError: If the agent run fails (wraps the underlying SDK/API error).
    """
    prompt = PROSPECT_CONTEXT_TEMPLATE.format(**prospect_context)
    try:
        result = await Runner.run(agent, input=prompt)
    except Exception as exc:
        raise RuntimeError(f"Failed to generate email via {agent.name}: {exc}") from exc
    return result.final_output


async def pick_best_email(
    emails: dict[str, str], prospect_context: dict[str, str]
) -> tuple[str, str]:
    """Run the sales picker agent to select the best of the three emails.

    Args:
        emails: Dict with keys 'professional', 'witty', 'concise' mapping to email text.
            Entries with a falsy value (failed generation) are excluded from consideration.
        prospect_context: Same shape as generate_email's prospect_context.

    Returns:
        (chosen_agent_name, reasoning_text) — chosen_agent_name is one of
        "The Professional", "The Witty", "The Concise" as stated by the picker.

    Raises:
        RuntimeError: If the agent run fails or its output can't be parsed.
    """
    available = {name: text for name, text in emails.items() if text}
    if not available:
        raise RuntimeError("No emails available for the picker to evaluate.")

    labeled_emails = "\n\n".join(
        f"--- Email ({name.capitalize()}) ---\n{text}"
        for name, text in available.items()
    )
    prompt = (
        f"{PROSPECT_CONTEXT_TEMPLATE.format(**prospect_context)}\n"
        f"{labeled_emails}\n\n"
        "Which email is best, and why?"
    )

    try:
        result = await Runner.run(sales_picker_agent, input=prompt)
    except Exception as exc:
        raise RuntimeError(f"Failed to run sales picker: {exc}") from exc

    return parse_picker_output(result.final_output)


def parse_picker_output(output: str) -> tuple[str, str]:
    """Parse the picker agent's raw text into (chosen_agent, reasoning).

    Expects lines of the form "Best Email: ..." and "Reasoning: ...";
    matching is case-insensitive and tolerant of extra surrounding text.

    Args:
        output: Raw text returned by the sales picker agent.

    Returns:
        (chosen_agent_name, reasoning_text).

    Raises:
        RuntimeError: If no "Best Email:" line could be found.
    """
    output = output.strip()
    chosen_agent = ""
    reasoning = ""
    for line in output.splitlines():
        if line.lower().startswith("best email:"):
            chosen_agent = line.split(":", 1)[1].strip()
        elif line.lower().startswith("reasoning:"):
            reasoning = line.split(":", 1)[1].strip()

    if not chosen_agent:
        raise RuntimeError(f"Could not parse picker output: {output!r}")

    return chosen_agent, reasoning or output
