# Sales Agents — Design Document

## 1. Architecture Overview

The Sales Agents system follows a **multi-agent orchestration pattern** with three parallel email-generation agents and one downstream picker agent. The architecture is layered as follows:

```
┌─────────────────────────────────────────┐
│  CLI Entry Point (sales_agents.py)      │
│  - Parse/validate user input            │
│  - Orchestrate agent workflow           │
│  - Format & print output                │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  Agent Orchestrator (agents_def.py)     │
│  - Define agent personas & instructions │
│  - Execute agent runs via SDK           │
│  - Collect results                      │
└─────────────────────────────────────────┘
              ↓
       [OpenAI API]
       - gpt-4-mini model
       - Agents SDK Runner
```

### Components

#### 1. `src/sales_agents.py` — Main CLI Entry
- **Responsibility:** User interface and workflow orchestration.
- **Inputs:** Prospect company, industry, pain point, desired outcome (via CLI args or prompts).
- **Outputs:** Printed emails and picker decision to stdout.
- **Flow:**
  1. Parse/validate CLI arguments.
  2. Call `orchestrate_emails(prospect_context)` to generate three emails.
  3. Call `orchestrate_picker(emails, prospect_context)` to select best email.
  4. Format and print all results.
  5. Handle errors gracefully.

#### 2. `src/agents_def.py` — Agent Definitions
- **Responsibility:** Define all agents, their personas, instructions, and execution logic.
- **Exports:**
  - `professional_agent`, `witty_agent`, `concise_agent` — three email generators.
  - `sales_picker_agent` — the ranking/selection agent.
  - `generate_email(agent, prospect_context) → str` — execute one agent and return email.
  - `pick_best_email(emails, prospect_context) → (agent_name, reasoning)` — execute picker.

#### 3. `src/utils.py` — Utilities
- **Responsibility:** Helper functions for formatting, validation, and error handling.
- **Exports:**
  - `format_email_output(agent_name, persona, email_text) → str` — pretty-print an email.
  - `format_picker_output(chosen_agent, reasoning) → str` — pretty-print picker decision.
  - `validate_prospect_input(company, industry, pain_point, outcome) → bool` — input validation.
  - Error logging and user-facing error messages.

## 2. Agent Definitions

Each agent is defined using the OpenAI Agents SDK's `Agent` class, specifying:
- A unique name.
- System instructions (persona, tone, style guide).
- The model (`gpt-4-mini`).
- No tools (tool-free for MVP).

### 2.1 Agent: "The Professional"

**Name:** `professional_agent`

**Persona:** Corporate, credentials-focused, formal tone.

**System Instructions (excerpt):**
```
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

Ensure the email is 150–250 words, grammatically perfect, and ready to send.
```

**Input Context:**
```
Prospect Company: {company}
Industry: {industry}
Pain Point: {pain_point}
Desired Outcome: {outcome}
```

**Expected Output Style:**
- Formal salutation ("Dear Operations Director,")
- Problem identification (backed by data if possible)
- Solution statement (TechFlow's key differentiators)
- Social proof / case study hint
- CTA (discovery call, product demo)
- Formal closing

### 2.2 Agent: "The Witty"

**Name:** `witty_agent`

**Persona:** Clever, conversational, personality-driven; uses humor.

**System Instructions (excerpt):**
```
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

Ensure the email is 120–200 words, feels genuine, and isn't trying too hard.
Keep humor tasteful and respectful; avoid anything offensive or off-brand.
```

**Expected Output Style:**
- Punchy, relatable opening
- Humor or clever observation
- Empathetic problem statement
- Informal solution pitch
- Conversational CTA ("Let's chat," "Coffee call?")
- Casual, personable closing

### 2.3 Agent: "The Concise"

**Name:** `concise_agent`

**Persona:** Direct, efficient, data-driven; respects reader's time.

**System Instructions (excerpt):**
```
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
3. 2–4 bullet points: Key benefits specific to the prospect's industry/pain
4. CTA: Single, specific action (e.g., "Book a 15-min demo here: [link]")
5. Signature: Name, title, company, brief one-liner

Ensure the email is scannable in 30 seconds. No paragraphs longer than 2 lines.
Every word earns its space.
```

**Expected Output Style:**
- Action-oriented subject
- Punchy opening (1–2 lines)
- 2–4 bullet-point benefits
- Specific, clickable CTA
- Minimal, clean signature

### 2.4 Agent: "The Sales Picker"

**Name:** `sales_picker_agent`

**Persona:** Discerning sales director; data-driven and experienced; makes judgment calls.

**System Instructions (excerpt):**
```
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

3. Provide your recommendation as:
   - Which email is best? (name the agent: "The Professional," "The Witty," or "The Concise")
   - Why? (1–2 sentence reasoning, e.g., "The prospect is in a formal enterprise
     environment and values credibility over cleverness. The Professional's
     emphasis on case studies and compliance will resonate better.")

Do NOT rank all three; pick one and defend it clearly.
```

**Input Context:**
- All three emails (email 1, email 2, email 3)
- Prospect company, industry, pain point, desired outcome

**Expected Output Format:**
```
Best Email: The [Agent Name]
Reasoning: [1–2 sentences explaining why this email is most likely to convert.]
```

## 3. Execution Flow

### 3.1 Email Generation (Three Agents in Parallel/Sequential)

```python
def orchestrate_emails(prospect_context: dict) -> dict[str, str]:
    """
    Execute all three email-generation agents.
    
    Args:
        prospect_context: {
            'company': str,
            'industry': str,
            'pain_point': str,
            'outcome': str,
        }
    
    Returns:
        {
            'professional': <email_text>,
            'witty': <email_text>,
            'concise': <email_text>,
        }
    """
    emails = {}
    
    # For MVP: sequential execution (avoids rate limit issues)
    # Future: can parallelize with asyncio or similar
    for agent_name, agent in [
        ('professional', professional_agent),
        ('witty', witty_agent),
        ('concise', concise_agent),
    ]:
        try:
            email = generate_email(agent, prospect_context)
            emails[agent_name] = email
        except Exception as e:
            # Log error, print user-friendly message, continue
            print(f"Error generating email for {agent_name}: {e}")
            emails[agent_name] = None
    
    return emails
```

### 3.2 Picker Execution

```python
def orchestrate_picker(emails: dict[str, str], prospect_context: dict) -> tuple[str, str]:
    """
    Execute the sales picker agent to select the best email.
    
    Args:
        emails: {'professional': ..., 'witty': ..., 'concise': ...}
        prospect_context: same as email generation
    
    Returns:
        (chosen_agent_name, reasoning_text)
    """
    try:
        chosen, reasoning = pick_best_email(emails, prospect_context)
        return chosen, reasoning
    except Exception as e:
        print(f"Error running picker: {e}")
        # Fallback: return None or a default
        return None, f"Unable to determine best email (error: {e})"
```

### 3.3 Output Formatting

```python
def main():
    # 1. Collect user input
    prospect = {
        'company': <input>,
        'industry': <input>,
        'pain_point': <input>,
        'outcome': <input>,
    }
    
    # 2. Generate emails
    emails = orchestrate_emails(prospect)
    
    # 3. Print emails
    print("\n=== GENERATED SALES EMAILS ===\n")
    for agent_name in ['professional', 'witty', 'concise']:
        email = emails[agent_name]
        if email:
            print(format_email_output(agent_name, email))
        else:
            print(f"[{agent_name} email generation failed]")
        print("\n" + "─" * 60 + "\n")
    
    # 4. Run picker
    chosen_agent, reasoning = orchestrate_picker(emails, prospect)
    
    # 5. Print picker result
    print("\n=== SALES PICKER RECOMMENDATION ===\n")
    print(format_picker_output(chosen_agent, reasoning))
```

## 4. Tool-Free Design (MVP)

All agents are **tool-free** in this MVP:
- No external function calls (no email validation, no prospect research, no web search).
- Agents rely entirely on LLM reasoning and instructions.
- Future iterations can add tools (e.g., company research, email validation, sentiment analysis).

## 5. Error Handling Strategy

### OpenAI API Errors
- **Authentication (401):** Print "Invalid API key. Check OPENAI_API_KEY environment variable."
- **Rate Limit (429):** Print "Rate limit reached. Please retry in a moment."
- **Network errors:** Print "Network error. Please check your connection and retry."
- **Other API errors:** Print a user-friendly generic message; log full error for debugging.

### Input Validation Errors
- **Missing fields:** Print usage message and exit.
- **Empty or suspicious input:** Warn user but proceed (LLM can handle some fuzziness).

### Agent Execution Failures
- **If one email agent fails:** Print "[agent_name] email generation failed"; continue with other agents.
- **If picker fails:** Print a fallback message, optionally default to the first email.

### Logging
- All errors logged to stderr or a debug log file (not shown to end user).
- Stack traces never printed to stdout.

## 6. Output Format Specification

### Email Output Template

```
═══════════════════════════════════════════════════════════════
AGENT: The Professional
PERSONA: Formal, credentials-focused, B2B expert
═══════════════════════════════════════════════════════════════

Subject: [Subject Line Here]

Dear Prospect,

[Email body here...]

Best regards,
[TechFlow Sales Team]

───────────────────────────────────────────────────────────────
```

Each email section is clearly labeled. Agents are numbered implicitly by order (Professional first, Witty second, Concise third).

### Picker Output Template

```
═══════════════════════════════════════════════════════════════
SALES PICKER RECOMMENDATION
═══════════════════════════════════════════════════════════════

Best Email: The Professional

Reasoning: This prospect values credibility and proven results. The Professional's
emphasis on case studies and ROI metrics aligns with their conservative
decision-making style in the finance industry.

───────────────────────────────────────────────────────────────
```

## 7. Data Flow Diagram

```
User Input
│
├─> company: "Acme Corp"
├─> industry: "Finance"
├─> pain_point: "Manual reconciliation delays"
└─> outcome: "Automate reconciliation"
    │
    ↓
[Prospect Context Dictionary]
    │
    ├──→ Professional Agent ──→ Email 1
    ├──→ Witty Agent ──────────→ Email 2
    └──→ Concise Agent ────────→ Email 3
    │
    ├──→ Format & Print All Three Emails
    │
    ├──→ [Emails 1, 2, 3] + [Prospect Context]
    │    │
    │    ↓
    └──→ Sales Picker Agent ──→ (Best Email, Reasoning)
         │
         ↓
    Format & Print Picker Result
```

## 8. Implementation Notes

### Code Style
- Follow PEP 8.
- Type hints for all function signatures.
- Docstrings for all functions (module-level and class-level).
- Clear, descriptive variable names.

### Dependencies
- `openai` (OpenAI Python SDK with Agents SDK)
- `python-dotenv` (for `.env` file support)

### Testing (Future Scope)
- Unit tests for `utils.py` functions (formatting, validation).
- Integration tests for agent runs (mock or live API).
- Example test scenarios with known prospect contexts.

### Deployment (Future Scope)
- Docker container for reproducible execution.
- GitHub Actions CI/CD for tests.
- Scheduled runs via cron or task scheduler.

## 9. Example Walkthrough

**Input:**
```
Company: StartupXYZ
Industry: FinTech
Pain Point: Manual CSV imports between legacy banking systems
Outcome: Reduce data-entry time by 50%
```

**Expected Output:**
```
=== GENERATED SALES EMAILS ===

[Professional Email with formal tone, ROI numbers, compliance focus, case study]

──────────────────────────────────────────────────────────────

[Witty Email with clever opening about "spreadsheet hell," casual tone, rapport-building]

──────────────────────────────────────────────────────────────

[Concise Email with subject line, 3 bullet points on time savings, scannable format]

──────────────────────────────────────────────────────────────

=== SALES PICKER RECOMMENDATION ===

Best Email: The Concise

Reasoning: FinTech founders are time-constrained and data-driven. The Concise email's
bullet-point format and focus on quantifiable time savings (50% reduction) will cut
through a busy inbox more effectively than corporate credentials or humor.
```

---

**Document Version:** 1.0  
**Last Updated:** 2026-07-27  
**Status:** Design finalized for MVP implementation
